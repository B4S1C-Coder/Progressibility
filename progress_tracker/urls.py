from django.urls import path
from . import views

app_name = "progress_tracker"

urlpatterns = [
	path("dashboard", views.dashboard, name="dashboard"),
	path("add-task", views.add_task, name="addtask"),
	path("delete-task/<int:taskid>", views.delete_task, name="deletetask"),
	path("update-task/<int:taskid>", views.update_task, name="updatetask"),
	path("alter-task/<int:taskid>", views.alter_task_status, name="altertask"),
	path("add-trend-raw", views.add_trend, name="addtrendraw"),
	path("delete-trend/<int:trendid>", views.delete_trend, name="deletetrend"),
	path("update-trend-raw/<int:trendid>", views.update_trend, name="updatetrendraw"),
	path("detail-trend/<int:trendid>", views.detailed_trend, name="detailtrend"),
]