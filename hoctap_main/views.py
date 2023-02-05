from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect

from .forms import CreatePostForm, ChangePostForm, QuestionForm, AnswerForm, SendMessageForm, CreateTestForm ,ChangeTestForm
from .models import post, QnA, chatQnA, test


from profiles.models import profile as member, notification as Notification
from django.contrib.auth.models import User

import markdown as md
from unidecode import unidecode
import re

from myfunc.myfunc import GetSideContentData

def indexView(request):
    #chưa sửa xong
    if "notification" in request.POST:
        notification = Notification.objects.get(id=int(request.POST['notification']))
        direct_post = str(notification.link)
        notification.delete()
        HttpResponseRedirect(direct_post)
    data = GetSideContentData(request)
    paginator = Paginator(post.objects.filter(is_verify=True, is_publish=True).order_by('-createdAt'), 10)
    try:
        page_number = request.GET['page']
    except:
        page_number = 1
    page_obj = paginator.get_page(page_number)

    data['posts'] = page_obj
    return render(request, 'hoctap/hoctap.html', data)

# post 

def PostListView(request):
    data = GetSideContentData(request)
    PostList = post.objects.filter(is_verify=True, is_publish=True)
    if ('date' in request.GET) or ('like' in request.GET):
        if ('date' in request.GET) and (request.GET['date'] in ['old', 'new']):
            if request.GET['date'] == 'old':
                PostList = PostList.order_by('createdAt')
            else:
                PostList = PostList.order_by('-createdAt')
        else:
            PostList = PostList.order_by('-createdAt')

        if ('like' in request.GET) and (request.GET['like'] in ['most', 'least']):
            if request.GET['like'] == 'least':
                PostList = PostList.order_by('NumberOfLike')
            else:
                PostList = PostList.order_by('-NumberOfLike')
    else:
        PostList = PostList.order_by('-createdAt')


    paginator = Paginator(PostList, 10)
    try:
        page_number = request.GET['page']
    except:
        page_number = 1
    page_obj = paginator.get_page(page_number)

    data['posts'] = page_obj

    return render(request, 'hoctap/post/postList.html', data)

def searchPostView(request):
    if "notification" in request.POST:
        notification = Notification.objects.get(id=int(request.POST['notification']))
        direct_post = str(notification.link)
        notification.delete()
        HttpResponseRedirect(direct_post)
    data = GetSideContentData(request)
    data['is_searching'] = False

    if (request.method == 'GET') and ('title' in request.GET):
        if (request.GET['username'] != "") and (request.GET['username'] in User.objects.all()):
            data['posts'] = post.objects.filter(author=User.objects.get(username=request.GET['username']), title__icontains = request.GET['title'], is_verify=True, is_publish=True) | post.objects.filter(author=User.objects.get(username=request.GET['username']), post_id__contains = request.POST['title'], is_verify=True, is_publish=True)
            data['is_searching'] = True
        else:
            data['posts'] = post.objects.filter(title__icontains = request.GET['title'], is_verify=True, is_publish=True) | post.objects.filter(post_id__contains = request.GET['title'], is_verify=True, is_publish=True)
            data['is_searching'] = True
        data['isUserinDB'] = request.GET['username'] in User.objects.all()
        data['Userinclude'] = request.GET['username']


    return render(request, 'hoctap/post/SearchPost.html', data)

