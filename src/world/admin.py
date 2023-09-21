from django.contrib import admin
from . models import Country, State, City, StateCity
from import_export import resources
from import_export.admin import ImportExportModelAdmin

# Register your models here.
class CountryResource(resources.ModelResource):
	class Meta:
		model = Country
		import_id_fields = ('id',)
		

class CountryAdmin(ImportExportModelAdmin):
	resource_class = CountryResource


class StateResource(resources.ModelResource):
	class Meta:
		model = State
		import_id_fields = ('id',)


class StateAdmin(ImportExportModelAdmin):
	resource_class = StateResource	


class CityResource(resources.ModelResource):
	class Meta:
		model = City

class CityAdmin(ImportExportModelAdmin):
	resource_class = CityResource		

admin.site.register(Country, CountryAdmin)	
admin.site.register(State, StateAdmin)	
admin.site.register(City, CityAdmin)	
