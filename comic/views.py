from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.core.context_processors import csrf
from django.contrib import auth
from django.shortcuts import render_to_response
from django.http import JsonResponse

from .models import *


# Create your views here.


def home(request):
    context = {}
    context.update(csrf(request))
    if request.POST:
        username = request.POST.get("username", "")
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            return render(request, 'auth.html', context)
    elif request.user.is_active:
        context['comics'] = Comics.objects.all()
        return render(request, 'home.html', context)
    else:
        return render(request, 'auth.html', context)


@login_required
def images(request, comics_id):
    context = {
        'images': ComicsImage.objects.filter(comics_id=comics_id)
    }
    return render_to_response('images.html', context)


def coordinates(request, image_id):
    context = {
        'image': ComicsImage.objects.get(id=image_id),
        'coordinates': Coordinate.objects.filter(image_id=image_id)
    }
    ###############################################################################
    if request.method == 'POST':
        # POST goes here . is_ajax is must to capture ajax requests. Beginner's pit.
        if request.is_ajax():
            # Always use get on request.POST. Correct way of querying a QueryDict.
            coordinatez = request.POST.get('coordinates')
            data = {"coordinates": coordinatez}
            # Returning same data back to browser.It is not possible with Normal submit
            print data
            return JsonResponse(data)

            # Get goes here
    #############################################################################
    return render_to_response('coordinates.html', context)
