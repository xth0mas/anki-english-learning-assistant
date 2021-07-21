from django.urls import path

from . import views


urlpatterns = [
    path(
        'word/<int:identifier>', views.WordView.as_view(), name="word"
    )
]
