from django import forms
from django.db import transaction
from django.contrib.auth.models import Group
from django.contrib.auth.forms import ReadOnlyPasswordHashField, AuthenticationForm
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget


from .models import User, CustomerUser, Employee

class RegistrationForm(forms.ModelForm):
	password = forms.CharField(label='Password', widget=forms.PasswordInput)
	
	class Meta:
		model = User
		fields = ('email', 'name', 'phone', 'first_name', 'last_name', 'date_of_birth', 'gender', 'uid', 'country', 'state', 'city', 'address', 'password')
		widgets = {
			'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
			'phone': PhoneNumberPrefixWidget(initial='US'),
		}

	def save(self, commit=True):
		user = super().save(commit=False)
		user.set_password(self.cleaned_data['password'])
		if commit:
			user.save()
		return user
		
class UserCreationForm(forms.ModelForm):
	password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
	password2 = forms.CharField(label='Password Confirmation', widget=forms.PasswordInput)

	class Meta:
		model = User
		fields = ('email', 'name', 'phone', 'first_name', 'last_name', 'date_of_birth', 'gender', 'uid', 'country', 'state', 'city', 'address', 'is_active','is_staff', 'is_superuser')

		def clean_password2(self):
			password1 = self.cleaned_data.get('password1')
			password2 = self.cleaned_data.get('password2')	
			if password1 and password2 and password1 != password2:
				raise forms.ValidationError("Password don't match")
			return password2
			
		def save(self, commit=True):
			user = super().save(commit=False)
			user.set_password(self.cleaned_data['password1'])
			if commit:
				user.save()
			return user
			
class UserChangeForm(forms.ModelForm):
	password = ReadOnlyPasswordHashField()

	class Meta:
		model = User
		fields = ('email', 'name', 'phone', 'first_name', 'last_name', 'date_of_birth', 'gender', 'uid', 'country', 'state', 'city', 'address', 'password', 'is_active', 'is_staff', 'is_superuser')	

	def clean_password(self):
		return self.initial['password']	


class CustomerSignUpForm(UserCreationForm):

	MALE = 'MALE'
	FEMALE = 'FEMALE'

	GENDER_CHOICES = (
		(MALE, 'Male'),
		(FEMALE, 'Female'),
	)

	email = forms.EmailField(widget=forms.EmailInput())
	name = forms.CharField(widget=forms.TextInput())
	phone = PhoneNumberField()
	password1 = forms.CharField(label='Password', widget=forms.PasswordInput())
	password2 = forms.CharField(label='Password Confirm', widget=forms.PasswordInput())

	first_name = forms.CharField(widget=forms.TextInput())
	last_name = forms.CharField(widget=forms.TextInput())
	date_of_birth = forms.DateField()
	gender = forms.ChoiceField(label='Gender', choices=GENDER_CHOICES)
	country = forms.CharField(widget=forms.TextInput())
	state = forms.CharField(widget=forms.TextInput())
	city = forms.CharField(widget=forms.TextInput())
		

	class Meta:
		model = User
		fields = ('email', 'name', 'phone', 'date_of_birth', 'first_name', 'last_name', 'gender', 'uid', 'country', 'state', 'city', 'address', 'password1', 'password2')
		widgets = {
			'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
			'phone': PhoneNumberPrefixWidget(initial='US'),
		}

	@transaction.atomic
	def save(self, commit=True):
		user = super().save(commit=False)
		user.is_customer = True
		if commit:
			user.save()
		customer = CustomerUser.objects.create(user=user, name=self.cleaned_data.get('name'), phone=self.cleaned_data.get('phone'), first_name=self.cleaned_data.get('first_name'), last_name=self.cleaned_data.get('last_name'), date_of_birth=self.cleaned_data.get('date_of_birth'), gender=self.cleaned_data.get('gender'), uid=self.cleaned_data.get('uid'), country=self.cleaned_data.get('country'), state=self.cleaned_data.get('state'), city=self.cleaned_data.get('city'), address=self.cleaned_data.get('address'))
		return user