def PostDetailView(request, post_id):
    if "notification" in request.POST:
        notification = Notification.objects.get(id=int(request.POST['notification']))
        direct_post = str(notification.link)
        notification.delete()
        HttpResponseRedirect(direct_post)
    data = GetSideContentData(request)

    baiviet = post.objects.get(post_id=post_id)
    if request.method == 'POST':
        baiviet = post.objects.get(post_id=post_id)
        if request.user.is_authenticated:
            if not (request.user.username in baiviet.interactiveUsers):
                if request.POST['vote'] == "like":
                    baiviet.NumberOfLike += 1
                else:
                    baiviet.NumberOfDislike += 1
            else:
                if (request.POST['vote'] != baiviet.interactiveUsers.get(request.user.username)):
                    if request.POST['vote'] == "like":
                        baiviet.NumberOfLike += 1
                        baiviet.NumberOfDislike -= 1
                    else:
                        baiviet.NumberOfDislike += 1
                        baiviet.NumberOfLike -= 1
            baiviet.interactiveUsers.update({
                f"{request.user.username}": request.POST['vote']
            })
            baiviet.save()

    hoidap = QnA.objects.filter(post=baiviet, is_finished=True)
    # if (baiviet.is_verify == False) or ((baiviet.is_publish == False) and (str(baiviet.author) != str(request.user.username))):
    #     return HttpResponseRedirect('/')
    
    if ((baiviet.is_verify == False) or (baiviet.is_publish == False)) and (str(baiviet.author) != str(request.user.username)):
        return HttpResponseRedirect('/')

    baiviet.content = md.markdown(baiviet.content).replace('<img', "<img class='content-img'")
    if hoidap.values().count() >= 15:
        isLargeQnA = True
    else:
        isLargeQnA = False
    own_post = str(request.user.username) == str(baiviet.author)
    last_voted = 'none'
    if request.user.username in baiviet.interactiveUsers:
        last_voted = str(baiviet.interactiveUsers.get(request.user.username))

    data.update({
        "post": baiviet,
        "isLargeQnA": isLargeQnA,
        "hoidaps": hoidap,
        "own_post": own_post,
        "interactiveUsersCount": int(baiviet.NumberOfLike) - int(baiviet.NumberOfDislike),
        "last_voted": last_voted,
    })

    return render(request, 'hoctap/post/postDetail.html', data)


@login_required(login_url='/login')
def createNewPostPageView(request):
    form = CreatePostForm()
    is_success = False
    if request.method == 'POST':
        form = CreatePostForm(request.POST)
        if form.is_valid():
            post_id = request.POST['title'] + '_' + str(post.objects.all().count() + 1)
            post_id = post_id.replace('  ',' ').replace(' ', '_').lower()
            post_id = re.sub(r'\W', '', post_id)
            post_id = unidecode(post_id)
            is_success = True
            post.objects.create(
                post_id = post_id,
                title = request.POST['title'],
                content = request.POST['content'],
                author = request.user,
            )

    data = {
        "form": form,
        "is_success": is_success,
    }

    return render(request, 'hoctap/post/createNewPost.html', data)

def PostChangeView(request, post_id):
    postdetail = post.objects.get(post_id = post_id)
    if (postdetail.is_verify == False) or (postdetail.is_publish == False):
        return HttpResponseRedirect('/')
    if (str(request.user.username) != str(postdetail.author)):
        return HttpResponseRedirect('/')
    form = ChangePostForm()
    if request.method == 'POST':
        form = ChangePostForm(request.POST)
        if (form.is_valid()):
            postdetail.title = request.POST['title']
            postdetail.content = request.POST['content']
            postdetail.save()
            return HttpResponseRedirect(f'/hoctap/posts/{postdetail.post_id}/')
    form.fields['title'].initial = postdetail.title
    form.fields['content'].initial = postdetail.content
    return render(request, 'hoctap/post/postchange.html', {
        "form": form,
        "post": postdetail,
    })

def PostDeleteView(request, post_id):
    postDetail = post.objects.get(post_id=post_id)
    if (str(request.user.username) != str(postDetail.author)):
        return HttpResponseRedirect(f'/hoctap/posts/{postDetail.post_id}')
    postDetail.delete()
    return HttpResponseRedirect('/')


def PostQnAListView(request, post_id):
    #phần này là display các qna đã được trả lời (mọi người dùng có thể xem)
    hoidap = QnA.objects.filter(post=post.objects.get(post_id=post_id), is_finished=True)

    return render(request, 'hoctap/post/hoidap/listFinished.html', {
        "post": post.objects.get(post_id=post_id),
        "hoidaps": hoidap,
    })

