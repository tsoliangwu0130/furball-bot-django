import json
import random
import re
import requests
from pprint import pprint
from pytz import timezone

from django.conf import settings
from django.http.response import HttpResponse
from django.utils.decorators import method_decorator
from django.views import generic
from django.views.decorators.csrf import csrf_exempt

FUNC_KEYWORD = '@furball'


def furball_behavior(recevied_message):
	# or function: choose one from a list of options
	clean_message = re.findall(r'^@furball(.*)', recevied_message)[0]
	recevied_message = random.choice(clean_message.split("or")).strip()
	return recevied_message


def post_facebook_message(fbid, recevied_message):
	user_details_url = settings.FB_GRAPH_API_URL + "/%s" % fbid
	user_details_params = {'fields': 'first_name,last_name,profile_pic', 'access_token': settings.PAGE_ACCESS_TOKEN}
	user_details = requests.get(user_details_url, user_details_params).json()

	if recevied_message.startswith(FUNC_KEYWORD):
		response_text = furball_behavior(recevied_message)
	else:
		response_text = 'Meow!'

	post_message_url = settings.FB_GRAPH_API_URL + '/me/messages?access_token=%s' % settings.PAGE_ACCESS_TOKEN
	response_msg = json.dumps({'recipient': {'id': fbid}, 'message': {'text': response_text}})
	status = requests.post(post_message_url, headers={'Content-Type': 'application/json'}, data=response_msg)
	pprint(status.json())


class FurballBotView(generic.View):
	def get(self, request, *args, **kwargs):
		if self.request.GET.get('hub.verify_token') == settings.VERIFY_TOKEN:
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
