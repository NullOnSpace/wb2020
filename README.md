### Usage
#### Configure DATABASES option file
Add `my.cnf` to root dir, the content should be like this:
```
[client]
user=your_username
password=your_password
database=your_database_name
default-character-set=utf8mb4
```

#### Configure application key and secret
Add `weibo_app.ini` to root dir, the content should be like this:
```
[weibo]
key = the_app_key
secret = the_secret_string
redirect = http://yoursite.com/callback
```
The app key and app secret can be fetched after you have applied in the official website.

#### Configure `settings.py` extra options
This is only neccessary if you plant this app to another django project,
in the origin project these options are ready for you.
```
# Weibo
_config = configparser.ConfigParser()
_config.read(os.path.join(BASE_DIR, 'weibo_app.ini'))
WEIBO_APP_KEY = _config["weibo"]["key"]

WEIBO_APP_SECRET = _config["weibo"]["secret"]

WEIBO_REDIRECT_URI = _config["weibo"]["redirect"]

WEIBO_ACCESS_TOKEN_URL = "https://api.weibo.com/oauth2/access_token"

WEIBO_USER_DETAIL_URL = "https://api.weibo.com/2/users/show.json"
WEIBO_TIMELINE_URL = "https://api.weibo.com/2/statuses/home_timeline.json"
```
