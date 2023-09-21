from django.db import models

# Create your models here.
class Country(models.Model):
	id = models.IntegerField(primary_key=True)
	sortname = models.CharField(max_length=250)
	name = models.CharField(max_length=250)
	phoneCode = models.IntegerField()

	def __str__(self):
		return self.name

	class Meta:
		verbose_name_plural= 'Countries'		


class State(models.Model):
	id = models.IntegerField(primary_key=True)
	name = models.CharField(max_length=250)
	country_id = models.ForeignKey(Country, on_delete=models.CASCADE)

	def __str__(self):
		return self.name

class City(models.Model):
	name = models.CharField(max_length=250)
	lat = models.CharField(max_length=250, verbose_name='Latitude')
	lng = models.CharField(max_length=250, verbose_name='Longitude')
	

	def __str__(self):
		return self.name

	class Meta:
		verbose_name_plural= 'Cities'			

class StateCity(models.Model):
	state_id = models.ForeignKey(State, on_delete=models.SET_NULL, null=True)
	city_id = models.ForeignKey(City, on_delete=models.SET_NULL, null=True)	

	def __str__(self):
		return f'{self.state_id}-{self.city_id}'

	class Meta:
		verbose_name_plural= 'State Code'		






