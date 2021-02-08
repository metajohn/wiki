import random

from django import forms
from django.shortcuts import render

from markdown2 import Markdown

from . import util

md = Markdown()


class newEntry(forms.Form):
    f_entry_title = forms.CharField(label= "Title")
    f_entry_text = forms.CharField(widget=forms.Textarea(), label = "Content")

class editEntry(forms.Form):
    textarea = forms.CharField(widget=forms.Textarea(), label='Edited')

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    page = util.get_entry(title)
    if page is not None:
        page_converted = md.convert(page)

        context = {
            'title': title.capitalize,
            'content': page_converted,            
        }

        return render(request, "encyclopedia/entry.html", context)
    else:
        return render(request, "encyclopedia/error.html")

def error(request):
    return render(request, "encyclopedia/error.html")

def edit(request, title):
    if request.method == 'GET':
        entryEdit = util.get_entry(title)

        context = {
            'edit': editEntry(initial={'textarea': entryEdit}),
            'title': title
        }

        return render(request, "encyclopedia/edit.html", context)
    else:
        form = editEntry(request.POST)
        if form.is_valid():
            textarea = form.cleaned_data["textarea"]
            util.save_entry(title, textarea)
            return entry(request, title)

def new(request):
    if request.method == 'POST':
        form = newEntry(request.POST)
        if form.is_valid():
            title = form.cleaned_data["f_entry_title"]
            textarea = form.cleaned_data["f_entry_text"]
            entry_list = util.list_entries()
            if title in entry_list:
                return error(request)
            else:
                util.save_entry(title, textarea)
                return entry(request, title)
        else:
            return error(request)
    else:
        return render(request, "encyclopedia/new.html")

def random_entry(request):
    entry_list = util.list_entries()
    rand_num = random.randint(0, len(entry_list) - 1)
    title = entry_list[rand_num]
    return entry(request, title)


