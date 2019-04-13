from django.shortcuts import render, redirect
from django.http import HttpResponse
from . forms import LoginForm
import requests
from django.template import RequestContext

def login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            payload = {"email": email, "password": password}
            req = requests.post('https://mybook.ru/api/auth/', payload)
            if req.status_code == 200:
                session = req.cookies['session']
                response = redirect('book_list')
                response.set_cookie('session', session)
                return response
            else:
                return HttpResponse ('Wrong request')
        else:
            form = LoginForm()
    else:
        form = LoginForm()
        return render(request, 'books/login.html', {'form': form})



def book_list(request):
    base_url = 'https://mybook.ru'
    if 'session' in request.COOKIES:
        cookies = {'session': request.COOKIES.get('session')}
        req = requests.get('https://mybook.ru/api/bookuserlist/', headers={"Accept":"application/json, version=5"}, cookies=cookies)
        books = []
        while req.json()['meta']['next'] != None:
            req = requests.get(base_url + req.json()['meta']['next'], headers={"Accept":"application/json, version=5"}, cookies=cookies)
            for num in range(int(req.json()['meta']['total_count'])):
                book={}
                book['name'] = req.json()['objects'][num]['book']['name']
                book['cover'] = req.json()['objects'][num]['book']['default_cover']
                try:
                    book['author'] = req.json()['objects'][num]['book']['main_author']['cover_name']
                except TypeError:
                    book['author'] = 'Автор отсутствует'
                books.append(book)
        else:
            for num in range(int(req.json()['meta']['total_count'])):
                book={}
                book['name'] = req.json()['objects'][num]['book']['name']
                book['cover'] = req.json()['objects'][num]['book']['default_cover']
                try:
                    book['author'] = req.json()['objects'][num]['book']['main_author']['cover_name']
                except TypeError:
                    book['author'] = 'Автор отсутствует'
                books.append(book)
        return render(request, 'books/books.html', {'books': books})
    else:
        response = redirect('login')
        return response