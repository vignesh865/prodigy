from django.shortcuts import redirect
from django.views import View


class IndexView(View):
    def get(self, request):
        # return redirect(to="/static/html/integrate_sources.html")
        return redirect(to="/static/Postrequest1.htm")
