import json
import requests
import random
import re
from pprint import pprint

from django.views import generic
from django.http.response import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

PAGE_ACCESS_TOKEN = 'EAAFe4BILMB0BAO2Sua74SdRFWF6Uno5FmlIDthU3hHpZA7eJOYOf2FfjbZBOXJSOe6YpbNaj1LNHGfk59aOmUioe2DD4NZC1oKgCxVycZA8cufB1ge53PiGeq4jB6uD6eSWLLPXMqWRPPaPKy8P4OF7nVGiBamhZANkVR4KwpTgZDZD'
VERIFY_TOKEN = 'furball_bot_token'


def post_facebook_message(fbid, recevied_message):
	post_message_url = 'https://graph.facebook.com/v2.8/me/messages?access_token=%s' % PAGE_ACCESS_TOKEN
	response_msg = json.dumps({"recipient": {"id": fbid}, "message": {"text": recevied_message}})
	status = requests.post(post_message_url, headers={"Content-Type": "application/json"}, data=response_msg)
	pprint(status.json())


class FurballBotView(generic.View):
	# The get method is the same as before.. omitted here for brevity
	@method_decorator(csrf_exempt)
	def dispatch(self, request, *args, **kwargs):
		return generic.View.dispatch(self, request, *args, **kwargs)

	def get(self, request, *args, **kwargs):
		if self.request.GET['hub.verify_token'] == VERIFY_TOKEN:
			return HttpResponse(self.request.GET['hub.challenge'])
		else:
			return HttpResponse('Error, invalid token')

	# Post function to handle Facebook messages
	def post(self, request, *args, **kwargs):
		# Converts the text payload into a python dictionary
		incoming_message = json.loads(self.request.body.decode('utf-8'))
		# Facebook recommends going through every entry since they might send
		# multiple messages in a single call during high load
		for entry in incoming_message['entry']:
			for message in entry['messaging']:
				# Check to make sure the received call is a message call
				# This might be delivery, optin, postback for other events
				if 'message' in message:
					# Print the message to the terminal
					pprint(message)
					# Assuming the sender only sends text. Non-text messages like stickers, audio, pictures
					# are sent as attachments and must be handled accordingly.
					post_facebook_message(message['sender']['id'], message['message']['text'])
		return HttpResponse()
