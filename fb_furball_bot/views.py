from django.views import generic
from django.http.response import HttpResponse


VERIFY_TOKEN = "furball_bot_token"
PAGE_ACCESS_TOKEN = ""


class FurballBotView(generic.View):
	def get(self, request, *args, **kwargs):
		if self.request.GET['hub.verify_token'] == VERIFY_TOKEN:
			return HttpResponse(self.request.GET['hub.challenge'])
		else:
			return HttpResponse('Error, invalid token')
