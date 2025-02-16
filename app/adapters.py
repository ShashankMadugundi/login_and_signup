from allauth.account.adapter import DefaultAccountAdapter
from django.contrib import messages

class CustomAccountAdapter(DefaultAccountAdapter):
    def user_logged_in(self, request, user):
        # Suppress the default "Successfully signed in" message
        pass
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter

class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        # Disable the message for successful Google login
        pass
