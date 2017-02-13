from django.conf.urls import include, url
from .views import FurballBotView

urlpatterns = [
	url(r'^de359a0d3ecb5c944759d520a48bdb8b2e191b66a1dae4cc0c/?$', FurballBotView.as_view())
]
