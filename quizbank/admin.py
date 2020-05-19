from django.contrib import admin

from .models import ThreadTopic, ThreadPost, ForumUserProfilePic, ForumPost
# Register your models here.
admin.site.register(ThreadTopic)
admin.site.register(ThreadPost)
admin.site.register(ForumUserProfilePic)
admin.site.register(ForumPost)