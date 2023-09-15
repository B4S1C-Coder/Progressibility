from django.db import models
from django.contrib.auth.models import User
import hashlib

class ProgressibilityUserProfile(models.Model):
	avatar = models.ImageField(upload_to='user_avatars/', null=True, blank=True,
					default='user_avatars/default_user.png')
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	bio = models.CharField(max_length=200, default='I use Progressibility to progress.')
	avatar_md5hash = models.CharField(max_length=32, null=True, blank=True)

	def __str__(self):
		return self.user.username

	def __calculate_md5hash(self) -> str:
		""" This function is meant to be used at the time of saving.
			This is to prevent duplication of avatars to a certain extent. """

		# Since, the instance isn't saved yet so we can't use self.avatar.path,
		# so we read the image and get the binary data. Reset the pointer so that
		# it can be saved correctly later on. Then we calculate the md5 hash.

		# NOTES TO SELF: models.ImageField and models.FileField are Django's File
		# objects. Refer: https://docs.djangoproject.com/en/4.2/topics/files/

		avatar_bin_data = self.avatar.read()
		self.avatar.seek(0)
		avatar_hash = hashlib.md5(avatar_bin_data).hexdigest()

		return avatar_hash

	def save(self, *args, **kwargs):
		if self.avatar:
			self.avatar_md5hash = self.__calculate_md5hash()

			# check if any other user(s) has(have) this avatar
			user_with_this_avatar = ProgressibilityUserProfile.objects.exclude(user=self.user).filter(avatar_md5hash=self.avatar_md5hash).first()

			if user_with_this_avatar:
				# if there is such a user then set thier avatar as the avatar
				self.avatar = user_with_this_avatar.avatar

		super().save(*args, **kwargs)

	def delete(self, *args, **kwargs):
		# we remove the refernces to the avatar hash and image because any other user MIGHT
		# have the same avatar (in turn same avatar hash)
		self.avatar_md5hash = None
		self.avatar = None
		self.save()
		super().delete(*args, **kwargs)