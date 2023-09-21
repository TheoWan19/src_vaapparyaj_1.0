from django.shortcuts import render

# Create your views here.
def index(request):
	template_name = 'core/home.html'
	context = {}
	return render(
		request=request, 
		template_name=template_name, 
		context=context
	)
