from django.urls import path

from query_system.controller.chat_controller import ChatController

"""
  IndexView is Only for testing purpose, should be removed after separate FrontEnd development
 """
urlpatterns = [
    path('chat', ChatController.as_view(), name="chat"),
]
