from django.urls import include, path
from rest_framework import routers
from . import views

# Instantiate our API router
router = routers.DefaultRouter()

# eg.
# router.register(r'myviewfunction', views.TheViewFunction, basename='custom')

urlpatterns = [
    path('', include(router.urls)),
]
