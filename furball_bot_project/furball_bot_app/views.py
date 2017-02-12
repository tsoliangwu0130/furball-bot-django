from django.shortcuts import render
from django.views import generic
from django.http.response import HttpResponse


# Create your views here.
class FurballBotView(generic.View):
	def get(self, request, *args, **kwargs):
		if self.request.GET['hub.verify_token'] == 'furball_bot_token':
			return HttpResponse(self.request.GET['hub.challenge'])
		else:
			return HttpResponse('Error, invalid token')
