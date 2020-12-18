import datetime

from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse

import requests
import redis

from .models import WeiboAccount

# Create your views here.
def weibo_login(request):
    app_key = settings.WEIBO_APP_KEY
    redirect_uri = settings.WEIBO_REDIRECT_URI
    return render(request, 'weibo/login.html', {
        'app_key': app_key,
        'redirect_uri': redirect_uri,
    })


def auth_complete(request):
    app_key = settings.WEIBO_APP_KEY
    app_secret = settings.WEIBO_APP_SECRET
    redirect_uri = settings.WEIBO_REDIRECT_URI
    code = request.GET['code']
    res = requests.post(
        settings.WEIBO_ACCESS_TOKEN_URL,
        data={
            "client_id": app_key, "client_secret": app_secret,
            "grant_type": "authorization_code", "code": code,
            "redirect_uri": redirect_uri,
        },
    )
    print(res.text)
    if res.status_code == requests.codes.ok:
        response_json = res.json()
        access_token = response_json['access_token']
        expire = response_json['expires_in']
        uid = response_json['uid']
        R = redis.StrictRedis()
        R.set(access_token, uid, ex=int(expire))
        request.session['access_token'] = access_token
        request.session.set_expiry(int(expire))
        user_info_res = requests.get(settings.WEIBO_USER_DETAIL_URL,
            params={'access_token': access_token, 'uid':uid}
        )
        if user_info_res.status_code == requests.codes.ok:
            user_info = user_info_res.json()
            wa, create = WeiboAccount.objects.get_or_create(
                access_token=access_token,
                defaults=dict(
                    uid=uid,
                    nickname=user_info['name'],
                    description=user_info['description'],
                    profile_image_url=user_info['profile_image_url'],
                    gender=user_info['gender'],
                    followers_count=user_info['followers_count'],
                    friends_count=user_info['friends_count'],
                    created=datetime.datetime.strptime(
                    user_info['created_at'], "%a %b %d %X %z %Y"),
                    allow_all_comment=user_info['allow_all_comment'],
                    avatar=user_info['avatar_hd'],
                    verified_reason=user_info['verified_reason'],
                    credit_score=user_info['credit_score'],
                    user_ability=user_info['user_ability'],
                )
            )
            return HttpResponse("OK!")
    return HttpResponse("FAIL!!!")
