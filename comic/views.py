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
        context['comics'] = UploadComics.objects.all()
        return render(request, 'home.html', context)
    else:
        return render(request, 'auth.html', context)


@login_required
def images(request, comics_id):
    comics = Comics.objects.get(general_id=comics_id)
    context = {
        'comics': comics
    }
    return render_to_response('images.html', context)


def coordinates(request, image_id):
    context = {
        'image': ComicsImage.objects.get(id=image_id),
    }
    if request.method == 'POST':
        if request.is_ajax():
            coordinatez = request.POST.get('coordinates')
            arr = coordinatez.split('|')
            array = arr[1:len(arr)-1]
            image = ComicsImage.objects.get(id = image_id)
            for i in array:
                coordinate = i.split(' ')
                x = float(coordinate[0].split(':')[1])
                y = float(coordinate[1].split(':')[1])
                w = float(coordinate[2].split(':')[1])
                h = float(coordinate[3].split(':')[1])
                coor = Coordinate.objects.create(x=x,y=y,w=w,h=h)
                coor.save()
                image.coordinates.add(coor)
            image.save()
    return render_to_response('coordinates.html', context)