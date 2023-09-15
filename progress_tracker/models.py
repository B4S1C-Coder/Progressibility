from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.exceptions import ValidationError
# from datetime import datetime

class ProgressibilityTask(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	content = models.CharField(max_length=200)
	dateadded = models.DateField('date added', auto_now_add=True, null=True)
	deadline = models.DateField('deadline', null=True, blank=True)
	completed = models.BooleanField('completed', default=False)

	def __str__(self):
		return f"{self.user.email}:{self.content}"

	def save(self, **kwargs):
		print("save was called; calling clean")
		self.clean()
		return super(ProgressibilityTask, self).save(**kwargs)

	def clean(self, *args, **kwargs):

		super().clean(*args, **kwargs)

		date_added = timezone.now().date()

		if self.deadline:

			if self.deadline < date_added:
				raise ValidationError("Deadline can't be before the date added.")

			# elif self.deadline < timezone.now().date():
			# 	raise ValidationError("Deadline can't be in the past.")

# ideally it should contain a 'progressibility_trends.something' key
# this key will contain an array of values that will be plotted.
# Graphs are always line charts (for now)
# an example json object could be as follows:

# {
# 	"progressibility.trends.maths": [98,99,100],
# 	"progressibility.trends.physics": [99,99,100],
# 	"progressibility.trends.chemistry": [90,91,100],
# 	"progressibility.title": "Test Performance Analysis",
# 	"progressibility.xaxis": ["12/03/2023","14/03/2023","16/03/2023"],
# 	"progressibility.yaxis.title": "Marks in Subject",
# 	"progressibility.xaxis.title": "Date"
# }

# HOW WILL THE USER INTERACT?

# OPTION-1: The user itself creates these fields and any additional
# fields that the user might like to display below the graph

# OPTION-2: The user interacts with an independent form which in turn
# creates the corressponding JSON.

# OPTION-1: Similiar to other forms
# OPTION-2: Will be a form independent of any model. The data of the form
# will be processed manually, and the JSON will be added to the database.

# we would also need to sanitize the user inputs to prevent any 
# SQL Injections etc.

# This would NOT exist on the dashboard page as, that could make the web
# page extremely heavy if the user has multiple trends (graphs).

class ProgressibilityTrend(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	dateadded = models.DateField('date added', auto_now_add=True, null=True)
	trend_name = models.CharField(max_length=100)
	trends = models.JSONField('trends')
