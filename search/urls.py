from django.urls import path
from .views import upload_data, keyword_suggestion

urlpatterns = [
    path('upload/', upload_data, name='upload_data'),
    path('search/', keyword_suggestion, name='keyword_suggestion'),
]
