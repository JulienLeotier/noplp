from datetime import datetime
from django.shortcuts import render, get_object_or_404
from application.models import *
from django.http import HttpResponse
import json
from django.views.decorators.csrf import csrf_exempt
import random


def choice_player(request):
    data = CustomUser.objects.all()
    myData = []
    for user in data:
        if user.pseudo != 'ADMIN':
            myData.append(
                {'name': user.pseudo, 'image': user.avatar, 'id': user.pk})
    return render(request, 'blog/choice_perso.html', {'characters': myData})


def choice_cat(request, nombre1, nombre2):
    categorie = []
    name_exclude = []
    user1 = CustomUser.objects.get(pk=nombre1)
    user2 = CustomUser.objects.get(pk=nombre2)
    historique, created = Historique.objects.get_or_create(
        primary_user=CustomUser.objects.get(pk=nombre1),
        secondary_user=CustomUser.objects.get(pk=nombre2))
    for x in historique.categorie.all():
        name_exclude.append(x)
    categorie = Categorie.objects.exclude(
        name__in=name_exclude).order_by('points').reverse()
    return render(request, 'blog/choice_categorie.html', {'historiques': historique, 'categories': categorie, 'user1': user1, 'user2': user2})


@csrf_exempt
def add_score(request, id, nombre1, nombre2, catId):
    if request.method == 'POST':
        historique = Historique.objects.get(id=id)
        historique.categorie.add(Categorie.objects.get(id=catId))
        historique.scoreUser = historique.scoreUser + nombre1
        historique.scoreUser2 = historique.scoreUser2 + nombre2
        historique.save()
        return HttpResponse(json.dumps({'message': 'historique update',
                                        'historique': {
                                            'scoreUser': historique.scoreUser,
                                            'scoreUser2': historique.scoreUser2
                                        }, 'catId': catId}),
                            content_type='application/json')
    else:
        return HttpResponse(json.dumps({'message': 'Merci d\'effectuer un POST'}),
                            content_type='application/json')


def choice_music(request, catId):
    categorie = Categorie.objects.get(id=catId)
    music = Musique.objects.filter(categorie=categorie, use=False)
    try :
        choice_two_music = random.sample(list(music), k=2)
    except:
        return render(request, 'blog/choice_music.html', {'music': music})
    return render(request, 'blog/choice_music.html', {'music': choice_two_music})

@csrf_exempt
def use_music(request, musicId):
    if request.method == 'POST':
        music = Musique.objects.get(id=musicId)
        music.use = True
        music.save()
        return HttpResponse(json.dumps({'message': 'update music ok'}), content_type='application/json')
    else:
        return HttpResponse(json.dumps({'message': 'Merci d\'effectuer un POST'}),
                            content_type='application/json')


def player(request, id):
    music = Musique.objects.get(id=id)
    return render(request, 'blog/player.html', {'music': music})
