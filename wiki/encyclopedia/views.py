from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
import markdown2
import re
from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    try:
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "entry": markdown2.markdown(util.get_entry(title))
        })
    except TypeError:
        return render(request, "encyclopedia/error.html", {
            "error": "No entry exists, feel free to write one of your own!"
        })


def search(request):
    entries = util.list_entries()
    form = request.POST
    query = form['q']
    if query in entries:
        return HttpResponseRedirect(reverse("entry", args=[query]))
    else:
        search_list = []
        for entry in entries:
            if re.search(fr".*{query}.*", entry):
                search_list.append(entry)
        print(search_list)
        return render(request, "encyclopedia/search.html", {
            "search_list": search_list,
            "query": query
        })
    
def new_entry(request):
    if request.method == "GET":
        message = "Write your entry here, be sure to use Markdown syntax for formatting headers, text style,\
        paragraph breaks, etc. Visit markdownguide.org/basic-syntax/ for a primer on Markdown syntax."
        return render(request, "encyclopedia/new_entry.html", {
            "message": message
        })
    if request.method == "POST":
        form = request.POST
        title = form['title']
        new_entry = form['new_entry']
        entries = util.list_entries()
        if title in entries:
            return render(request, "encyclopedia/error.html", {
                "error": "This page already exists, no need to overwrite it, just edit if you'd like!"
            })
        util.save_entry(title, new_entry)
        return HttpResponseRedirect(reverse("entry", args=[title]))