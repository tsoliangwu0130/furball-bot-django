from django.shortcuts import render
from django.views import generic
from django.http.response import HttpResponse


class FurBallBotView(generic.View):
	def get(self, request, *args, **kwargs):
		return HttpResponse("Furball: Meow!")
