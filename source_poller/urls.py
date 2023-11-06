from django.urls import path

from source_poller.controller.trigger_ingestion_view import TriggerIngestionView

"""
  IndexView is Only for testing purpose, should be removed after separate FrontEnd development
 """
urlpatterns = [

    path('ingest', TriggerIngestionView.as_view(), name="triggerIngestion"),

]
