from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.models import User
from .models import profile
from .models import notification as Notification
from hoctap_main.models import post, test
from .forms import ChangeProfileForm
from markdown import markdown

from myfunc.myfunc import GetSideContentData

def profileView(request, username):
    if "notification" in request.POST:
        notification = Notification.objects.get(id=int(request.POST['notification']))
        direct_post = str(notification.link)
        notification.delete()
        HttpResponseRedirect(direct_post)
    data = GetSideContentData(request)
    user = User.objects.get(username=username)
    ChangeNumberOfPosts_User = profile.objects.get(username=user)
    ChangeNumberOfPosts_User.NumberOfPosts = post.objects.filter(author=user, is_publish=True).values().count()
    ChangeNumberOfPosts_User.save()
    
    posts = post.objects.filter(author=user, is_verify=True, is_publish=True)
    tests = test.objects.filter(author=user, is_verify=True, is_publish=True)

    data['User'] = profile.objects.get(username=user)
    data['is_own_profile'] = str(request.user.username) == str(user.username)
    data['posts'] = posts
    data['is_has_tests'] = (tests != [])
    data['tests'] = tests

    return render(request, 'profile/Profile.html', data)

def profileChangeView(request, username):
    user = User.objects.get(username=username)
    userProfile = profile.objects.get(username=user)

    if str(request.user.username) != str(userProfile.username):
        return HttpResponseRedirect(f'/profile/detail/{user.username}')

    form = ChangeProfileForm()
    if request.method == 'POST':
        form = ChangeProfileForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['firstname']
            last_name = form.cleaned_data['lastname']
            user.first_name = first_name
            user.last_name = last_name 
            user.save()
            userProfile.name = last_name + " " + first_name
            userProfile.about = form.cleaned_data['about']
            userProfile.save()
            return HttpResponseRedirect(f'/profile/detail/{user.username}')

    
    form.fields['firstname'].initial = user.first_name
    form.fields['lastname'].initial = user.last_name
    form.fields['about'].initial = userProfile.about


    return render(request, 'profile/ProfileChange.html', {
        "form": form,
    })

def claimRankView(request, username):
    user = User.objects.get(username=username)
    userProfile = profile.objects.get(username=user)
    userPostCount = post.objects.filter(author=user).values().count()
    result = ''
    isClaimed = False
    if request.method == 'POST':
        if (10 <= userPostCount) and (userPostCount < 50) and (userProfile.rank != 'C'):
            userProfile.rank = 'C'
            result = 'Bạn đã nhận được hạng <b>Đồng</b>!'
        elif (50 <= userPostCount) and (userPostCount < 200) and (userProfile.rank != 'B'):
            userProfile.rank = 'B'
            result = 'Bạn đã nhận được hạng <b>Bạc</b>!'
        elif (200 <= userPostCount) and (userProfile.rank != 'A'):
            userProfile.rank = 'A'
            result = 'Bạn đã nhận được hạng <b>Vàng</b>!'
        else:
            result = 'Có vẻ bạn chưa nhận được hạng mới!'
        userProfile.save()
        isClaimed = True
    return render(request, 'profile/claimRank.html', {
        'isClaimed': isClaimed,
        'rank': result,
    })

def searchView(request):
    if "notification" in request.POST:
        notification = Notification.objects.get(id=int(request.POST['notification']))
        direct_post = str(notification.link)
        notification.delete()
        HttpResponseRedirect(direct_post)
    data = GetSideContentData(request)
    try:
        SearchData = {
            "is_searching": True,
            "usersFound": User.objects.filter(username__icontains=request.GET['username'])
        }
    except:
        SearchData = {
            "is_searching": False,
        }
    data.update(SearchData)
    return render(request, 'profile/SearchProfile.html', data)

def topUserListView(request):
    if "notification" in request.POST:
        notification = Notification.objects.get(id=int(request.POST['notification']))
        direct_post = str(notification.link)
        notification.delete()
        HttpResponseRedirect(direct_post)
    data = GetSideContentData(request)
    #update NumberOfPost for all users
    allUser = profile.objects.filter(NumberOfPosts__gt=0).order_by('-NumberOfPosts')
    for user in allUser:
        user.NumberOfPosts = post.objects.filter(is_publish=True, author=user.username).values().count()
        user.save()
    #pagination
    valid_users = profile.objects.filter(NumberOfPosts__gt=0).order_by('-NumberOfPosts')
    paginator = Paginator(valid_users, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    data['topUsers'] = page_obj
    return render(request, 'profile/topUsers.html', data)