import json
import random
import re
import requests
from pprint import pprint

from django.views import generic
from django.http.response import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


VERIFY_TOKEN = "furball_bot_token"
PAGE_ACCESS_TOKEN = "EAAFe4BILMB0BAG9IHy5FZBpdywkLzrqK1UmPXTFQSYMdgYkuZABC0hEulEvsswxqHFhpcrDC4cJWqwEeS3O5noQ3ps4alyFiVwHfeKsH4eNF9nM670YU03zvuOCZAZAUY8U04nB28eQ5YpaXn1LAKY7UXOeS5mAIAYRjXAgZBLwZDZD"


def post_facebook_message(fbid, recevied_message):
	post_message_url = 'https://graph.facebook.com/v2.8/me/messages?access_token=%s' % PAGE_ACCESS_TOKEN
	response_msg = json.dumps({"recipient": {"id": fbid}, "message": {"text": recevied_message}})
	status = requests.post(post_message_url, headers={"Content-Type": "application/json"}, data=response_msg)
	pprint(status.json())


class FurballBotView(generic.View):
	def get(self, request, *args, **kwargs):
		if self.request.GET['hub.verify_token'] == VERIFY_TOKEN:
			return HttpResponse(self.request.GET['hub.challenge'])
		else:
			return HttpResponse('Error, invalid token')

	@method_decorator(csrf_exempt)
	def dispatch(self, request, *args, **kwargs):
		return generic.View.dispatch(self, request, *args, **kwargs)

	def post(self, request, *args, **kwargs):
		incoming_message = json.loads(self.request.body.decode('utf-8'))
		for entry in incoming_message['entry']:
			for message in entry['messaging']:
				if 'message' in message:
					pprint(message)
					post_facebook_message(message['sender']['id'], message['message']['text'])
		return HttpResponse()
