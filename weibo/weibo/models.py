from django.db import models

# Create your models here.
class WeiboPost(models.Model):
    mid = models.PositiveBigIntegerField()  # status['mid']
    create = models.DateTimeField()
    text = models.TextField()
    source = models.TextField()  # device info
    author = models.ForeignKey('WeiboUser', on_delete=models.CASCADE, null=True)
    origin = models.ForeignKey('self', on_delete=models.SET_NULL, null=True)

    class Meta:
        ordering = ('-create',)

    def __str__(self):
        return f"{self.text[:15]}"

class WeiboUser(models.Model):
    uid = models.CharField(max_length=50)
    nickname = models.CharField(max_length=20)
    description = models.CharField(max_length=120)
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
    user_ability = models.PositiveIntegerField()

    def __str__(self):
        return self.nickname


class PostPic(models.Model):
    pid = models.CharField(max_length=50)  # extract from url
    post = models.ForeignKey('WeiboPost', on_delete=models.CASCADE, null=True)
    order = models.PositiveSmallIntegerField()
    url = models.TextField()
