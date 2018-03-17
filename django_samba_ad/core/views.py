from django.shortcuts import render

from django_samba_ad.core.models import User


def index(request):
    users = User.objects.all()
    context ={
        'users': users,
    }
    return render(request, 'index.html', context)
