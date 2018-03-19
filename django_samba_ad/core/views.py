from django.shortcuts import render

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
    user = request.GET.get('user')
    form = UserForm(instance=User.objects.get(username=user))
    context = {
        'form': form
    }
    return render(request, 'user_edit.html', context)
