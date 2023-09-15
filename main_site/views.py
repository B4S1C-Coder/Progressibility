from django.shortcuts import render

def guidelines(request):
	return render(request=request, template_name="guidelines.html")

def landing(request):
	return render(request=request, template_name="landing.html")

def unavailable(request):
	return render(request=request, template_name="unavailable.html")

def about(request):
	return render(request=request, template_name="about.html")