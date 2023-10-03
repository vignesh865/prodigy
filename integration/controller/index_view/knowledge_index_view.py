from django.http import HttpResponse
from django.shortcuts import redirect
from django.views import View


class KnowledgeIndexView(View):
    def get(self, request):
        return redirect(to="/static/html/knowledge_clusters.html")
