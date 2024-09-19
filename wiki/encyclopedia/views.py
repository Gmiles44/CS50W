from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
import re, markdown2, random
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
                "error": "This page already exists, use the edit page if you'd like to change the content!"
            })
        util.save_entry(title, new_entry)
        return HttpResponseRedirect(reverse("entry", args=[title]))
    
def edit_entry(request, title):
    if request.method == "GET":
        return render(request, "encyclopedia/edit_entry.html", {
            "title": title,
            "entry": util.get_entry(title)
        })
    if request.method == "POST":
        form = request.POST
        name = form['title']
        edits = form['entry']
        entries = util.list_entries()
        if name not in entries:
            return render(request, "encyclopedia/error.html", {
                "error": "Entry does not exist, go to \"Create New Page\" if you'd like to create one!"
            })
        
        util.save_entry(name, edits)
        return HttpResponseRedirect(reverse("entry", args=[name]))
    
def random_page(request):
    calc = random.Random()
    entries = util.list_entries()
    random_entry = entries[calc.randrange(0, len(entries), 1)]
    return HttpResponseRedirect(reverse("entry", args=[random_entry]))
        
