from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .forms import SignUpForm, LogInForm
from .models import UserDetails
from .serializers import UserDetailsSerializer
import json
from django.views.decorators.csrf import csrf_exempt


# Create your views here.
def index(request):
    return HttpResponse("<h1>Hello, World!</h1>")


def signup(request):

    if request.method == "POST":
        signupform = SignUpForm(request.POST)

        if signupform.is_valid():
            signupform.save()
            return redirect("login")

    else:
        signupform = SignUpForm()

    return render(request, "Loginify/signup.html", {"signupform": signupform})


def login(request):

    error_message = ""

    if request.method == "POST":
        loginform = LogInForm(request.POST)

        if loginform.is_valid():
            try:
                user = UserDetails.objects.get(email=loginform.cleaned_data["email"])

                if user.password == loginform.cleaned_data["password"]:
                    request.session["username"] = user.username
                    request.session.set_expiry(10)
                    return redirect("home")
                else:
                    error_message = "Incorrect Password!!!"

            except UserDetails.DoesNotExist:
                error_message = "Email does not exist!!!"
    else:
        loginform = LogInForm()

    return render(
        request,
        "Loginify/login.html",
        {"loginform": loginform, "error_message": error_message},
    )


def home(request):
    if request.session.get("username"):
        return render(request, "Loginify/home.html")
    else:
        return redirect("login")


def get_all_users(request):

    if request.method == "GET":

        users = UserDetails.objects.all()
        serialized_users = UserDetailsSerializer(users, many=True)
        return JsonResponse(
            {"success": True, "users": serialized_users.data}, status=200
        )


@csrf_exempt
def user_detail_by_id(request, username):

    try:
        user = UserDetails.objects.get(username=username)
    except Exception as err:
        return JsonResponse(
            {"success": False, "message": f"no user by the username: {username}"},
            status=404,
        )

    if request.method == "PATCH":
        input_data = json.loads(request.body)

        serialized_user = UserDetailsSerializer(user, data=input_data, partial=True)

        if serialized_user.is_valid():
            serialized_user.save()

            return JsonResponse(
                {
                    "message": "user details updated successfully",
                    "user": serialized_user.data,
                },
                status=200,
            )

    else:
        return JsonResponse(
            {"success": False, "message": f"{request.method} Method not allowed"},
            status=405,
        )


@csrf_exempt
def user_detail_by_email(request, email):

    try:
        user = UserDetails.objects.get(email=email)
        serialized_user = UserDetailsSerializer(user)
    except Exception as err:
        return JsonResponse(
            {"success": False, "message": f"No user found by the email: {email}"},
            status=404,
        )

    if request.method == "GET":
        return JsonResponse({"success": True, "user": serialized_user.data}, status=200)

    elif request.method == "DELETE":
        user.delete()

        return JsonResponse(
            {
                "success": True,
                "message": f"User by the email: {email} deleted successfully",
            },
            status=200,
        )

    else:
        return JsonResponse(
            {"success": False, "message": f"{request.method} Method not allowed"},
            status=405,
        )
