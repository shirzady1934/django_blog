from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from .models import Post, Token, UserProfile, Comment
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.contrib.auth.hashers import check_password, make_password
from django.utils import timezone
@csrf_protect
def submit_post(request):
	if request.method == "POST":
		#p_token = request.POST['token'] 
		if 'member_id' in request.session:
			this_user = get_object_or_404(User, pk=request.session['member_id'])
			text = request.POST['message']
			title = request.POST['title']
			post = Post.objects.create(author = this_user, text = text, title = title)
			return HttpResponseRedirect('/blog/home', "the post submited with id %d" % post.id)
		else:
			HttpResponse("you should first login")
@csrf_protect
def delete_post(request):
    if request.method == "POST":
    	if 'member_id' in request.session:
	        this_user = get_object_or_404(User, pk=request.session['member_id'])
	        p_id = request.POST['post_id']
	        this_post = get_object_or_404(Post, id=p_id)
	        if this_post.author.username == this_user.username:
	            this_post.delete()
	            return HttpResponseRedirect('/blog/home', "the post have been deleted sucssesfuly")
@csrf_exempt
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
        return Http404("error")
def user_show(request, username):
    try:
        me = User.objects.get(pk=request.session['member_id'])
        log_status = True
    except:
        log_status = False
    this_user = User.objects.get(username=username)
    post_list = [ post for post in Post.objects.filter(author = this_user).order_by('-created_date')]
    this_profile = get_object_or_404(UserProfile, user=this_user)
    is_owner = True if me != None and me.username == this_user.username else False
    context = { 'post_list' : post_list, 'log_status' : log_status, 'profile' : this_profile, 'is_owner' : is_owner}
    return render(request, 'blog/user_profile.html', context)

def new_post(request):
    try:
        me = User.objects.get(pk=request.session['member_id']).username
        log_status = True
    except:
        me = None
        log_status = False
    news = Post.objects.order_by('-created_date')
    context = { 'post_list' : news, 'log_status' : log_status, 'username' : me}
    return render(request, 'blog/news.html', context)
def user_post(request, username, id):
    try:
        me = User.objects.get(pk=request.session['member_id'])
        log_status = True
    except:
        me = None
        log_status = False

    this_user = get_object_or_404(User, username=username)
    this_post = get_object_or_404(Post, id=id)
    is_owner = True if me != None and me.username == this_post.author.username else False
    comments = Comment.objects.filter(post=this_post)
    comments = comments if len(comments) != 0 else None
    if this_post.author.username == this_user.username:
        context = { 'post' : this_post, 'comments': comments,'log_status' : log_status, 'is_owner' : is_owner}
        return render(request, 'blog/post_show.html', context)
    else:
        return Http404("Page not found")
def submit_comment(request):
    if request.method == 'POST':
        if 'member_id' in request.session:
            if 'text' in request.POST and 'post_id' in  request.POST:
                this_post = get_object_or_404(Post, pk=request.POST['post_id'])
                text = request.POST['text']
                this_user = get_object_or_404(User, id=request.session['member_id'])
                Comment.objects.create(text=text, post=this_post, author=this_user)
                return HttpResponseRedirect('/blog/profile/%s/%d' % (this_post.author, this_post.id))
            else:
                return HttpResponse("please fill all forms!")
        else:
            return HttpResponse("please first login!")
    else:
        return HttpResponse("hello :)")
def check_login(user, passwd):
	try:
		this_user = User.objects.get(username=user)
	except:
		return False
	if check_password(passwd, this_user.password):
		return True
	return False

@csrf_protect
def login(request):
    if request.method == "POST":
        if 'username' in request.POST and 'password' in request.POST:
            user = request.POST['username']
            passwd = request.POST['password']
            if check_login(user, passwd):
                this_user = User.objects.get(username=user)
                request.session['member_id'] = this_user.id
                return HttpResponseRedirect('/blog', "you loged in succesfully")
            else:
                return HttpResponse("username or pass dosent match")
    elif 'member_id' in request.session:
    	user = User.objects.get(id=request.session['member_id'])
    	return HttpResponseRedirect('/blog/home', "You're loged in as %s " % user)
    else:
        return render(request, 'blog/login.html')
def logout(request):
    request.session.flush()
    return HttpResponseRedirect('/blog/login', "You logged out")
def home(request):
	if 'member_id' in request.session:
		this_user = User.objects.get(pk=request.session['member_id'])
		this_profile = get_object_or_404(UserProfile, user=this_user)
		posts = Post.objects.filter(author=this_user).order_by('-created_date')
		empty = True if len(posts) is 0 else False
		context={'profile' : this_profile, 'post_list' : posts, 'isempty' : empty}
		return render(request, 'blog/home.html', context)
	else:
		return render(request, 'blog/login.html')
@csrf_protect
def sign_up(request):
    if 'member_id' in request.session:
        return HttpResponseRedirect('/blog/home')
    elif request.method == 'POST':
        if 'username' in request.POST and 'password' in request.POST and 'name' in request.POST and 'age' in request.POST and 'location' in request.POST:
            try:
                User.objects.get(username=request.POST['username'].lower())
                user_stat = False
            except:
                user_stat = True
            if user_stat is False:
                return HttpResponse("this user name has been taken")
            username = request.POST['username'].lower()
            password = make_password(request.POST['password'])
            name = request.POST['name']
            try:
                age = int(request.POST['age'])
            except:
                age = 0
            location = request.POST['location']
            this_user = User.objects.create(username=username, password=password)
            this_profile = UserProfile.objects.create(user=this_user, name=name, age=age, location=location)
            request.session['member_id'] = this_user.id
            return HttpResponseRedirect('/blog/home', "the user created succesfully")
        else:
            HttpResponse("please fill up all forms")
    else:
        return render(request, 'blog/signup.html')
