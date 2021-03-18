from django.shortcuts import render
from markdown2 import Markdown
from . import util
from django import forms
from django.urls import reverse
from django.http import HttpResponseRedirect
from random import *


class NewPageForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Add a title','class': 'new-page-title'}))
    content = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Add new content here', 'class': 'new-page-textarea'}))


def index(request):
    return render(request, 'encyclopedia/index.html', {
        'entries': util.list_entries()
    })


def entries(request, title):
    markdowner = Markdown()
    content = util.get_entry(title)

    if content == None:
        return render(request, 'encyclopedia/404.html', {'msg': 'Uh oh! Sorry, the page (' + title + ') you were looking for was not found.'})

    content = markdowner.convert(content)
    return render(request, 'encyclopedia/page.html', {
        'content': content, 'title': title
    })


def new_page(request):
    if request.method == 'POST':
        form = NewPageForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']

            entries = util.list_entries()

            for entry in entries:            
                if title.upper() == entry.upper():
                    return render(request, 'encyclopedia/404.html', {'msg': 'Uh oh! Sorry, the page (' + title + ') already exist with this title.'})
               
            content = form.cleaned_data['content']
            util.save_entry(title, content)
            return HttpResponseRedirect(reverse('wikipedia:page-name',args=[title]))

    return render(request, 'encyclopedia/create_new_page.html', {'form': NewPageForm()})


def edit_page(request, title):
    content = util.get_entry(title)

    form = NewPageForm()
    form.fields['title'].initial = title
    form.fields['content'].initial = content

    if request.method == 'POST':
        form = NewPageForm(request.POST)

        if form.is_valid():
            entries = util.list_entries()

            for entry in entries:
                print(entry)
                # If only the page content edited but the title has kept
                if title == entry:
                    content = form.cleaned_data['content']
                    util.save_entry(title, content)  
                    return HttpResponseRedirect(reverse('wikipedia:page-name',args=[title]))
                # If title has changed, it'll delete and recreate the file with the new title
                elif title != entry:
                    util.delete_entry(title)

                    title = form.cleaned_data['title']
                    content = form.cleaned_data['content']
                    util.save_entry(title, content)  
                    return HttpResponseRedirect(reverse('wikipedia:page-name',args=[title]))

    return render(request, 'encyclopedia/edit_page.html', {'content': content, 'title': title, 'form': form})


def delete_page(request, title):
    util.delete_entry(title)
    return HttpResponseRedirect(reverse('wikipedia:index'))


def random_page(request):
    page_list = util.list_entries()

    # pick a random number from a list
    random_title = sample(page_list, 1)

    return HttpResponseRedirect(reverse('wikipedia:page-name',args=[random_title[0]]))


def search(request):
    page_list = util.list_entries()
    searched_string = request.GET.get('q', '').upper()
    page_found = []

    for page in page_list:
        if searched_string in page.upper():
            page_found.append(page)

    if len(page_found) == 1 and page_found[0].upper() == searched_string:
        return HttpResponseRedirect(reverse('wikipedia:page-name',args=[page_found[0]]))
    elif len(page_found) >= 1:
        return render(request, 'encyclopedia/search.html', {'entries': page_found, 'result': True})
    else:
        return render(request, 'encyclopedia/search.html', {'entries': page_found, 'result': False})

    return HttpResponseRedirect(reverse('wikipedia:index'))

