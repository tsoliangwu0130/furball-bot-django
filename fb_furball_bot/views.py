from django.views import generic
from django.http.response import HttpResponse


class FurballBotView(generic.View):
	def get(self, request, *args, **kwargs):
		return HttpResponse("Hello World!")
