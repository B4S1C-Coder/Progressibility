from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .forms import (
	ProgressibilityUserCreationForm, ProgressibilityUserAvatarUpdateForm,
	ProgressibilityUserBioUpdateForm, ProgressibilityUserAuthenticationForm
)
from . import users_config
from .models import ProgressibilityUserProfile

def register_user(request):
	if request.method == "POST":
		form = ProgressibilityUserCreationForm(request.POST)

		if form.is_valid():
			user = form.save()
			ProgressibilityUserProfile.objects.create(user=user)
			login(request, user)
			return redirect(users_config.LOGIN_REDIRECT_URL)

		# return HttpResponse(f"Registration unsuccessful. Please check the information entered. {form.errors}")
		return render(request=request, template_name="users/register.html",
						context={"register_form": form, "errors": form.errors})
		# return render(request=request, template_name="users/message.html",
		# 				context={
		# 					"message": "Registration unsuccessful. Please check the information entered.",
		# 					"urltogo": "users:register"
		# 					})
	form = ProgressibilityUserCreationForm()
	return render(request=request, template_name="users/register.html",
						context={"register_form": form})

def login_user(request):
	if request.method == "POST":
		form = ProgressibilityUserAuthenticationForm(request, data=request.POST)

		if form.is_valid():
			print("login form is valid")
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')

			user = authenticate(username=username, password=password)

			if user is not None:
				print(f"logging in: {username}")
				login(request, user)
				return redirect(users_config.LOGIN_REDIRECT_URL)

		return render(request=request, template_name="users/login.html",
				context={"login_form": form})

	form = ProgressibilityUserAuthenticationForm()
	return render(request=request, template_name="users/login.html",
						context={"login_form": form})

def logout_user(request):
	logout(request)
	return redirect(users_config.LOGOUT_REDIRECT_URL)

# This was used to test whether login worked or not, this is just a dummy dashboard
# and serves no purpose other than testing. Since, the actual dashboard could be a bit
# heavy (JS, CSS and other static files), this can be used in its place to test/troubleshoot
# any problems with the "users" app (which handles auth, login, logout, profile etc.).
@login_required
def debug_logged_in(request):
	# return HttpResponse(f"[DEBUG] successfully logged in as: {request.user.username}")
	user_profile = ProgressibilityUserProfile.objects.get(user=request.user)
	return render(request=request, template_name="users/debug_dashboard.html",
							context={
								"username": request.user.username,
								"firstname": request.user.first_name,
								"lastname": request.user.last_name,
								"email": request.user.email,
								"imgurl": user_profile.avatar.url
							})

@login_required
def update_avatar(request):
	if request.method == "POST":
		form = ProgressibilityUserAvatarUpdateForm(request.POST, request.FILES,
						instance=ProgressibilityUserProfile.objects.get(user=request.user))
		if form.is_valid():
			form.save()
			return redirect(users_config.USER_DASHBOARD_URL)

	else:
		form = ProgressibilityUserAvatarUpdateForm()

	return render(request=request, template_name="users/update_avatar.html",
					context={'form': form})

@login_required
def update_bio(request):
	if request.method == "POST":
		form = ProgressibilityUserBioUpdateForm(request.POST,
						instance=ProgressibilityUserProfile.objects.get(user=request.user))
		if form.is_valid():
			form.save()
			return redirect(users_config.USER_DASHBOARD_URL)

	else:
		# Here, we are putting the current bio in the form, so that the user doesn't
		# need to write the entire bio again.
		initial_bio = {
			"bio": ProgressibilityUserProfile.objects.get(user=request.user).bio
		}
		form = ProgressibilityUserBioUpdateForm(initial=initial_bio)

	return render(request=request, template_name="users/update_bio.html",
					context={'form': form})