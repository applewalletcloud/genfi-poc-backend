from django.db import models
from django.utils import timezone
import datetime

# Model for keeping track of user profile pictures
class ForumUserProfilePic(models.Model):
	# we use usernames to map profile pics to the accounts
	user_name = models.CharField(max_length=200)
	# this specifies where the images will be held when they're uploaded
	profile_pic = models.ImageField(upload_to='media/images/')

	def __str__(self):
		return self.user_name

# Model for forum posts
class ForumPost(models.Model):
	is_main_post = models.BooleanField(default=False)
	post_id = models.IntegerField()
	main_post_id = models.IntegerField() # to allow quick filtering for queries
	parent_id = models.IntegerField(default=-1)
	creator = models.CharField(max_length=255)
	post_title = models.TextField() # this is the username for normal comments
	post_text = models.TextField()
	created_on = models.DateTimeField('date published', default=timezone.now())
	last_updated_on = models.DateTimeField('last updated', default=timezone.now())
	indentation_level = models.IntegerField(default=1)







