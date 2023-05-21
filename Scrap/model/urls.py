from django.urls import path
from .views import predict
app_name = 'model'

urlpatterns = [
    path('predict/',predict,name='predict')
]