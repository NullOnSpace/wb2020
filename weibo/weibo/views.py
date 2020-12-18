from django.shortcuts import render
from django.views.generic import ListView
from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.db import transaction

from . import models

import json
import datetime

import requests

# Create your views here.
class FeedList(ListView):
    model = models.WeiboPost
    paginate_by = 30
    template_name = 'weibo/feedlist.html'

    def get_queryset(self):
        at = self.request.session.get('access_token')
        if at:
            post_list = _get_post_list(at)
            _persist_post_list(post_list)
        else:
            raise PermissionDenied
        return super().get_queryset()


def _get_post_list(at):
    url = settings.WEIBO_TIMELINE_URL
    res = requests.get(url, params={'access_token': at, "count": 150})
    if res.status_code == requests.codes.ok:
        return json.loads(res.content.decode('utf8')).get('statuses', {})
    else:
        return {}


def _persist_post_list(post_list):
    for post in post_list:
        with transaction.atomic():
            p = _extract_post_info(post)


def _extract_post_info(post):
    p, create_p = models.WeiboPost.objects.get_or_create(
        mid=post['mid'],
        defaults=dict(
            create=datetime.datetime.strptime(
            post["created_at"], "%a %b %d %X %z %Y"
            ),
            text=post["text"], source=post.get("source", ""),
        )
    )
    if create_p:
        user_info = post.get('user')
        if user_info:
            u, create_u = models.WeiboUser.objects.get_or_create(
                uid=user_info['id'],
                defaults=dict(
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
                ),
            )
            if create_u:
                u.save()
            p.author = u
            p.save()
        # pics handle
        pics = post.get("pic_urls", [])
        for order, pic in enumerate(pics, 1):
            url = pic['thumbnail_pic']
            pid = url.split("/")[-1].rsplit(".")[0]
            i = models.PostPic.objects.get_or_create(
                pid=pid,
                defaults={
                    'order': order, 'post': p, 'url': url,
                }
            )
        # retweet handle
        retweet = post.get('retweeted_status')
        if retweet:
            r = _extract_post_info(retweet)
            p.origin = r
    p.save()
    return p
