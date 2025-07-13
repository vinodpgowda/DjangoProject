from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .forms import SignUpForm, LogInForm
from .models import UserDetails
from .serializers import UserDetailsSerializer
import json
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
def index(request):
    return HttpResponse("<h1>Hello World! You are in Login Page.</h1>")

def signup(request):

    if request.method == "POST":
        signupform = SignUpForm(request.POST)

        if signupform.is_valid():
            signupform.save()
            return redirect("home")

    else:
        signupform = SignUpForm()

    return render(request, "Loginify/signup.html", {"signupform": signupform})

def login(request):

    if request.method == "POST":
        loginform = LogInForm(request.POST)

        if loginform.is_valid():
            user = UserDetails.objects.get(email=loginform.cleaned_data["email"])
            if user.password == loginform.cleaned_data["password"]:
                request.session["username"] = user.username
                request.session.set_expiry(10)
                return redirect("home")
            else:
                return render(request, "Loginify/login.html", {"loginform": loginform, "flag": False})
    else:
        loginform = LogInForm()

    return render(request, "Loginify/login.html", {"loginform": loginform, "flag": True})

def home(request):
    if request.session.get("username"):
        return render(request, "Loginify/home.html")
    else:
        return redirect("login")

def get_all_users(request):

    if request.method == "GET":

        email = request.GET.get('email')

        if email != None:
            user = UserDetails.objects.get(email=email)
            serialized_user = UserDetailsSerializer(user)
            return JsonResponse(
                serialized_user.data,
                safe=False
            )
        else:
            users = UserDetails.objects.all()
            serialized_users = UserDetailsSerializer(users, many=True)
            return JsonResponse(
                serialized_users.data,
                safe = False
            )

@csrf_exempt      
def get_user_by_id(request, username):
    
    try:
        user = UserDetails.objects.get(username=username)
    except Exception as err:
        return JsonResponse({
            "success": False,
            "message": f"no user by the username: {username}"
        }, status=404)

    if request.method == "PATCH":
        input_data = json.loads(request.body)

        updated_user = UserDetailsSerializer(user, data=input_data, partial=True)

        if updated_user.is_valid():
            updated_user.save()

            return JsonResponse({
                "message": "user updated successfully"
            })
        
    if request.method == "DELETE":

        user.delete()

        return JsonResponse({
            "message" : "User deleted succesfully"
        })