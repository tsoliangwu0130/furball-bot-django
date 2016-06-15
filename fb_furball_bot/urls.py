from django.conf.urls import include, url
from .views import YoMamaBotView

urlpatterns = [
	url(r'^3831107ab7fb3bfa2d853b5fb21f66b215e145d9d3436c5aa2/?$', YoMamaBotView.as_view())
]
