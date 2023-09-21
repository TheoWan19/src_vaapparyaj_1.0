from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from . models import User, ClientUser, CustomerUser, Employee, CustomerProfile, EmployeeProfile
from . forms import UserCreationForm, UserChangeForm

# Register your models here.

class UserAdmin(BaseUserAdmin):
	form = UserChangeForm
	add_form = UserCreationForm

	list_display = ('email', 'name', 'phone', 'first_name', 'last_name', 'date_of_birth', 'gender', 'uid', 'country', 'state', 'city', 'address', 'is_active','is_staff', 'is_superuser', 'is_customer', 'is_employee')
	list_filter = ('is_superuser',)

	fieldsets = (
		(None, {'fields': ('email', 'is_staff', 'is_superuser', 'password')}),
		('Personal info', {'fields': ('name', 'phone', 'first_name', 'last_name', 'date_of_birth', 'gender', 'uid', 'country', 'state', 'city', 'address', 'is_customer','is_employee')}),
		('Groups', {'fields': ('groups',)}),
		('Permissions', {'fields': ('user_permissions',)}),
	)
	add_fieldsets = (
		(None, {'fields': ('email', 'is_staff', 'is_superuser', 'password1', 'password2')}),
		('Personal info', {'fields': ('name', 'phone', 'first_name', 'last_name', 'date_of_birth', 'gender', 'uid', 'country', 'state', 'city', 'address', 'is_customer', 'is_employee')}),
	)

	search_fields = ('email', 'name', 'phone')
	ordering = ('email',)
	filter_horizontal = ()

class AdminClientUser(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'first_name', 'last_name', 'gender', 'country', 'state', 'city', 'address', 'age', 'zip_code')


admin.site.register(User, UserAdmin)
admin.site.register(ClientUser, AdminClientUser)
admin.site.register(CustomerUser)
admin.site.register(Employee)
admin.site.register(CustomerProfile)
admin.site.register(EmployeeProfile)		
