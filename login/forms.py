from django.contrib.auth.models import User
from django import forms
from login.models import Utilisateur

class LoginForm(forms.Form):
	username = forms.CharField(max_length=75)
	password = forms.CharField(max_length=75)

class UserForm(forms.ModelForm):
	class Meta:
		model = User
		exclude = ("groups", "user_permissions", "is_active", "is_superuser", "last_login", "date_joined", "is_staff")
"""
class UtilisateurForm(forms.ModelForm):
	class Meta:
		model = Utilisateur
		exclude = ("profilBase",)
"""