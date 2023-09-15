LOGIN_REDIRECT_URL = "progress_tracker:dashboard" # change to progress tracker
LOGOUT_REDIRECT_URL = "users:login"
# just another way to reference it, login_redirect may sound confusing when being
# used anywhere except the login view. It was used while making the users app when
# no dashboard page was availiable it loaded a dummy page to simulate a dashboard.
USER_DASHBOARD_URL = LOGIN_REDIRECT_URL