@login_required(login_url='/login')
def PostQnASeeQuestions_forAuthor(request, post_id):
    #phần này là display các qna chưa được trả lời (owner post và admin chỉ có thể xem)

    baiviet = post.objects.get(post_id=post_id)
    hoidap = QnA.objects.filter(post=baiviet).order_by('is_finished')

    if (str(baiviet.author) != str(request.user.username)) and ( member.objects.get(username=request.user).role != 'A'):
        return HttpResponseRedirect(f'/hoctap/posts/{baiviet.post_id}')

    
    return render(request, 'hoctap/post/hoidap/listAllQuestions_forAuthor.html', {
        'hoidaps': hoidap,
        'post': baiviet,
    })

@login_required(login_url='/login')
def PostQnASeeQuestions_forQuestioner(request, post_id):
    #phần này là display các qna của người xem post gửi đến

    baiviet = post.objects.get(post_id=post_id)
    hoidap = QnA.objects.filter(post=baiviet, questioner=str(request.user.username)).order_by('is_finished')
        
    return render(request, 'hoctap/post/hoidap/listAllQuestions_forQuestioner.html', {
        'hoidaps': hoidap,
        'post': baiviet,
    })

@login_required(login_url='/login')
def PostQnACreateQuestion(request, post_id):
    baiviet = post.objects.get(post_id=post_id)
    form = QuestionForm()
    isSent = False
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            hoidap = QnA.objects.create(
                post=baiviet,
                question=request.POST['question'],
                questioner=request.user.username,
                answerer=User.objects.get(username=baiviet.author).username,
            )

            Notification.objects.create(
                user=User.objects.get(username=baiviet.author),
                link= f'/hoctap/posts/{baiviet.post_id}/hoidap/{hoidap.id}/answer',
                content=f"Bài viết <b><i>{baiviet.title}</i></b> đã được nhận một thắc mắc từ <b><i>{request.user.username}</i></b>", 
            )
            isSent=True

    if str(baiviet.author) == str(request.user.username):
        return HttpResponseRedirect(f'/hoctap/posts/{baiviet.post_id}')
    return render(request, 'hoctap/post/hoidap/question.html',
    {
        "post": baiviet,
        "form": form,
        "isSent": isSent,
    })

@login_required(login_url='/login')
def PostQnA_Answer(request, post_id, idQnA):
    baiviet = post.objects.get(post_id=post_id)
    hoidap = QnA.objects.get(id=idQnA)
    form = AnswerForm()
    isSent = False
    if str(baiviet.author) != str(request.user.username):
        return HttpResponseRedirect(f'/hoctap/posts/{baiviet.post_id}')

    if request.method == 'POST':
            form = AnswerForm(request.POST)
            if form.is_valid():
                hoidap.answer = request.POST['answer']
                hoidap.save()
                isSent=True

                Notification.objects.create(
                    user=User.objects.get(username=hoidap.questioner),
                    link= f'/hoctap/posts/{baiviet.post_id}/hoidap/{hoidap.id}',
                    content=f"Thắc mắc của bạn đã được trả lời trong bài viết <b><i>{baiviet.title}</i></b>", 
                )

    return render(request, 'hoctap/post/hoidap/answer.html',{
        "hoidap": hoidap,
        "post": baiviet,
        "form": form,
        "isSent": isSent,
    })

