from django.conf.urls import url, include
from .views import FurBallBotView

urlpatterns = [
	# webhook: print binascii.hexlify(os.urandom(25))
	url(r'^4071858ca401f905fb75de5417e28e68857a4fc90cdbc49291/?$', FurBallBotView.as_view()),
]
