from django.http import HttpResponse
from django.shortcuts import redirect
from django.views import View


class IndexView(View):
    def get(self, request):
        return redirect(to="/static/html/integrate_sources.html")
