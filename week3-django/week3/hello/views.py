from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, "hello/index.html")

def dave(request):
    return HttpResponse("I'm afraid I can't let you do that, Dave")

def greet(request, name):
    return render(request, "hello/greet.html", {
        "name": name.capitalize()
    })