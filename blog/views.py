from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from .models import Post, Token, UserProfile, Comment, Notification
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.contrib.auth.hashers import check_password, make_password
from django.utils import timezone
from django.contrib import auth
import re

def check_login(user, passwd):
    this_user = User.objects.filter(username=user)
    if not this_user.exists():
        return False
    if check_password(passwd, this_user[0].password):
        return True
    return False
def check_list(words, the_list):
    for word in words:
        if not word in the_list:
            return False
    return True

@csrf_protect
def submit_post(request):
    if request.method == "POST":
        #p_token = request.POST['token']
        if request.user.is_authenticated:
            this_user = get_object_or_404(User, pk=request.user.id)
            text = request.POST['message']
            title = request.POST['title']
            post = Post.objects.create(author = this_user, text = text, title = title)
            return HttpResponseRedirect('/blog/home', "the post submited with id %d" % post.id)
        else:
            return HttpResponse("you should first signin")
@csrf_protect
def delete_post(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            this_user = get_object_or_404(User, pk=request.user.id)
            p_id = request.POST['post_id']
            this_post = get_object_or_404(Post, id=p_id)
            if this_post.author.username == this_user.username:
                this_post.delete()
                return HttpResponseRedirect('/blog/home', "the post have been deleted sucssesfuly")
'''@csrf_exempt
def publish(request):
    if request.method == "POST":
        p_token = request.POST['token']
        p_id = request.POST['id']
        this_user = get_object_or_404(Token, token = p_token).user
        this_post = get_object_or_404(Post, id = p_id)
        if this_user.username == this_post.author.username:
            if this_post.published_date == None:
                this_post.publish()
                this_post.save()
                return HttpResponse("post have been published")
            else:
                return HttpResponse("Post have been published before!")
        return Http404("error")'''
def profile(request, username):
    this_user = get_object_or_404(User, username=username)
    posts = Post.objects.filter(author=this_user).order_by('-created_date')
    this_profile = get_object_or_404(UserProfile, user=this_user)
    context = { 'posts' : posts, 'profile' : this_profile}
    return render(request, 'blog/profile.html', context)

def timeline(request):
    posts = Post.objects.order_by('-created_date')
    context = { 'posts' : posts}
    return render(request, 'blog/timeline.html', context)
def show_post(request, username, id):
    this_user = get_object_or_404(User, username=username)
    this_post = get_object_or_404(Post, id=id)
    comments = Comment.objects.filter(post=this_post).order_by('-created_date')
    comments = comments if len(comments) != 0 else None
    if this_post.author.username == this_user.username:
        context = { 'post' : this_post, 'comments': comments}
        return render(request, 'blog/show_post.html', context)
    else:
        return Http404("Page not found")
def submit_comment(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            if check_list(['text','post_id'], request.POST):
                this_post = get_object_or_404(Post, pk=request.POST['post_id'])
                text = request.POST['text']
                this_user = get_object_or_404(User, pk=request.user.id)
                this_comment = Comment.objects.create(text=text, post=this_post, author=this_user)
                if this_post.author != this_user:
                    Notification.objects.create(user=this_post.author, comment=this_comment, type='comment')
                mentions = set(re.findall('@\w+', text))
                if len(mentions) > 0:
                    for mention in mentions:
                        try:
                            mention_user = User.objects.get(username=mention[1:])
                            Notification.objects.create(user=mention_user, comment=this_comment, type='mention')
                        except:
                            pass
                return HttpResponseRedirect('/blog/profile/%s/%d' % (this_post.author, this_post.id))
            else:
                return HttpResponse("please fill all forms!")
        else:
            return HttpResponse("please first signin!")
    else:
        return HttpResponse("hello :)")
@csrf_protect
def delete_comment(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            this_user = get_object_or_404(User, pk=request.user.id)
            comment_id = request.POST['comment_id']
            this_comment = get_object_or_404(Comment, id=comment_id)
            if this_comment.author.username == this_user.username:
                url = '/blog/profile/%s/%s' % (this_comment.post.author, this_comment.post.id)
                this_comment.delete()
                return HttpResponseRedirect(url, "the post have been deleted sucssesfuly")
            else:
                return HttpResponse("you are not owner of this comment!")
        else:
            return HttpResponseRedirect("/blog/signin")
@csrf_protect
def signin(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/blog/home')
    elif request.method == "POST":
        if 'username' in request.POST and 'password' in request.POST:
            user = request.POST['username']
            passwd = request.POST['password']
            if check_login(user, passwd):
                this_user = User.objects.get(username=user)
                #request.session['member_id'] = this_user.id
                auth.login(request, this_user)
                return HttpResponseRedirect('/blog', "you loged in succesfully")
            else:
                goback = "<a href=\"/blog/signin\"> <b> username or password dosen\'t match click for go back </b> </a>"
                return HttpResponse(goback)
    else:
        return render(request, 'blog/signin.html')
def signout(request):
    request.session.flush()
    return HttpResponseRedirect('/blog/signin', "You logged out")
def home(request):
    if request.user.is_authenticated:
        this_user = User.objects.get(pk=request.user.id)
        this_profile = get_object_or_404(UserProfile, user=this_user)
        posts = Post.objects.filter(author=this_user).order_by('-created_date')
        empty = True if len(posts) is 0 else False
        context={'profile' : this_profile, 'posts' : posts, 'isempty' : empty}
        return render(request, 'blog/home.html', context)
    else:
        return render(request, 'blog/signin.html')
@csrf_protect
def sign_up(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/blog/home')
    elif request.method == 'POST':
        if check_list(['username','password','email','name','age','location'], request.POST):
            if User.objects.filter(username=request.POST['username'].lower()).exists():
                return HttpResponse("this user name has been taken!")
            if User.objects.filter(email=request.POST['email']).exists():
                return HttpResponse("this email currently is in use!")
            username = request.POST['username'].lower()
            password = make_password(request.POST['password'])
            name = request.POST['name']
            age = request.POST['age']
            location = request.POST['location']
            this_user = User.objects.create(username=username, password=password)
            this_profile = UserProfile.objects.create(user=this_user, name=name, age=age, location=location)
            auth.login(request, this_user)
            return HttpResponseRedirect('/blog/home', "the user created succesfully")
        else:
            HttpResponse("please fill up all forms")
    else:
        return render(request, 'blog/signup.html')
def notifications(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/blog/signin/')
    this_user = User.objects.get(pk=request.user.id)
    this_notif = Notification.objects.filter(user=this_user).order_by('-created_date')[:20]
    have_notif = False if len(this_notif) == 0 else True
    context = {'notifications' : this_notif, 'have_notif' : have_notif}
    return render(request, 'blog/notifications.html', context)

@csrf_protect
def edit_post(request, pk):
    if request.method == 'GET':
        if request.user.is_authenticated:
            post = get_object_or_404(Post, pk=pk)
            if post.author.username == request.user.username:
                context = { 'post' : post }
                return render(request, 'blog/edit_post.html', context)
            else:
                return HttpResponse("ERROR 400 BAD_REQUEST")
        else:
            return HttpResponseRedirect('/blog/signin')

    elif request.method == 'POST':
        if request.user.is_authenticated:
            post = get_object_or_404(Post, pk=pk)
            if request.user.username == post.author.username:
                if check_list(['title', 'text'], request.Post):
                    post.title = request.POST['title']
                    post.text = request.POST['text']
                    post.save()
                    return HttpResponseRedirect('/blog/profile/%s/%s' % (post.author.username, post.id))
                else:
                    return HttpResponse("Please fill up the form!")
            else:
                return HttpResponse('ERROR 400 BAD_REQUEST')
        else:
            return HttpResponseRedirect('/blog/signin')



def mss(request):
    if request.user.is_authenticated:
        return HttpResponse(request.user.id)