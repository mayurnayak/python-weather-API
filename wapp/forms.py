from django import forms
from .models import City, CustomUser
class CityForm(forms.ModelForm):
	class Meta:
		fields=('country','name',)
		model=City
class LoginForm(forms.Form):
	username=forms.CharField(label="Username")
	password = forms.CharField(widget=forms.PasswordInput)
class LocationForm(forms.Form):
	log=forms.DecimalField(label="Longitude", required=True)
	lat=forms.DecimalField(label="Latitude", required=True)
	def get_log(self):
		return self.log
	def get_lat(self):
		return self.lat

class RegisterForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput,required=True)
	confirm_password = forms.CharField(label="Confirm Password",required=True,widget=forms.PasswordInput)
	class Meta:
		fields=('name','email','username','password',)
		model=CustomUser
