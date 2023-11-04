from django.urls import path

from integration.controller.google_integration import GoogleIntegrationView
from integration.controller.index_view.index_view import IndexView
from integration.controller.index_view.knowledge_index_view import KnowledgeIndexView
from integration.controller.knowledge_cluster_view import KnowledgeClusterView
from integration.controller.load_external_folder import LoadExternalFolder
from integration.controller.source_integrate_view import SourceIntegrateView

"""
  IndexView is Only for testing purpose, should be removed after separate FrontEnd development
 """
urlpatterns = [
    path("", IndexView.as_view(), name="integration_index"),
    path("index-knowledge", KnowledgeIndexView.as_view(), name="knowledge_index"),


    path('integrate', SourceIntegrateView.as_view(), name="integrate"),
    path('google-drive', GoogleIntegrationView.as_view(), name="google-drive"),

    path('knowledge', KnowledgeClusterView.as_view(), name="knowledge-cluster"),
    path('load-folders', LoadExternalFolder.as_view(), name="load-folders"),
]
