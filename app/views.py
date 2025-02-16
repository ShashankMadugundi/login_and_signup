from django.shortcuts import render, redirect,HttpResponse
from django.contrib import messages
from .forms import UserRegistrationForm
from django.contrib.auth import authenticate, login
from .forms import UserLoginForm
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login,logout
from django.core.cache import cache
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegistrationForm
from django.contrib.auth.backends import ModelBackend

from django.contrib.messages import get_messages
import random
import requests
from django.conf import settings

from django.http import JsonResponse

def home_view(request):
    if request.user.is_authenticated:
        print(request.user.full_name)  # Print the logged-in user's full name
    else:
        print("No user is logged in")

    # if not request.user.is_authenticated:
    #     print(request, "You were logged out. Please log in again.")
    # print(f"User Authenticated: {request.user.is_authenticated}")
    # print(f"Session Key: {request.session.session_key}")  # Debugging
    # print(f"Session Data: {dict(request.session.items())}")
    return render(request, "home.html")



def profile(request):
    return render(request,"profile.html")
# def signup_view(request):
#     # print("SIGNUP")
#     if request.method == 'POST':
#         form = UserRegistrationForm(request.POST)
#         if form.is_valid():
#             user = form.save(commit=False)
#             user.set_password(form.cleaned_data['password'])
#             user.save()
#             messages.success(request, "Registration successful! Please log in.")
#             return redirect("login")
#         else:
#             messages.error(request, "Please correct the errors below.")
#     else:
#         form = UserRegistrationForm()
#     return render(request, 'signup.html', {'form': form})

CUSTOMER_ID = "581D0320-A4C0-41BA-893F-68AD39625930"
API_KEY = "dMbgiW3xtOGLe67rUhwxu6J0btEZPTfCFDnzPq5DxSZlrE9HdMs0HG5lWHWAqveZs8uj2dB14/e89+N27O+Dsg=="
TELESIGN_CUSTOMER_ID = "581D0320-A4C0-41BA-893F-68AD39625930"
TELESIGN_API_KEY = "dMbgiW3xtOGLe67rUhwxu6J0btEZPTfCFDnzPq5DxSZlrE9HdMs0HG5lWHWAqveZs8uj2dB14"

# OTP Generation Function

# from .models import User
# Function to send OTP via Telesign
import time
def send_otp(phone):
    # print("Inside",phone)
    otp = random.randint(100000, 999999)  # Generate a 6-digit OTP
    message = f"Your OTP for password reset is {otp}. Do not share this with anyone."
    # Store OTP in cache (expires in 5 minutes)
    cache.set(f"otp_{phone}", otp, timeout=300)
    # stored_otp = cache.get(f"otp_{phone}")
    # print(f"OTP stored in cache for {phone}: {stored_otp}")
    url = f"https://rest-ww.telesign.com/v1/messaging"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {
        "phone_number": phone,
        "message": message,
        "message_type": "OTP"
    }
    # print("Inside)
    print(otp)
    response = requests.post(url, auth=(CUSTOMER_ID, API_KEY), headers=headers, data=data)
    # print(response)
    if response.status_code == 200:
        return True
    else:
        return False

def resend_otp_view(request):
    if request.method == "POST":
        phone = request.session.get("phone")  # Get phone number from session
        phone="+918333837975"
        if not phone:
            return JsonResponse({"message": "Session expired. Please try again."}, status=400)

        otp = random.randint(100000, 999999)  # Generate new OTP
        cache.set(f"otp_{phone}", otp, timeout=300)  # Store OTP in cache for 5 minutes

        # Send OTP via SMS
        if send_otp(phone):
            return JsonResponse({"message": "OTP has been resent successfully!"})
        else:
            return JsonResponse({"message": "Failed to resend OTP. Try again later."}, status=500)
    
    return JsonResponse({"message": "Invalid request"}, status=400)



def signup_view(request):
    storage = get_messages(request)
    storage.used=True
    for _ in storage:
        pass
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            phone = form.cleaned_data['mobile_number']
            User = get_user_model()
            # Check if the phone number already exists
            if User.objects.filter(mobile_number=phone).exists():
                # err="Mobile number already registered."
                messages.error(request, "Mobile number already registered.")
                print("Mobile already registered")
                return redirect("signup")

            # Store user details temporarily in session
            request.session["signup_data"] = {
                "full_name": form.cleaned_data["full_name"],
                "email": form.cleaned_data["email"],
                "mobile_number": phone,
                "password": form.cleaned_data["password"],
            }
            # print(request.session["signup_data"])
            # Send OTP
            print(phone)
            phone='+918333837975'
            if send_otp(phone):
                print("OTP Sent")
                messages.success(request, "OTP sent to your mobile number for verification.")
                return redirect(f"/verify-otp-signup/?signup=1")  # Indicate it's for signup verification
            else:
                print("Failed to send otp")
                messages.error(request, "Failed to send OTP. Try again.")

    else:
        form = UserRegistrationForm()
    
    return render(request, 'signup.html', {'form': form})



