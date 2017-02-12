from django.shortcuts import render
from django.views import generic
from django.http.response import HttpResponse


# Create your views here.
class FurballBotView(generic.View):
	def get(self, request, *args, **kwargs):
		return HttpResponse("Furball: Meow!")
