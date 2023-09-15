from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from datetime import datetime
import json
from contextlib import redirect_stdout
from users.models import ProgressibilityUserProfile
from .models import ProgressibilityTask, ProgressibilityTrend
from .forms import (
	ProgressibilityTaskCreationForm, ProgressibilityTaskUpdateForm,
	ProgressibilityRAWTrendCreationForm, ProgressibilityRAWTrendUpdateForm,
	ProgressibilityTrendCreationForm
)
from . import pt_validators

@login_required
def dashboard(request):
	user_profile = ProgressibilityUserProfile.objects.get(user=request.user)

	# try:
	# 	user_tasks = [ProgressibilityTask.objects.get(user=request.user)]
	# except Exception as err:
	# 	user_tasks = []

	user_tasks = ProgressibilityTask.objects.filter(user__id=request.user.id)
	user_trends = ProgressibilityTrend.objects.filter(user__id=request.user.id)

	return render(request=request, template_name="progress_tracker/dashboard.html",
							context={
								"username": request.user.username,
								"firstname": request.user.first_name,
								"lastname": request.user.last_name,
								"email": request.user.email,
								"imgurl": user_profile.avatar.url,
								"bio": user_profile.bio,
								"datejoin": request.user.date_joined.strftime('%d/%m/%Y'),
								"usertasks": user_tasks,
								"usertrends": user_trends,
							})

@login_required
def add_task(request):
	if request.method == "POST":
		form = ProgressibilityTaskCreationForm(request.POST)

		if form.is_valid():
			form.save(user=request.user)
			return redirect('progress_tracker:dashboard')

	form = ProgressibilityTaskCreationForm()
	return render(request, template_name="progress_tracker/addtask.html",
							context={"form": form, "errors": form.errors})

@login_required
def alter_task_status(request, taskid):
	task = ProgressibilityTask.objects.filter(id=taskid).first()
	if task:

		if task.user != request.user:
			return HttpResponse("Access denied.")

		if not task.completed:
			task.completed = True
		else:
			task.completed = False
		task.save()
	return redirect('progress_tracker:dashboard')

@login_required
def delete_task(request, taskid):
	task = ProgressibilityTask.objects.filter(id=taskid).first()
	if task:

		if task.user != request.user:
			return HttpResponse("Access denied.")
		
		task.delete()

	return redirect('progress_tracker:dashboard')

@login_required
def update_task(request, taskid):
	task = ProgressibilityTask.objects.filter(id=taskid).first()

	if task:

		if task.user != request.user:
			return HttpResponse("Access denied.")

		if request.method == "POST":

			form = ProgressibilityTaskUpdateForm(request.POST, instance=task)

			if form.is_valid():
				form.save()
				return redirect('progress_tracker:dashboard')

		else:

			initial = {
				"content": task.content,
				"deadline": task.deadline
			}

			form = ProgressibilityTaskUpdateForm(initial=initial)
			return render(request, template_name="progress_tracker/updatetask.html",
								context={"form": form,})

	else:
		return HttpResponse(f"'{taskid}' does not exist.")

@login_required
def add_trend(request):
	if request.method == "POST":
		form = ProgressibilityTrendCreationForm(request.POST)

		if form.is_valid():
			# form.save(user=request.user)
			# In order to see, if the fields added to the form via JS in frontend
			# is accessible in django or not. Here, we temporarily change the
			# standard output to the file output.txt and see if the new keys have been
			# added or not.
			# with open("output_checkbox.txt", "w") as f:
			# 	with redirect_stdout(f):
			# 		print(form.cleaned_data)
			# 		print(dict(request.POST))
			# 		for i in form.cleaned_data:
			# 			print(i)
			trend_dict = dict(request.POST)
			data_to_plot_dict = pt_validators.trend_validator(trend_dict)
			if data_to_plot_dict["progressibility.trend_validator.status_code"] != 1:

				# for key in data_to_plot_dict:
				# 	if key.startswith("progressibility.trend_validator"):
				# 		data_to_plot_dict.pop(key)

				# equivalent_json_obj = json.dumps(data_to_plot_dict)

				with open("debug_trend_addition.txt", "w") as f:
					with redirect_stdout(f):
						print(trend_dict)
						print("\n")
						print(data_to_plot_dict)

				trend = ProgressibilityTrend(user=request.user,
						trend_name=data_to_plot_dict["progressibility.title"],
						trends=data_to_plot_dict)
				trend.save()
			
			return redirect("progress_tracker:dashboard")

	form = ProgressibilityTrendCreationForm()
	return render(request=request, template_name="progress_tracker/addtrend.html",
								context={"form": form,})

@login_required
def update_trend(request, trendid):
	trend = ProgressibilityTrend.objects.filter(id=trendid).first()

	if trend:

		if trend.user != request.user:
			return HttpResponse("Access denied.")

		if request.method == 'POST':

			# form = ProgressibilityRAWTrendUpdateForm(request.POST, instance=trend)
			form = ProgressibilityTrendCreationForm(request.POST)

			if form.is_valid():
				trend_dict = dict(request.POST)
				data_to_plot_dict = pt_validators.trend_validator(trend_dict)

				if data_to_plot_dict["progressibility.trend_validator.status_code"] != 1:
					trend.trend_name = data_to_plot_dict["progressibility.title"]
					trend.trends = data_to_plot_dict
					trend.save()
				# form.save()
				return redirect('progress_tracker:dashboard')

			else:
				return HttpResponse(form.errors)

		else:

			# initial = {
			# 	"trend_name": trend.trend_name,
			# 	"trends": trend.trends
			# }

			# form = ProgressibilityRAWTrendUpdateForm(initial=initial)
			# return render(request, template_name="progress_tracker/updatetrendraw.html",
			# 					context={"form": form,})

			form = ProgressibilityTrendCreationForm()
			return render(request, template_name="progress_tracker/updatetrend.html",
								context={"form": form, "trendattrs": trend.trends})

	else:
		return HttpResponse(f"'{trendid}' does not exist.")

@login_required
def delete_trend(request, trendid):
	trend = ProgressibilityTrend.objects.filter(id=trendid).first()

	if trend:

		if trend.user != request.user:
			return HttpResponse("Access denied.")
		
		trend.delete()
	return redirect("progress_tracker:dashboard")

@login_required
def detailed_trend(request, trendid):
	trend = ProgressibilityTrend.objects.filter(id=trendid).first()

	if trend:
		# trend.trends is a dict
		# output = "".join([f"{i}: {trend.trends[i]}<br>" for i in trend.trends])
		# return HttpResponse(output)

		if trend.user != request.user:
			return HttpResponse("Access denied.")
		
		return render(request=request, template_name="progress_tracker/detail.html",
								context={
									"trendname": trend.trend_name,
									# "trendattrs": json.loads(trend.trends.replace('\'', '"')),
									"trendattrs": trend.trends
								})

	return HttpResponse(f"'{trendid}' does not exist.")