def verify_otp_view_signup(request):
    storage = get_messages(request)
    storage.used=True
    for _ in storage:
        pass
    # err=""
    if request.method == "POST":
        # print("Im In")
        # print(f"Cache keys: {list(cache._cache.keys())}" if hasattr(cache, '_cache') else "Cache backend does not support key listing")
        err=""
        # Retrieve phone number from session
        signup_data = request.session.get("signup_data")
        # print(request.POST.get('signup'))
        phone = signup_data.get("mobile_number") if signup_data else None
        otp_entered = request.POST.get("otp")
        phone="+918333837975"
        otp_stored = cache.get(f"otp_{phone}")  # Get OTP from cache
        print(otp_entered,otp_stored)
        print(f"Phone: {phone}, OTP Entered: {otp_entered}")

        if otp_stored and str(otp_stored) == otp_entered:
            print("OTP Verifird")
            cache.delete(f"otp_{phone}")  # Remove OTP after successful verification

            # If this is a signup verification
            if request.POST.get("signup"):  # <-- Change from GET to POST
                print("SIGNUP")
                if not signup_data:
                    # err="Signup session expired. Please sign up again."
                    # time.sleep(3)
                    messages.error(request, "Signup session expired. Please sign up again.")
                    return redirect("signup")

                # Save the user after OTP verification
                User = get_user_model()
                user = User.objects.create(
                    full_name=signup_data["full_name"],
                    email=signup_data["email"],
                    mobile_number=signup_data["mobile_number"]
                )
                print("Name:",signup_data["full_name"],"Email:",signup_data["email"],"Phone",signup_data["mobile_number"])
                user.set_password(signup_data["password"])
                user.save()

                # Clear session
                del request.session["signup_data"]

                messages.success(request, "Signup successful! You can now log in.")
                return redirect("login")

            messages.success(request, "OTP verified successfully!")
            return redirect("signup")

        else:
            # err="Invalid OTP. Try again."
            messages.error(request, "Invalid OTP. Try again.")

    return render(request, "verify_otp_signup.html")



def login_view(request):
    if request.user.is_authenticated:
        # print("Auth")
        return redirect('home')
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            email = email.strip()
            
            # print(f"Email: {email}, Password: {password}")
            # User = get_user_model()
            # user_check = User.objects.filter(email=email).first()
            # # user_check = User.objects.filter(email__iexact=email).first()

            # if user_check:
            #     print(f"User found: {user_check.email}")
            #     print(f"Password correct: {user_check.check_password(password)}")
            # else:
            #     print("User not found.")
            user = authenticate(request, email=email, password=password)
            print(user)
            if user is not None:
                login(request, user)
                request.session.save()
                request.session['user_id'] = user.id
                return redirect('home')
                # messages.success(request, "Login successful!")
                # print(f"Session Key: {request.session.session_key}")
                # print(f"Session Data: {request.session.items()}")
                # if user.is_authenticated:
                #     print("Authenticated")
                # return render(request,'home.html')
            else:
                login_error = "Invalid email or password."
        
        else:
            # form = UserLoginForm()
            login_error = "Please enter the correct details"
    else:
        form = UserLoginForm()
        login_error = ""
    return render(request, 'login.html',{'form': form, 'login_error': login_error})


def request_otp_login(request):
    # storage = get_messages(request)
    # storage.used=True
    # for _ in storage:
    #     pass
    if request.method == "POST":
        phone = request.POST.get("phone")
        User=get_user_model()
        try:
            user = User.objects.get(mobile_number=phone)
        except User.DoesNotExist:
            messages.error(request, "Mobile number not registered.")
            return redirect("login_with_otp")

        request.session["phone"] = phone  # Store phone in session for verification step
        if send_otp(phone):
            messages.success(request, "OTP sent to your mobile number.")
            return redirect("verify_otp_login")
        else:
            # err="Failed to send OTP. Try again."
            # time.sleep(3)
            messages.error(request, "Failed to send OTP. Try again.")
            return redirect("login_with_otp")

    return render(request, "login_with_otp.html")

