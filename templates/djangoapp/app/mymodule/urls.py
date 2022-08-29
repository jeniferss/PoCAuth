from django.urls import path
from app.mymodule.views.views import MyView

urlpatterns = [
    path('hello/', MyView.as_view()),
]
