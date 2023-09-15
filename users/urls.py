from django.urls import path
from . import views

app_name = "users"

urlpatterns = [
	path("register", views.register_user, name="register"),
	path("logincheck", views.debug_logged_in, name="logincheck"),
	path("login", views.login_user, name="login"),
	path("logout", views.logout_user, name="logout"),
	path("update-avatar", views.update_avatar, name="updateavatar"),
	path("update-bio", views.update_bio, name="updatebio"),
]