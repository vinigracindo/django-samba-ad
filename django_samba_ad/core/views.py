from django.conf import settings
from django.forms import model_to_dict
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from django_samba_ad.core.decorators import synchronize_user
from django_samba_ad.core.forms import UserForm
from django_samba_ad.core.models import User


@synchronize_user
def index(request):
    users = User.objects.all()
    context ={
        'users': users,
    }
    return render(request, 'index.html', context)


@synchronize_user
def user_edit(request):
    username = request.GET.get('user')
    user = User.objects.get(username=username)
    form = UserForm(instance=user)
    if request.method == "POST":
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()

            active_directory = settings.STRATEGY_AD_MODEL(
                settings.SAMBA_SERVER_IP,
                settings.SAMBA_SERVER_PORT,
                settings.SAMBA_ADMIN_USER,
                settings.SAMBA_ADMIN_PASSWORD,
            )

            active_directory.update_user(model_to_dict(user))

            return HttpResponseRedirect(reverse('index'))

    context = {
        'form': form
    }
    return render(request, 'user_edit.html', context)
