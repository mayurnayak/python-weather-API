from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

import requests
from .forms import LoginForm, CityForm, LocationForm,RegisterForm
from .models import City, CustomUser
APPID="02e26d17d5eb412d1f9d10b5940fc588"
CITY_NAME="http://api.openweathermap.org/data/2.5/weather?q={query}&APPID={appid}"
CITY_ID="http://api.openweathermap.org/data/2.5/weather?id={cid}&&APPID={appid}"
GEO_LOC="http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={log}&APPID={appid}"
ZIP_CODE="http://api.openweathermap.org/data/2.5/weather?zip={zip_cod},{country_code}&APPID={appid}"
# Create your views here.
@login_required
def home(request):
	context={'cities':City.objects.filter(user=request.user)}
	return render(request,"welcome.html",context)
@login_required
def city_list(request):
	try:
		cities=City.objects.filter(user=request.user)
		return render(request,"cities.html",{
			"cities":cities
			});
	except Exception as e:
		context={
			"cities":[],
			"error":"Could not find users: {}".format(repr(e))
		}
		return render(request,"cities.html",context)
@login_required
def make_current(request,city_id):
	try:
		City.objects.filter(user=request.user).update(current=False)
		city=City.objects.get(city_id=city_id,user=request.user)
		if city is not None:
			city.current=True
			city.save()
	except Exception as e:
		print("Error :%s"%repr(e))
	return redirect("city_list")
@login_required
def delete_city(request,city_id):
	try:
		city=City.objects.get(city_id=city_id,user=request.user)
		if city is not None:
			city.delete()
	except:
		pass
	return redirect("city_list")

class CityView(View):
	form_class=CityForm
	def get(self,request):
		context=context={'cities':City.objects.all(),
		"page":"City","form":self.form_class}
		return render(request,"add_city.html",context);
	def post(self,request):
		form=self.form_class(request.POST)
		try:
			if form.is_valid():
				city=form.save(commit=False)
				city.user=request.user
				city.save()
				return redirect("/");
			else:
				context=context={
				'cities':City.objects.all(),
				"page":"City",
				"form":self.form_class
				}
				return render(request,"add_city.html",context);
		except Exception as e:
			context={
				"form":form,
				"error":"Could not create city: {}".format(repr(e))
			}
			return render(request,"add_city.html",context); 
class LocationView(View):
	form_class=LocationForm
	def get(self,request):
		return render(request,"location.html",{"form":self.form_class})
	def post(self,request):
		form=self.form_class(request.POST)
		if form.is_valid():
			lat=form.cleaned_data['lat']
			log=form.cleaned_data['log']
			try:
				w=requests.get(GEO_LOC.format(log=log,lat=lat,appid=APPID)).json()
				context={
				"weather":w,
				"location":{
					"lat":lat,
					"log":log
				}
				}
				return render(request,"location.html",context)	
			except Exception as e:
				context={
				"weather":None,
				"location":{
					"lat":lat,
					"log":log
				},
				"error":"Could not complete request:{}".format(str(e)),
				"form":form
				}
				return render(request,"location.html",context)
		else:
			return render(request,"location.html",{"form":form})
class RegisterView(View):
	form_class=RegisterForm
	template_name="register.html"
	def get(self,request):
		if(request.user.is_authenticated()):
			return redirect("home")
		return render(request,self.template_name,
			{"form":self.form_class})
	def post(self,request):
		form=self.form_class(request.POST)
		if form.is_valid:
			try:
				u=form.save(commit=False)
				if u.password==form.cleaned_data['confirm_password']:
					user=CustomUser.objects.create_user(u.username,
						email=u.email,
						password=u.password)
					user.name=u.name
					user.save()
					return redirect("login")
				else:
					return render(request,self.template_name,{"form":form,"error":"Password Missmatch"})
			except ValueError as e:
				return render(request,self.template_name,{"form":form,"error":"Could not create account: {}".format(repr(e))})
		else:
			return render(request,self.template_name,{"form":form,"error":"Please correct errors and try again"});
class LoginView(View):
	form_class=LoginForm
	template_name="login.html"
	def get(self,request):
		if(request.user.is_authenticated()):
			return redirect("home")
		return render(request,self.template_name,{
			"form":self.form_class
			})
	def post(self,request):
		form=self.form_class(request.POST)
		if(form.is_valid()):
			user=authenticate(
				username=form.cleaned_data['username'],
				password=form.cleaned_data['password'])
			if(user is not None and user.is_active):
				login(request,user)
				return redirect("home")
			return render(request,self.template_name,{"form":form,"error":"Invalid username or password"})
		else:
			return render(request,self.template_name,{"form":form})
@login_required
def logout_user(request):
	logout(request)
	return redirect("home")
#Weather
@login_required
def weather_bycity(request,city,country=None):
	try:
		bcity=City.objects.get(city_id=city)
		if(country):
			req=CITY_NAME.format(query="{},{}".format(bcity.name,country),appid=APPID)
		else:
			req=CITY_NAME.format(query=bcity.name,appid=APPID)
		w=requests.get(req).json()
		message=""
		print(w)
		if(w['cod']==401):
			message="Unauthenticated request: "+w['message']
			w=None
		context={'weather':w,"city":bcity,"error":message}
		return render(request,"city_weather.html",context)
	except Exception as e:
		context={
			'weather':None,
			"city":None,
			"error":"Could not load city weather: {0}".format(str(e))
		}
		return render(request,"city_weather.html",context)
@login_required
def weather_byuser(request):
	try:
		city=City.objects.get(user=request.user,current=True)
		if(city is not None):
			w=requests.get(CITY_NAME.format(query=city.name,appid=APPID)).json()
			context={'weather':w,"city":city}
			return render(request,"weather_user.html",context)
		else:
			context={"weather":None,"city":None,
			"error":"You have not selected your location"
			}
			return reder(request,"weather_user.html",context)
	except Exception as e:
		print("Error: %s"%(repr(e)))
		context={
			'weather':None,
			"city":None,
			"error":"Could not load city weather"
		}
		return render(request,"weather_user.html",context)