def verify_otp_login(request):
    storage = get_messages(request)
    storage.used=True
    for _ in storage:
        pass
    if request.method == "POST":
        phone = request.session.get("phone")
        otp_entered = request.POST.get("otp")
        otp_stored = cache.get(f"otp_{phone}")
        User=get_user_model()
        print(phone,otp_entered,otp_stored)
        if otp_stored and str(otp_stored) == otp_entered:
            cache.delete(f"otp_{phone}")  # Remove OTP after successful verification

            try:
                user = User.objects.get(mobile_number=phone)
                backend = "django.contrib.auth.backends.ModelBackend"
                login(request, user,backend=backend)  # Log the user in
                messages.success(request, "Login successful!")
                return redirect("home")  # Change this to your dashboard/homepage
            except User.DoesNotExist:
                err="User not found"
                # time.sleep(3)
                messages.error(request, "User not found.")
                return redirect("login_with_otp")

        else:
            # err="Invalid OTP. Try again."
            messages.error(request, "Invalid OTP. Try again.")

    return render(request, "verify_otp_login.html")


def logout_view(request):
    logout(request)
    return redirect('home')


import requests
from django.shortcuts import render
from django.http import JsonResponse
import random
import os
# from django.core.cache import cache  # For storing OTP temporarily

def send_otp_view(request):
    storage = get_messages(request)
    storage.used=True
    for _ in storage:
        pass
    if request.method == "POST":
        phone = request.POST.get("phone")
        # print(phone)
        print("Phone:", phone)
        User = get_user_model()
        # users = User.objects.all()  # Get all users
        # for user in users:
        #     print(user.email)
        # Check if the phone number exists in the database
        try:
            
            user = User.objects.get(mobile_number=phone) 
            # print(user)
            user_id = user.id  # Get user ID
        except User.DoesNotExist:
            messages.error(request, "No account found with this mobile number.")
            return redirect("send_otp")

        if send_otp(phone):
            print("OTP Sent Successfully")
            request.session["phone"] = phone  # Store phone in session
            request.session["user_id"] = user_id
            return redirect(f"/verify-otp/?user_id={user_id}")  # Redirect with user_id in URL
        else:
            messages.error(request, "Failed to send OTP. Try again.")

    return render(request, "send_otp.html")


# http://127.0.0.1:8000/verify-otp/?user_id=9
def verify_otp_view(request):
    # print("Request GET Data:", request.GET)
    storage = get_messages(request)
    storage.used=True
    for _ in storage:
        pass
    if request.method == "POST":
        # err=""
        phone = request.session.get("phone")
        # user_id = request.GET.get("user_id")
        user_id = request.GET.get("user_id") or request.session.get("user_id")
        otp_entered = request.POST.get("otp")
        # print(user_id,phone,otp_entered)
        otp_stored = cache.get(f"otp_{phone}")  # Get OTP from cache

        if otp_stored and str(otp_stored) == otp_entered:
            messages.success(request, "OTP verified successfully!")
            cache.delete(f"otp_{phone}")  # Remove OTP after successful verification
            request.session["user_id"] = user_id
            return redirect(f"/reset-password/?user_id={user_id}")  # Redirect with user_id
        else:
            # err="Invalid OTP. Try again"
            messages.error(request, "Invalid OTP. Try again.")

    return render(request, "verify_otp.html")


from django.contrib.auth.hashers import make_password




def reset_password_view(request):
    storage = get_messages(request)
    storage.used=True
    for _ in storage:
        pass
    if request.method == "POST":
        user_id = request.GET.get("user_id") or request.session.get("user_id")  # Get user_id from URL
        print(user_id)
        new_password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")
        print(new_password)
        if not user_id:
            messages.error(request, "Invalid request. Please try again.")
            return redirect("send_otp")

        if new_password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect(f"/reset-password/?user_id={user_id}")

        if not is_valid_password(new_password):
            messages.error(
                request,
                "Password must be at least 8 characters long, contain at least one uppercase letter, one number, and one special character."
            )
            return redirect(f"/reset-password/?user_id={user_id}")

        try:
            User = get_user_model()
            # Fetch the user using user_id and update password
            user = User.objects.get(id=user_id)
            user.password = make_password(new_password)  # Hash and update password
            user.save()

            messages.success(request, "Password reset successful! You can now log in.")
            return redirect("login")
        except User.DoesNotExist:
            messages.error(request, "User not found. Please sign up first.")
            return redirect("signup")

    return render(request, "reset_password.html")












import re
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

# Function to validate password strength
def is_valid_password(password):
    if (
        len(password) >= 8 and
        re.search(r'[A-Z]', password) and  # At least one uppercase letter
        re.search(r'\d', password) and    # At least one digit
        re.search(r'[!@#$%^&*(),.?":{}|<>]', password)  # At least one special character
    ):
        return True
    return False


