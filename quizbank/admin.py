from django.contrib import admin

from .models import Question, Answer, ThreadTopic, ThreadPost, ForumUserData
# Register your models here.
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(ThreadTopic)
admin.site.register(ThreadPost)
admin.site.register(ForumUserData)