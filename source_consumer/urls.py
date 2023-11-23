from django.urls import path

from source_consumer.controller.source_ingest_view import SourceIngestView

"""
  IndexView is Only for testing purpose, should be removed after separate FrontEnd development
 """
urlpatterns = [
    path('source-ingest', SourceIngestView.as_view(), name="sourceIngest"),
]
