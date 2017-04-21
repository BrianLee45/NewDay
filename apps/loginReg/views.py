# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from . models import User
from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages

# Create your views here.
def index(request):

    if 'id' in request.session:
        context = {
            "users": User.objects.GetUser(request.session['id'])
        }
    # ##uncomment to view contents of dbase
    # context = {
    #     "users": User.objects.all()
    # }
        return render(request, 'loginReg/index.html', context)

    if request.method == "GET":
        return render(request, 'loginReg/index.html')

def doLogin(request):
    print "Function doLogin"
    if request.method == 'POST':
        objReturn, context = User.objects.ValidateAndLogin(request.POST)

    if objReturn:
        print context['user'].first_name
        request.session['id'] = context['user'].id
        # request.session[''] = context['user']
        # return render(request, 'loginReg/welcome.html', context)
        # return redirect('loginReg:welcome')
        return redirect('secrets:home')

    else:
        for error in context:
            messages.add_message(request, messages.ERROR, error)

        return redirect('/')

def doLogout(request):
    request.session.clear()

    return redirect('loginReg:index')

def showWelcome(request):
    if 'id' in request.session:
        print "showWelcome"
        objReturn = User.objects.GetUser(request.session['id'])

        context = {
            "user": objReturn[0]
        }

    return redirect('secrets:home')
    # return render(request, 'loginReg/welcome.html', context)

def doRegister(request):
    if request.method == 'POST':
        response, context = User.objects.ValidateAndCreate(request.POST)

    if response:
        request.session['id'] = context['user'].id
        messages.info(request, "Thank you for registering!")
        return render(request, 'loginReg/welcome.html', context)
    else:
        for error in context:
            messages.error(request, error)
        return render(request, 'loginReg/index.html')

# def doDelete(request):
#     if request.method == 'POST':
#
#         context = {
#             "users": User.objects.filter(email='tony@starkenterprises.com').delete()
#         }
#
#         return render(request, 'loginReg/index.html')
