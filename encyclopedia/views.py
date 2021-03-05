import random

from django import forms
from django.shortcuts import render

from markdown2 import Markdown

from . import util

md = Markdown()


class newEntry(forms.Form):
    #f_entry_etc is referenced in views ONLY
    f_entry_title = forms.CharField(label= "Title")
    f_entry_text = forms.CharField(widget=forms.Textarea(), label = "Content")

class editForm(forms.Form):
    #f_edit is referenced in views ONLY
    f_edit = forms.CharField(widget=forms.Textarea(), label="Edited")

#search form must be referenced in every view for it to appear in the side bar, as without a reference it does not exist within layout.html
class searchForm(forms.Form):
    #f_search is referenced in views ONLY
    f_search = forms.CharField(label="Search", required=False,
    widget= forms.TextInput
    (attrs={'placeholder': 'Search Encyclopedia'}))

def index(request):
    return render(request, "encyclopedia/index.html", {
        #'entries' is the variable referenced in index.html
        "entries": util.list_entries(),
        #'form' is the variable referenced in layout.html
        'searchForm': searchForm()
    })

def displayEntry(request, title):
    page = util.get_entry(title)
    if page is not None:
        page_converted = md.convert(page)

        context = {
            'title': title.capitalize,
            'content': page_converted,
            'searchForm': searchForm()            
        }

        return render(request, "encyclopedia/entry.html", context)
    else:
        return render(request, "encyclopedia/error.html")

def edit(request, title):
    #creates an editable form, when first clicked the method is always GET because the method of the form is GET
    if request.method == 'GET':
        #this creates the entry to edit as a variable to be passed to the edit Context
        entryToEdit = util.get_entry(title)

        context = {
            #context edit recieves the entry to edit and applies it to the form class editForm
            #edit and title are then passed to the edit.html
            'edit': editForm(initial={'f_edit': entryToEdit}),
            'title': title
        }

        return render(request, "encyclopedia/edit.html", context)
    else:
        #when the form is POSTED (submit clicked) it is tested and if success SAVED
        form = editForm(request.POST)
        if form.is_valid():
            editedText = form.cleaned_data["f_edit"]
            util.save_entry(title, editedText)
            return displayEntry(request, title)
        else:
            return error(request)

def new(request):
    if request.method == 'POST':
        form = newEntry(request.POST)
        if form.is_valid():
            title = form.cleaned_data["f_entry_title"]
            textarea = "#" + title + '\n' + form.cleaned_data["f_entry_text"]
            entry_list = util.list_entries()
            if title in entry_list:
                return error(request)
            else:
                util.save_entry(title, textarea)
                return displayEntry(request, title)
        else:
            return error(request)
    else:
        return render(request, "encyclopedia/new.html", {
            'searchForm': searchForm()
        })

def random_entry(request):
    entry_list = util.list_entries()
    rand_num = random.randint(0, len(entry_list) - 1)
    title = entry_list[rand_num]
    return displayEntry(request, title)

def error(request):
    return render(request, "encyclopedia/error.html",{
        'searchForm': searchForm()
    })

def search(request):
    if request.method == "GET":
        form = searchForm(request.GET)
        errorM = ''

        if form.is_valid():
            searchquery = form.cleaned_data["f_search"].lower()
            all_entries = util.list_entries()

            files=[filename for filename in all_entries if searchquery in filename.lower()]

            #no matches
            if len(files) == 0:
                errorM = (f'No results found for search \"{searchquery}\"')
                return render(request, "encyclopedia/search_results.html", {
                    'error':errorM,
                    'searchForm': searchForm()
                })
            #one match
            elif len(files) == 1 and files[0].lower() == searchquery:
                title = files[0]
                return displayEntry(request, title)
            #multiple matches
            else:
                title = [filename for filename in files if searchquery == filename.lower()]

                return render(request, "encyclopedia/search_results.html", {
                    'results': files,
                    'searchForm': searchForm()
                })