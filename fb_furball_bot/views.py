import json
import requests
import random
import re
from pprint import pprint
from django.views import generic
from django.http.response import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

PAGE_ACCESS_TOKEN = ""
VERIFY_TOKEN = ""


def post_facebook_message(fbid, recevied_message):
	post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=%s' % PAGE_ACCESS_TOKEN
	user_details_url = "https://graph.facebook.com/v2.6/%s" % fbid
	user_details_params = {'fields': 'first_name,last_name,profile_pic', 'access_token': PAGE_ACCESS_TOKEN}
	user_details = requests.get(user_details_url, user_details_params).json()
	response_text = 'Meow~\nHello ' + user_details['first_name'] + '!\necho: ' + recevied_message
	response_msg = json.dumps({"recipient": {"id": fbid}, "message": {"text": response_text}})
	status = requests.post(post_message_url, headers={"Content-Type": "application/json"}, data=response_msg)
	pprint(status.json())


class YoMamaBotView(generic.View):
	@method_decorator(csrf_exempt)
	def dispatch(self, request, *args, **kwargs):
		return generic.View.dispatch(self, request, *args, **kwargs)

	def get(self, request, *args, **kwargs):
		if self.request.GET['hub.verify_token'] == VERIFY_TOKEN:
			return HttpResponse(self.request.GET['hub.challenge'])
		else:
			return HttpResponse('Error, invalid token')

	def post(self, request, *args, **kwargs):
		incoming_message = json.loads(self.request.body.decode('utf-8'))
		for entry in incoming_message['entry']:
			for message in entry['messaging']:
				if 'message' in message:
					pprint(message)
					post_facebook_message(message['sender']['id'], message['message']['text'])
		return HttpResponse()
