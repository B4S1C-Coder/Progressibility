from django import forms
from django.forms.widgets import Textarea, SelectDateWidget, TextInput
from .models import ProgressibilityTask, ProgressibilityTrend

class ProgressibilityTaskCreationForm(forms.ModelForm):
	content = forms.CharField(required=True, widget=Textarea(attrs={
				"class": "form-input",
				"placeholder": "Enter your task",
		}),label="Task")
	deadline = forms.DateField(required=True, widget=SelectDateWidget(attrs={
				"class": "form-input",
				"id": "form-date-input",
		}),label="Deadline")
	class Meta:
		model = ProgressibilityTask
		fields = ('content', 'deadline')

	def save(self, user, commit=True):
		# we assign user first to ensure super(...).save(...) works, since
		# task also has a user associated with it.
		# task.user = user
		task = super(ProgressibilityTaskCreationForm, self).save(commit=False)
		task.user = user
		task.content = self.cleaned_data['content']
		task.deadline = self.cleaned_data['deadline']

		if commit:
			task.save()

class ProgressibilityTaskUpdateForm(forms.ModelForm):
	content = forms.CharField(required=True, widget=Textarea(attrs={
				"class": "form-input",
				"placeholder": "Enter your Task",
		}), label="Task")
	deadline = forms.DateField(required=True, widget=SelectDateWidget(attrs={
				"class": "form-input",
				"id": "form-date-input",
				"width": "50px",
		}), label="Deadline")
	class Meta:
		model = ProgressibilityTask
		fields = ('content', 'deadline')

	def save(self, commit=True):
		task = super(ProgressibilityTaskUpdateForm, self).save(commit=False)
		task.content = self.cleaned_data['content']
		task.deadline = self.cleaned_data['deadline']

		if commit:
			task.save()

class ProgressibilityRAWTrendCreationForm(forms.ModelForm):
	trend_name = forms.CharField(required=True, widget=TextInput(attrs={
				"class": "form-input",
				"placeholder": "Trend Name"
		}), label="")
	trends = forms.JSONField(required=True, widget=Textarea(attrs={
				"class": "form-input",
				"placeholder": "Trends JSON",
		}), label="Trends")

	class Meta:
		model = ProgressibilityTrend
		fields = ('trend_name', 'trends')

	def save(self, user, commit=True):
		trend = super(ProgressibilityRAWTrendCreationForm,
						self).save(commit=False)
		trend.user = user
		trend.trend_name = self.cleaned_data['trend_name']
		trend.trends = self.cleaned_data['trends']

		if commit:
			trend.save()

######## Why am I not using formsets here? ########

# The trends field in the ProgressibilityRAWTrendCreationForm stores the JSON
# that is essentially used to visualize (generate detail page) the data.
# So, we are not actually storing the individual fields in a trend in a separate
# column/table in the database, we are storing the JSON object (which holds all
# the fields) in a column in the database.

# I don't want the user to be writing actual JSON when adding the data or fields.
# Instead I will use JS to add fields / data to the form on the client side.
# Additionally, a much better approach would be to get the user to upload a csv
# file and we either:

# 1) Generate JSON from the csv and store it in the database
# 2) Store the csv file on the server and generate the JSON for plotting everytime
# 3) We produce the JSON when the user uploads the csv file, instead of storing the
# csv file, we store the JSON in a json file on the server.

# We can normally use 1), but if the csv file exceeds a particular size, we use
# 3) and in the JSON field in the db we store {"progressibility.json": "path/to/json"}

class ProgressibilityTrendCreationForm(forms.Form):
	trend_name = forms.CharField(required=True, widget=TextInput(attrs={
				"class": "form-input",
				"placeholder": "Trend Name",
				"title": "This is the name of the trend and the title of the generated graph."
		}), label="")
	xaxis_field = forms.CharField(required=True, widget=TextInput(attrs={
				"class": "form-input",
				"placeholder": "X-axis field",
				"title": "Please enter a single field (create it, if not created). This will be used as the X-axis."
		}), label="")
	yaxis_title = forms.CharField(required=True, widget=TextInput(attrs={
				"class": "form-input",
				"placeholder": "Title for Y-Axis",
				"title": "This will be used as the title for Y-Axis in the graph."
		}), label="")
	xaxis_title = forms.CharField(required=True, widget=TextInput(attrs={
				"class": "form-input",
				"placeholder": "Title for X-Axis",
				"title": "This will be used as the title for X-Axis in the graph."
		}), label="")
	# rest of the things to be handled by JS on the client-side

class ProgressibilityRAWTrendUpdateForm(forms.ModelForm):
	trend_name = forms.CharField(required=True, widget=TextInput(attrs={
				"class": "form-input",
				"placeholder": "Trend Name"
		}), label="")
	trends = forms.JSONField(required=True, widget=Textarea(attrs={
				"class": "form-input",
				"placeholder": "Trends JSON",
		}), label="Trends")

	class Meta:
		model = ProgressibilityTrend
		fields = ('trend_name', 'trends')

	def save(self, commit=True):
		trend = super(ProgressibilityRAWTrendUpdateForm,
						self).save(commit=False)
		trend.trend_name = self.cleaned_data['trend_name']
		trend.trends = self.cleaned_data['trends']

		if commit:
			trend.save()
