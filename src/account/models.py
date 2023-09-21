from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from django.db.models.signals import post_save
#from django.dispatch import receiver
from phonenumber_field.modelfields import PhoneNumberField


import os
from world.models import Country, State, City 
from . managers import UserManager

# Create your models here.
class User(AbstractBaseUser, PermissionsMixin):
	user_type_data=((1,"HOD"),(2,"ClientUser"),(3,"CustomerUser"), (4,"Employee"))
	user_type=models.CharField(default=1,choices=user_type_data,max_length=10)

	MALE = 'MALE'
	FEMALE = 'FEMALE'

	GENDER_CHOICES = (
		(MALE, 'Male'),
		(FEMALE, 'Female'),
	)


	email = models.EmailField(unique=True)
	name = models.CharField(max_length=120)
	phone = PhoneNumberField(unique=True)
	first_name = models.CharField(max_length=120)
	last_name = models.CharField(max_length=120)
	date_of_birth = models.DateField(blank=True, null=True)
	gender = models.CharField(max_length=6, choices=GENDER_CHOICES, verbose_name='Gender')
	uid = models.CharField(max_length=10, unique=True, verbose_name='User Identifier', default='')
	is_staff = models.BooleanField(default=False)
	is_customer = models.BooleanField(default=True)
	is_employee = models.BooleanField(default=False)
	is_active = models.BooleanField(default=True)
	date_joined = models.DateTimeField(default=timezone.now)
	modified_at = models.DateTimeField(auto_now=True)
	last_login = models.DateTimeField(null=True)
	country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True)
	state = models.ForeignKey(State, on_delete=models.SET_NULL, null=True)
	city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True)
	address = models.CharField(max_length=500)



	objects = UserManager()

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['name', 'phone']


	def get_full_name(self):
		return f'{self.first_name }'+' '+ f'{self.last_name}'.title()

	def get_short_name(self):
		return self.name.split()[0]	

class AdminHOD(models.Model):
    admin=models.OneToOneField(User,on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    

class ClientUser(models.Model):

	MALE = 'MALE'
	FEMALE = 'FEMALE'

	GENDER_CHOICES = (
		(MALE, 'Male'),
		(FEMALE, 'Female'),
	)

	email = models.EmailField(unique=True)
	name = models.CharField(max_length=120)
	phone = PhoneNumberField(unique=True)
	first_name = models.CharField(max_length=120)
	last_name = models.CharField(max_length=120)
	gender = models.CharField(max_length=6, choices=GENDER_CHOICES, verbose_name='Gender')
	address = models.CharField(max_length=255)
	city = models.CharField(max_length=100)
	age = models.CharField(max_length=100)
	zip_code = models.CharField(max_length=100)
	created_at = models.DateTimeField(auto_now_add=True)
	modifed_at = models.DateTimeField(auto_now=True)
	country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True)
	state = models.ForeignKey(State, on_delete=models.SET_NULL, null=True)
	city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True)
	save_by = models.ForeignKey(User, on_delete=models.PROTECT)
	


	objects = UserManager()

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = []


	def get_full_name(self):
		return f'{self.first_name }'+' '+ f'{self.last_name}'.title()

	def get_short_name(self):
		return self.name.split()[0]



class CustomerUser(models.Model):
	STATUS = [
		('customer', 'customer'),
	]

	user = models.OneToOneField(User, on_delete=models.CASCADE)
	status = models.CharField(max_length=10, choices=STATUS, default='customer')

	def __str__(self):
		return self.get_full_name
 	

class Employee(models.Model):

	STATUS = [
		('employee', 'employee'),
	]

	user = models.OneToOneField(User, on_delete=models.CASCADE)
	status = models.CharField(max_length=10, choices=STATUS, default='employee')

	def __str__(self):
		return self.get_full_name	


class CustomerProfile(models.Model):

	def image_upload_to(self, instance=None):
		if instance:
			return os.path.join("Users", self.username, instance)
		return None	

	user = models.OneToOneField(CustomerUser, on_delete=models.CASCADE)
	follows = models.ManyToManyField('self', 
		related_name='followed_by', 
		symmetrical=False, blank=True)
	image = models.ImageField(default='default/user.jpg', upload_to=image_upload_to)
	description = models.TextField('Description', max_length=200, default='', blank=True)
	date_modified = models.DateTimeField(CustomerUser, auto_now=True)


	def __str__(self):
		return self.user.get_full_name


#Create Profile when new user Sign up
#@receiver(post_save, sender=CustomerUser)
def create_customerProfile(sender, instance, created, **kwargs):
	if created:
		user_customerProfile = CustomerUser(user=instance)
		user_customerProfile.save()

post_save.connect(create_customerProfile, sender=CustomerUser)	



class EmployeeProfile(models.Model):

	def image_upload_to(self, instance=None):
		if instance:
			return os.path.join("Users", self.username, instance)
		return None	

	user = models.OneToOneField(Employee, on_delete=models.CASCADE)
	follows = models.ManyToManyField('self', 
		related_name='followed_by', 
		symmetrical=False, blank=True)
	function = models.CharField('Designation', max_length=100)
	session_start_year=models.DateField()
	session_end_year=models.DateField()
	image = models.ImageField(default='default/user.jpg', upload_to=image_upload_to)
	description = models.TextField('Description', max_length=200, default='', blank=True)
	date_modified = models.DateTimeField(Employee, auto_now=True)


	def __str__(self):
		return self.user.get_full_name


#Create Profile when new user Sign up
#@receiver(post_save, sender=CustomerUser)
def create_employeeProfile(sender, instance, created, **kwargs):
	if created:
		user_employeeProfile = Employee(user=instance)
		user_employeeProfile.save()

post_save.connect(create_employeeProfile, sender=Employee)	


class Subjects(models.Model):
    subject_name=models.CharField(max_length=255)
    employee_id=models.ForeignKey(User,on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
    	return self.subject_name



class Attendance(models.Model):
    subject_id=models.ForeignKey(Subjects,on_delete=models.DO_NOTHING)
    attendance_date=models.DateTimeField(auto_now_add=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
    	return self.subject_id.subject_name



class AttendanceReport(models.Model):
    employee_id=models.ForeignKey(Employee,on_delete=models.DO_NOTHING)
    attendance_id=models.ForeignKey(Attendance,on_delete=models.CASCADE)
    status=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
    	return self.employee_id.user.name
    

class LeaveReportEmployee(models.Model):
    employee_id=models.ForeignKey(Employee,on_delete=models.CASCADE)
    leave_date=models.CharField(max_length=255)
    leave_message=models.TextField()
    leave_status=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
    	return self.employee_id.user.name


class FeedBackEmployee(models.Model):
    employee_id = models.ForeignKey(Employee, on_delete=models.CASCADE)
    feedback = models.TextField()
    feedback_reply = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
    	return self.employee_id.user.name


class NotificationEmployee(models.Model):
    employee_id = models.ForeignKey(Employee, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
    	return self.employee_id.user.name		


