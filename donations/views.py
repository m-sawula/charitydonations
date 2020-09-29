from django.views import View
from django.shortcuts import render, redirect


# LandingPage
class LandingPage(View):
    def get(self, request):
        return render(request, "index.html")

    def post(self, request):
        pass


# AddDonation
class AddDonation(View):
    def get(self, request):
        return render(request, "user/form.html")

    def post(self, request):
        pass


# Login
class Login(View):
    def get(self, request):
        return render(request, "auth/login.html")

    def post(self, request):
        pass

# Register
class Register(View):
    def get(self, request):
        return render(request, "auth/register.html")

    def post(self, request):
        pass