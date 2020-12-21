from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.urls import reverse

User = get_user_model()


def index(request):
	if request.user.is_authenticated:
		users = User.objects.select_related('logged_in_user')
		for user in users:
			user.status = 'online' if hasattr(user, 'logged_in_user') else 'offline'
			print(hasattr(user, 'logged_in_user'))

		return render(request, 'users_hub/index.html', {'users': users})
	else:
		return HttpResponseRedirect(reverse('register'))


def login_view(request):
	TEMPLATE_NAME = 'users_hub/login.html'
	
	if request.method == "POST":
		# Attempt to sign user in
		email = request.POST["email"]
		password = request.POST["password"]
		user = authenticate(request, username=email, password=password)

		# Check if authentication successful
		if user is not None:
			login(request, user)
			return HttpResponseRedirect(reverse("index"))
		else:
			return render(request, TEMPLATE_NAME, {
				"message": "Invalid email and/or password."
			})
	else:
		return render(request, TEMPLATE_NAME)


def logout_view(request):
	logout(request)
	return HttpResponseRedirect(reverse('login'))


def register(request):
	from django.db import IntegrityError

	TEMPLATE_NAME = 'users_hub/register.html'

	if request.method == "POST":
		email = request.POST["email"]

		# Ensure password matches confirmation
		password = request.POST["password"]
		confirmation = request.POST["confirmation"]
		if password != confirmation:
			return render(request, TEMPLATE_NAME, {
				"message": "Passwords must match."
			})

		# Attempt to create new user
		try:
			user = User.objects.create_user(email, email, password)
			user.save()
		except IntegrityError as e:
			print(e)
			return render(request, TEMPLATE_NAME, {
				"message": "Email address already taken."
			})
		login(request, user)
		return HttpResponseRedirect(reverse("index"))
	else:
		return render(request, TEMPLATE_NAME)
