from django.shortcuts import render
from django.views import View

class CommonIndexView(View):
    def get(self, request):
        return render(request, "contest/common/index.html")


class PanelIndexView(View):
    def get(self, request):
        return render(request, "contest/panel/index.html")