@login_required(login_url='/login')
def PostQnAInfo(request, post_id, idQnA):
    messageForm = SendMessageForm()
    baiviet = post.objects.get(post_id=post_id)
    hoidap = QnA.objects.get(id=idQnA)
    chat = chatQnA.objects.filter(QnA=hoidap, isHide=False).order_by('datetime')
    if not (str(request.user.username) in [hoidap.answerer, hoidap.questioner]):
        HttpResponseRedirect(f'/hoctap/posts/{baiviet.post_id}')

    if request.method == 'POST':
        if 'is-chat' in request.POST:
            if request.POST['is-chat'] == 'enable-chat':
                hoidap.is_open_chat = True
            else:
                hoidap.is_open_chat = False
                hoidap.is_finished = True
            hoidap.save()
        elif 'message' in request.POST:
            messageForm = SendMessageForm(request.POST)
            if messageForm.is_valid():
                chatQnA.objects.create(
                    QnA=hoidap,
                    user= User.objects.get(username=request.user.username),
                    content= request.POST['message']
                )
                userGetNotification = '' #Đây sẽ là người nhận thông báo
                if str(request.user.username) == hoidap.answerer:
                    userGetNotification = hoidap.questioner
                else:
                    userGetNotification = hoidap.answerer
                Notification.objects.create(
                    user=User.objects.get(username=userGetNotification),
                    link= f'/hoctap/posts/{baiviet.post_id}/hoidap/{hoidap.id}',
                    content=f"Bạn đã được nhận một tin nhắn từ <b><i>{request.user.username}</i></b> của bài viết <b><i>{baiviet.title}</i></b> ", 
                )
                return HttpResponseRedirect(f'/hoctap/posts/{baiviet.post_id}/hoidap/{hoidap.id}')
        elif 'close-qna' in request.POST:
            hoidap.is_finished = True
            hoidap.save()
            userGetNotification = '' #Đây sẽ là người nhận thông báo
            if str(request.user.username) == hoidap.answerer:
                userGetNotification = hoidap.questioner
            else:
                userGetNotification = hoidap.answerer
            Notification.objects.create(
                user=User.objects.get(username=userGetNotification),
                link= f'/hoctap/posts/{baiviet.post_id}/hoidap/{hoidap.id}',
                content=f"<b><i>{request.user.username}</i></b> đã đóng hỏi đáp!", 
            )
            return HttpResponseRedirect(f'/hoctap/posts/{baiviet.post_id}/')
        
        elif 'message-delete' in request.POST:
            message = chatQnA.objects.get(id=request.POST['message-delete'])
            message.isHide = True
            message.save()
            return HttpResponseRedirect(f'/hoctap/posts/{baiviet.post_id}/hoidap/{hoidap.id}')

    return render(request, 'hoctap/post/hoidap/chat.html', {
        "form": messageForm,
        "post": baiviet,
        "hoidap": hoidap,
        "chat": chat,
    })

# # Test

def TestListView(request):
    if "notification" in request.POST:
        notification = Notification.objects.get(id=int(request.POST['notification']))
        direct_post = str(notification.link)
        notification.delete()
        HttpResponseRedirect(direct_post)
    data = GetSideContentData(request)
    TestList = test.objects.filter(is_verify=True, is_publish=True)
    if ('date' in request.GET) and (request.GET['date'] in ['old', 'new']):
        if request.GET['date'] == 'old':
                TestList = TestList.order_by('createdAt')
        else:
                TestList = TestList.order_by('-createdAt')

    paginator = Paginator(TestList, 10)
    try:
        page_number = request.GET['page']
    except:
        page_number = 1
    page_obj = paginator.get_page(page_number)

    data['tests'] = page_obj

    return render(request, 'hoctap/test/testList.html', data)

def searchTestView(request):
    if "notification" in request.POST:
        notification = Notification.objects.get(id=int(request.POST['notification']))
        direct_post = str(notification.link)
        notification.delete()
        HttpResponseRedirect(direct_post)
    data = GetSideContentData(request)
    data['is_searching'] = False

    if (request.method == 'GET') and ('title' in request.GET):
        if (request.GET['username'] != "") and (request.GET['username'] in User.objects.all()):
            data['is_searching'] = True
            data['tests'] = test.objects.filter(author=User.objects.get(username=request.GET['username']), title__icontains = request.GET['title'], is_verify=True, is_publish=True) | test.objects.filter(author=User.objects.get(username=request.GET['username']), test_id__contains = request.POST['title'], is_verify=True, is_publish=True)    
        else:
            data['is_searching'] = True
            data['tests'] = test.objects.filter(title__icontains = request.GET['title'], is_verify=True, is_publish=True) | test.objects.filter(test_id__contains = request.GET['title'], is_verify=True, is_publish=True)
        data['isUserinDB'] = request.GET['username'] in User.objects.all()
        data['Userinclude'] = request.GET['username']

    return render(request, 'hoctap/test/SearchTest.html', data)

