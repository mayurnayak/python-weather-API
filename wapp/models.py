from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
import uuid
class MyUserManager(BaseUserManager):
    def create_user(self, username,email,password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not username:
            raise ValueError('Users must have an email address')
        user = self.model( username=username, email=email,)
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self, username,email,password=None,**kwargs):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        #name=**kwargs.get("name")
        if not username:
            raise ValueError('Users must have an email address')
        user = self.model( username=username,email=email,)
        user.is_admin=True
        user.set_password(password)
        user.save(using=self._db)
        return user

class CustomUser(AbstractBaseUser):
	username=models.CharField(max_length=60,unique=True)
	name=models.CharField(max_length=256,blank=True,null=True)
	email=models.EmailField(max_length=256,blank=False,null=True)
	log=models.DecimalField(max_digits=8,decimal_places=2,blank=True,null=True)
	lat=models.DecimalField(max_digits=8,decimal_places=2,blank=True,null=True)
	created_on=models.DateTimeField(auto_now_add=True)
	is_active = models.BooleanField(default=True)
	is_admin = models.BooleanField(default=False)

	objects=MyUserManager()
	USERNAME_FIELD='username'
	REQUIRED_FIELDS = ['email',]
	def get_full_name(self):
		return self.name
	def get_short_name(self):
		return self.username
	def __str__(self):
		return self.username
	def has_perm(self, perm, obj=None):
		return True
	def has_module_perms(self, app_label):
		return True
	@property
	def is_adm(self):
		return self.is_admin
	@property
	def is_staff(self):
		return self.is_adm
	@property
	def is_superuser(self):
		return True

class City(models.Model):
	city_id=models.AutoField(primary_key=True)
	wid_city=models.IntegerField(blank=True,null=True) #CityID
	zip_code=models.CharField(max_length=8,blank=True,null=True)
	country=models.CharField(max_length=100)
	name=models.CharField(max_length=150)
	date_created=models.DateTimeField(auto_now_add=True)
	user=models.ForeignKey(CustomUser)
	current=models.BooleanField(default=False)

class WeatherRecord(models.Model):
	record_id=models.AutoField(primary_key=True)
	location=models.ForeignKey(City)
	longitude=models.DecimalField(max_digits=8,decimal_places=4)
	latitude=models.DecimalField(max_digits=8,decimal_places=4)
	sunrise=models.TimeField()
	sunset=models.TimeField()
	humidity=models.DecimalField(max_digits=8,decimal_places=2)
	pressure=models.DecimalField(max_digits=8,decimal_places=4)
	cloudiness=models.CharField(max_length=250)
	rain=models.DecimalField(max_digits=8,decimal_places=2)
	wind_speed=models.DecimalField(max_digits=8,decimal_places=4)
	wind_deg=models.DecimalField(max_digits=8,decimal_places=4)
	temp_min=models.DecimalField(max_digits=8,decimal_places=4)
	temp_max=models.DecimalField(max_digits=8,decimal_places=4)
	create_on=models.DateTimeField(auto_now_add=True)
