from hoctap_others.models import ToDo
from profiles.models import profile as member
from profiles.models import notification as Notification
from home.models import announcement, BadWord
from hoctap_main.models import post, test
from hoctap_others.models import news
from django.contrib.auth.models import User

from django.http import HttpResponseRedirect

def GetSideContentData(request):
    if request.method == "POST":
            if "todo" in request.POST:
                task = ToDo.objects.get(id=request.POST['todo'])
                task.is_finished = True
                task.save()

    topUsers = member.objects.filter(NumberOfPosts__gt=0).order_by('-NumberOfPosts')
    TopUsersForDisplay=[]
    cnt = 1
    for topUser in topUsers:
        TopUsersForDisplay.append(topUser)
        if cnt == 5:
            break
        cnt+=1

    data = {
        "announcements": announcement.objects.filter(id__gt=announcement.objects.all().values().count()-10).order_by('-date'),
        "topUsers": TopUsersForDisplay,
        "news": news.objects.all().order_by('-date')
    }
    data['info'] = [
        f"<b>{member.objects.all().count()}</b> tài khoản đã được tạo",
        f"<b>{post.objects.filter(is_publish=True, is_verify=True).count()}</b> bài viết về học tập đã được tạo",
        f"<b>{test.objects.filter(is_publish=True, is_verify=True).count()}</b> bài viết về kiểm tra đã được tạo"
    ]
    if request.user.is_authenticated:
        data["todo"] = ToDo.objects.filter(user=User.objects.get(username=request.user.username)).order_by("is_finished")
        data['notifications'] = Notification.objects.filter(user=User.objects.get(username=request.user.username)).order_by('-date','-id')

    return data

def getBadwords():
    return BadWord.objects.all()