from django.shortcuts import render, redirect
from django.views import View

from contest.forms.standard_forms import AuthorForm
from contest.models import Author


class CommonIndexView(View):
    def get(self, request):
        return render(request, "contest/common/index.html")


class PanelIndexView(View):
    def get(self, request):
        return render(request, "contest/panel/index.html")


# 13:15 slac
class AuthorIndexView(View):
    def get(self, request):
        return render(
            request,
            "contest/panel/author/index.html",
            {"authors": Author.objects.all().order_by("band_name")}
        )


class AuthorCreateView(View):
    def get(self, request):
        form = AuthorForm()
        return render(
            request,
            "contest/panel/author/create.html",
            {"form": form}
        )

    def post(self, request):
        form = AuthorForm(request.POST)
        if not form.is_valid():
            return render(
                request,
                "contest/panel/author/create.html",
                {"form": form}
            )
        Author.objects.create(
            first_name=form.cleaned_data['first_name'],
            last_name=form.cleaned_data['last_name'],
            band_name=form.cleaned_data['band_name'],
            birth_date=form.cleaned_data['birth_date'],
            debut=form.cleaned_data['debut'],
        )
        return redirect('panel:authors:index')


# 14:58 dorobić walidację patrz zdjęcie
class AuthorUpdateView(View):
    def get(self, request, id):
        author = Author.objects.get(id=id)
        form = AuthorForm({
            "fist_name": author.first_name,
            "last_name": author.last_name,
            "birth_date": author.birth_date,
            "band_name": author.band_name,
            "debut": author.debut
        })
        return render(request, 'contest/panel/author/edit.html', {
            "form": form,
            "author": author
        })

    def post(self, request, id):
        author = Author.objects.get(id=id)
        form = AuthorForm(request.POST)
        if form.is_valid():
            author.first_name = form.cleaned_data['first_name']
            author.last_name = form.cleaned_data['last_name']
            author.birth_date = form.cleaned_data['birth_date']
            author.band_name = form.cleaned_data['band_name']
            author.debut = form.cleaned_data['debut']
            author.save()
            return redirect('panel:authors:index')


class AuthorDeleteView(View):
    def get(self, request, id):
        author = Author.objects.get(id=id)
        if author:
            author.delete()
            return redirect('panel:authors:index')
        return redirect('panel:authors:index')
