from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator

from .forms import RegisterForm
from .models import faq as Faq, AdminUser, announcement
from hoctap_others.models import ToDo
from hoctap_main.models import post, test
from profiles.models import profile as member
from profiles.models import notification as Notification
from django.contrib.auth.models import User

import markdown as md
from myfunc.myfunc import GetSideContentData

def indexView(request):
    if "notification" in request.POST:
        notification = Notification.objects.get(id=int(request.POST['notification']))
        direct_post = str(notification.link)
        notification.delete()
        return HttpResponseRedirect(direct_post)
    data = GetSideContentData(request)
    data['posts'] =  post.objects.filter(is_verify=True, is_publish=True, id__gt= post.objects.all().values().count()-10).order_by('-createdAt')
    data['tests'] = test.objects.filter(is_verify=True, is_publish=True, id__gt= test.objects.all().values().count()-10).order_by('-createdAt')
    return render(request, 'home/home.html', data)
    
def registerView(request):
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/')
    return render(request, 'login/register.html', {
        'form': form,
    })

def aboutView(request):
    if "notification" in request.POST:
        notification = Notification.objects.get(id=int(request.POST['notification']))
        direct_post = str(notification.link)
        notification.delete()
        HttpResponseRedirect(direct_post)
    return render(request, 'home/about.html', GetSideContentData(request))

def teamView(request):
    data = {}
    data['AdminUsers'] = AdminUser.objects.all().order_by('role')
    return render(request, 'home/team.html', data)

def faqsView(request):
    data = {}
    faqs = Faq.objects.all()
    for faq in faqs:
        faq.content = md.markdown(faq.content).replace('<img', "<img class='content-img'")
    data['faqs'] = faqs
    return render(request, 'home/faq/faqs.html', data)

def supportView(request):
    return render(request, 'home/support.html')

def AnnouncementListView(request):
    if "notification" in request.POST:
        notification = Notification.objects.get(id=int(request.POST['notification']))
        direct_post = str(notification.link)
        notification.delete()
        HttpResponseRedirect(direct_post)
    data = GetSideContentData(request)
    Announcement_list = announcement.objects.all().order_by('-date')
    paginator = Paginator(Announcement_list, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    data['announcements'] = page_obj
    return render(request, 'announcement/announcements.html', data)

def AnnouncementDetailView(request, id):
    if "notification" in request.POST:
        notification = Notification.objects.get(id=int(request.POST['notification']))
        direct_post = str(notification.link)
        notification.delete()
        HttpResponseRedirect(direct_post)
    data = GetSideContentData(request)
    announcementData = announcement.objects.get(id=id)
    announcementData.content = md.markdown(announcementData.content).replace('<img', "<img class='content-img'")
    data ['announcement'] = announcementData
    return render(request, 'announcement/announcement.html', data)

