from django.conf.urls import include, url
from .views import FurballBotView

urlpatterns = [
	url(r'^c97ea760afab571005f7996878f1ba7873417d8de500a86442/?$', FurballBotView.as_view()),
]
