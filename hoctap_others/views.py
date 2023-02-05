from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect

from hoctap_others.models import ToDo, news
from hoctap_others.forms import CreateShareForm, ChangeShareForm
from profiles.models import profile as member, notification as Notification
from django.contrib.auth.models import User

import markdown as md

from myfunc.myfunc import GetSideContentData

@login_required(login_url='/login')
def TodoListView(request):
    todolist = ToDo.objects.filter(user=User.objects.get(username=request.user.username)).order_by('is_finished')
    if request.method == 'POST':
        if 'taskFinish' in request.POST.dict():
            task = ToDo.objects.get(id = request.POST['taskFinish'])
            task.is_finished = True
            task.save()
    return render(request, 'hoctap_others/todo/todolist.html', {
        "todo": todolist,
    })
    
@login_required(login_url='/login')
def TodoCreateView(request):
    if request.method == 'POST':
        newTodo = ToDo.objects.create(
            user=User.objects.get(username=str(request.user.username)),
            title=request.POST['taskTitle'],
            detail=request.POST['taskDetail'],
        )
        return HttpResponseRedirect(f'/hoctap-others/todo/detail/{newTodo.id}')
    return render(request, 'hoctap_others/todo/taskcreate.html')

@login_required(login_url='/login')
def TodoTaskDetailView(request, id):
    task = ToDo.objects.get(id=id)
    if request.method == 'POST':
        if 'is_finished' in request.POST.dict():
            if request.POST['is_finished'] == 'false':
                task.is_finished = False
            elif request.POST['is_finished'] == 'true':
                task.is_finished = True
            task.save()

        if 'taskTitle' in request.POST.dict():
            taskTitle = request.POST['taskTitle']
            taskDetail = request.POST['taskDetail']
            if taskTitle.count(" ") != len(taskTitle):
                task.title = taskTitle
            task.detail = taskDetail
            task.save()
        task = ToDo.objects.get(id=id)
        
    return render(request, 'hoctap_others/todo/taskdetail.html', {
        "task" : task,
    })

def newsListView(request):
    if "notification" in request.POST:
        notification = Notification.objects.get(id=int(request.POST['notification']))
        direct_post = str(notification.link)
        notification.delete()
        HttpResponseRedirect(direct_post)
    data = GetSideContentData(request)
    data["news"] = news.objects.all().order_by('-id')
    return render(request, 'hoctap_others/news/list.html', data)

def newsDetailView(request, id):
    if "notification" in request.POST:
        notification = Notification.objects.get(id=int(request.POST['notification']))
        direct_post = str(notification.link)
        notification.delete()
        HttpResponseRedirect(direct_post)
    data = GetSideContentData(request)
    newinfo = news.objects.get(id=id)
    newinfo.description = md.markdown(newinfo.content).replace('<img', "<img class='content-img'")
    data['news'] = newinfo
    return render(request, 'hoctap_others/news/detail.html', data)