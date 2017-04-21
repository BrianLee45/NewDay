from django.shortcuts import render, HttpResponse, redirect

from . models import Secret
from django.contrib import messages

# Create your views here.
def index(request):

    #call to generat latest secrets
    if 'id' in request.session:
        print request.session['id']
        context = {
            "secrets": Secret.objects.GetLatestSecrets(),
            "currentUser": Secret.objects.GetCurrentUser(request.session['id'])
        }

    return render(request, 'secrets/index.html', context)

def showPopular(request):
    #call GetMostPopularSecrets
    context = {
        "posts": Secret.objects.GetMostPopularSecrets(),
        "currentUser": Secret.objects.GetCurrentUser(request.session['id'])
    }

    print context['posts'].created_by.id
    print context['currentUser'].id

    return render(request, 'secrets/popular.html', context)

def doPost(request):
    print "Function doPost"

    if request.method == 'POST':
        response, context = Secret.objects.ValidateAndSave(request)

    if response:
        return redirect('secrets:home')
    else:
        for item in context:
            messages.error(request, item)

    # return render(request, 'secrets/index.html')
    return redirect('secrets:home')

def doDelete(request, secret_id):
    print "Function doDelete"

    retVal = Secret.objects.DeleteSecret(request.session['id'], secret_id)

    if retVal:
        return redirect('secrets:home')
    else:
        messages.error(request, retVal)
        return redirect('secrets:home')

def doLike(request, secret_id):
    print "Function doLike"

    retVal = Secret.objects.LikeSecret(request.session['id'], secret_id)

    if retVal:
        return redirect('secrets:home')
    else:
        messages.error(request, retVal)
    return redirect('secrets:home')