@login_required(login_url='/login')
def TestDetailView(request, test_id):
    # xử lí làm bài kiểm tra
    if "notification" in request.POST:
        notification = Notification.objects.get(id=int(request.POST['notification']))
        direct_post = str(notification.link)
        notification.delete()
        HttpResponseRedirect(direct_post)
    data = GetSideContentData(request)
    data['is_finished'] = False
    baiviet = test.objects.get(test_id=test_id)
    baiviet.content = md.markdown(baiviet.content).replace('<img', "<img class='content-img'")
    data['test'] = baiviet
    if ((baiviet.is_verify == False) or (baiviet.is_publish == False)) and (str(baiviet.author) != str(request.user.username)):
        return HttpResponseRedirect('/')

    if (request.method == 'POST'):
        if ('question1' in request.POST):
            data['is_finished'] = True

            correctAns = baiviet.correctAnswers
            UserAns = {}
            keys = request.POST.keys()
            for key in keys:
                if key.find('question') != -1:
                    UserAns[key] = request.POST[key]
            # Chấm Điểm
            correctCount = 0
            keys = baiviet.correctAnswers.keys()
            wrongAns = {}
            i = 1
            for key in keys:
                if correctAns[key] == UserAns[key]:
                    correctCount+=1
                else:
                    wrongAns[str(i)] = f'Câu hỏi <b>{i}</b>:\nĐáp án bạn chọn: <b>{UserAns[key]}</b>\nĐáp án đúng: <b>{correctAns[key]}</b>'
                i+=1
            
            #add user to data
            if not ( str(request.user.username) in baiviet.userJoined ):
                baiviet.userJoined[str(request.user.username)] = correctCount
                baiviet.save()
                data['message'] = f'Kết quả của bạn đã được lưu vào dữ liệu!'
            else:
                data['message'] = f'Kết quả của bạn không được lưu vào dữ liệu (Bạn đã làm bài thi này vào thời gian trước)!'

            data['correctCount'] = correctCount
            data['wrongAnswers'] = wrongAns.values()

    return render(request, 'hoctap/test/testDetail.html', data)


@login_required(login_url='/login')
def createNewTestPageView(request):
    form = CreateTestForm()
    data={}
    data['num_of_questions'] = '0'
    data['is_success'] = False
    data['form'] = form
    if request.method == 'POST':
        if 'num_of_questions' in request.POST:
            data['num_of_questions'] = request.POST['num_of_questions']
            if (data['num_of_questions'].isdigit()):
                data['num_of_questions'] = int(data['num_of_questions'])
                if (data['num_of_questions'] >= 100):
                    data['num_of_questions'] = '0'
                else:
                    temp = []
                    for i in range(data['num_of_questions']):
                        temp.append(i+1)
                    data['idListQuestion'] = temp
            else:
                data['num_of_questions'] = '0'
        else:
            form = CreateTestForm(request.POST)
            if form.is_valid():
                test_id = request.POST['title'] + '_' + str(test.objects.all().count() + 1)
                test_id = test_id.replace('  ',' ').replace(' ', '_').lower()
                test_id = re.sub(r'\W', '', test_id)
                test_id = unidecode(test_id)
                data['is_success'] = True

                # get right ans
                correct_ans = {}
                keys = request.POST.keys()
                for key in keys:
                    if key.find('question') != -1:
                        correct_ans[key] = request.POST[key]

                test.objects.create(
                    test_id = test_id,
                    title = request.POST['title'],
                    content = request.POST['content'],
                    author = request.user,
                    NumberOfQuestions = len(correct_ans),
                    correctAnswers = correct_ans
                )

    return render(request, 'hoctap/test/createNewTest.html', data)
    
@login_required(login_url='/login')
def TestTopScoreView(request, test_id):
    if "notification" in request.POST:
        notification = Notification.objects.get(id=int(request.POST['notification']))
        direct_post = str(notification.link)
        notification.delete()
        HttpResponseRedirect(direct_post)
    data = GetSideContentData(request)
    baiviet = test.objects.get(test_id=test_id)
    topscore = sorted(baiviet.userJoined.items(),reverse=True, key=lambda x:x[1])

    for i in range(len(topscore)):
        topscore[i] += tuple(f"{i+1}")

    paginator = Paginator(topscore, 50)
    try:
        page_number = request.GET['page']
    except:
        page_number = 1
    page_obj = paginator.get_page(page_number)

    data['test'] = baiviet
    data['topScore'] = page_obj

    return render(request, 'hoctap/test/topscore.html', data)