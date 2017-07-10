from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from . import models
# Register your models here.
class CityAdmin(admin.ModelAdmin):
	list_display=("city_id","name","country","zip_code","wid_city","date_created",)
class UserAdmin(admin.ModelAdmin):
	list_display=("username","name","email","city","log","lat","created_on","is_active","is_admin",)
admin.site.unregister(Group)
admin.site.register(models.City,CityAdmin)
admin.site.register(models.CustomUser,UserAdmin)
admin.site.register(models.WeatherRecord)

