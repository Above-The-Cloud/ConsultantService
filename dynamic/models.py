import json

from django.db import models

# Create your models here.
from django.utils import timezone


class Dynamic(models.Model):
    user_id = models.IntegerField()
    # type = models.CharField(max_length=255,default='')
    # category = models.CharField(max_length=255, default='')
    title = models.CharField(max_length=255, default='')
    content = models.TextField(default='')
    tags=models.IntegerField(default=0,blank=True)
    images = models.TextField(default=json.dumps([]),blank=True)
    like_cnt = models.IntegerField(default=0)
    cmt_cnt = models.IntegerField(default=0)
    post_cnt = models.IntegerField(default=0)
    status = models.IntegerField(default=1, blank=True)
    ctime = models.DateTimeField(default = timezone.now)
    mtime = models.DateTimeField(auto_now = True)

class Comment(models.Model):
    dynamic_id = models.IntegerField()
    user_id=models.IntegerField()
    content = models.TextField(default='')
    images = models.TextField(default=json.dumps([]),blank=True)
    like_cnt = models.IntegerField(default=0)
    cmt_cnt = models.IntegerField(default=0)
    post_cnt = models.IntegerField(default=0)
    status = models.IntegerField(default=1, blank=True)
    ctime = models.DateTimeField(default = timezone.now)
    mtime = models.DateTimeField(auto_now = True)

class Reply(models.Model):
    comment_id = models.IntegerField()
    user_id=models.IntegerField()
    content = models.TextField(default='')
    # images = models.TextField(default=json.dumps([]),blank=True)
    like_cnt = models.IntegerField(default=0)
    # cmt_cnt = models.IntegerField(default=0)
    # post_cnt = models.IntegerField(default=0)
    status = models.IntegerField(default=1, blank=True)
    ctime = models.DateTimeField(default = timezone.now)
    mtime = models.DateTimeField(auto_now = True)