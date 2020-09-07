from datetime import datetime
from django.shortcuts import render, get_object_or_404, redirect
from application.models import *
from django.http import HttpResponse
import json
from django.views.decorators.csrf import csrf_exempt
import random
from django.core.files.base import ContentFile
import base64


def choice_player(request):
    data = CustomUser.objects.filter(use=True)
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
        name__in=name_exclude).order_by('points').reverse().filter(use=True)
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
    try:
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


def stream(request):
    return render(request, 'blog/stream.html')


def embed(request):
    return render(request, 'blog/embed.html')


def start(request):
    return render(request, 'mariage/acceuil.html')


def hubPhoto(request):
    return render(request, 'mariage/hubPhotos.html')


def view(request):
    return render(request, 'mariage/ceremonie.html')


def challenge(request):
    return render(request, 'mariage/challenge.html')


def photobooth(request):
    return render(request, 'mariage/photobooth.html')


def getChallenge(request, name):
    challenges = Challenge.objects.all()
    group, created = Group.objects.get_or_create(name=name)
    groupChallenge = ChallengeGroups.objects.filter(group=group)
    challengeDone = []
    challengeToDo = []
    challengeArray = []
    groupChallengeArray = []
    for challenge in challenges:
        if not groupChallenge:
            challengeToDo.append(
                {
                    'challenge': challenge,
                    'group': group.id
                }
            )
        challengeArray.append(challenge.id)
    for item in groupChallenge:
        groupChallengeArray.append(item.challenge.id)
        if item.challenge.id in challengeArray:
            challengeDone.append(
                {
                    'id': item.id,
                    'challenge': item.challenge,
                    'like': item.like,
                    'photos': item.photos,
                    'group': group.id
                }
            )
        else:
            challengeToDo.append(
                {
                    'challenge': item.challenge,
                    'group': group.id
                }
            )
    for element in challenges:
        if not groupChallenge:
            return render(request, 'mariage/photoChallenge.html', {'challengeDone': challengeDone, 'challengeToDo': challengeToDo, 'name': name})
        if element.id not in groupChallengeArray:
            challengeToDo.append(
                {
                    'challenge': element,
                    'group': group.id
                }
            )
    return render(request, 'mariage/photoChallenge.html', {'challengeDone': challengeDone, 'challengeToDo': challengeToDo, 'name': name})


@csrf_exempt
def postChallenge(request, challengeId, groupId):
    challenge = get_object_or_404(Challenge, pk=challengeId)
    group = get_object_or_404(Group, pk=groupId)
    try:
        image = request.FILES['image']
    except KeyError:
        # You can catch KeyError here as well
        # and return a response with 400 status code
        try:
            image = request.POST['data']
        except KeyError:
            return HttpResponse('No file content', status=400)
    challengeGroup, created = ChallengeGroups.objects.get_or_create(
        challenge=challenge, group=group, photos=image)
    if created:
        challengeGroup.save()
    else:
        challengeGroup.update(challenge=challenge, group=group, photos=image)
    return redirect('/challenge/' + group.name)


@csrf_exempt
def postChallengeDone(request, id):
    try:
        image = request.FILES['image']
    except KeyError:
        # You can catch KeyError here as well
        # and return a response with 400 status code
        try:
            image = request.POST['data']
        except KeyError:
            return HttpResponse('No file content', status=400)
    challengeGroup = ChallengeGroups.objects.get(id=id)
    challengeGroup.photos = image
    challengeGroup.save()
    return redirect('/challenge/' + challengeGroup.group.name)


@csrf_exempt
def deleteChallengeDone(request, id):
    challengeGroup = ChallengeGroups.objects.get(id=id)
    challengeGroup.delete()
    return redirect('/challenge/' + challengeGroup.group.name)


def getAllChallenge(request):
    challenge = Challenge.objects.all()
    return render(request, 'mariage/allChallenge.html', {'challenges': challenge})


def getMyChallenge(request, id):
    challenge = Challenge.objects.get(id=id)
    challenges = ChallengeGroups.objects.filter(challenge=challenge)
    data = []
    for item in challenges:
        data.append({'photos': item.photos, 'name': item.challenge.name,
                     'description': item.challenge.description, 'group': item.group.name})
    return render(request, 'mariage/getMyChallenge.html', {'challenges': data, 'name': challenge.name, 'description': challenge.description})


def getPhotobooth(request):
    photobooth = Photobooth.objects.all()
    return render(request, 'mariage/getPhotobooth.html', {'photobooth': photobooth})


def savePhotoBooth(request):
    try:
        image = request.FILES['image']
    except KeyError:
        # You can catch KeyError here as well
        # and return a response with 400 status code
        try:
            imageData = request.POST.get('image')
        except KeyError:
            return HttpResponse('No file content', status=400)
    format, imgstr = imageData.split(';base64,')
    print("format", format)
    ext = format.split('/')[-1]
    data = ContentFile(base64.b64decode(imgstr))
    file_name = "'myphoto." + ext
    photobooth, created = Photobooth.objects.get_or_create(photos=data)
    photobooth.photos.save(file_name, data, save=True)
    return redirect('/photobooth')
