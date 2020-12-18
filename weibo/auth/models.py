from django.db import models

# Create your models here.
class WeiboAccount(models.Model):
    """Account for authenticated weibo user"""

    access_token = models.CharField(max_length=50)
    uid = models.CharField(max_length=15)
    nickname = models.CharField(max_length=20)
    description = models.TextField()
    profile_image_url = models.TextField()
    profile_url = models.CharField(max_length=50)
    gender = models.CharField(max_length=5)
    followers_count = models.PositiveIntegerField()
    friends_count = models.PositiveIntegerField()
    created = models.DateTimeField()
    allow_all_comment = models.BooleanField()
    avatar = models.TextField()
    verified_reason = models.TextField()
    credit_score = models.PositiveIntegerField()
    user_ability = models.BigIntegerField()

    def __str__(self):
        return self.nickname
