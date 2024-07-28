from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render


def redirect_to_hello(request):
    url = reverse("p-hi")
    print(url)
    return HttpResponseRedirect(url)


def hello(request):
    q = request.GET.get("q")
    context = {"name": q}
    return render(request, "portfolio/home.html", context)



def about_me(request):
    context = "About: info"
    return HttpResponse(context)

def my_skill(request, id):
    context = f"skill: id={id}"
    return HttpResponse(context)