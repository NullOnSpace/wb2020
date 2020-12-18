from django.urls import path
from django.views.decorators.cache import cache_page

from . import views


urlpatterns = [
    path('', cache_page(360)(views.FeedList.as_view()), name="timeline"),
]
