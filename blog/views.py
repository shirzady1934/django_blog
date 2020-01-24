from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from .models import Post, Token, UserProfile
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.contrib.auth.hashers import check_password
from django.utils import timezone
def post_show(request, post_id):
    if request.method == "GET":
    	result_post = get_object_or_404(Post, pk=post_id)
    context = { 'id' : post_id, 'post' : result_post} #'title' : result_post.title, 'text' : result_post.text, 'creation_date' : result_post.created_date, 'author' : result_post.author}
    return render(request, 'blog/post_show.html', context)
@csrf_protect
def submit_post(request):
	if request.method == "POST":
		#p_token = request.POST['token'] 
		if 'member_id' in request.session:
			this_user = get_object_or_404(User, pk=request.session['member_id'])
			text = request.POST['message']
			title = request.POST['title']
			post = Post.objects.create(author = this_user, text = text, title = title)
			return HttpResponse("the post submited with id %d" % post.id)
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
	            return HttpResponse("the post have been deleted sucssesfuly")
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
def user(request, username):
    this_user = User.objects.get(username = username)
    post_list = [ post for post in Post.objects.filter(author = this_user).order_by('-created_date')]
    context = { 'post_list' : post_list }
    return render(request, 'blog/user_profile.html', context)
def new_post(request):
	try:
		User.objects.get(pk=request.session['member_id'])
		log_status = True
	except:
		log_status = False
	news = Post.objects.order_by('-created_date')[:10]
	context = { 'post_list' : news, 'log_status' : log_status}
	return render(request, 'blog/news.html', context)
def user_post(request, p_id, p_user):
    this_user = get_object_or_404(User, username = p_user)
    this_post = get_object_or_404(Post, id = p_id)
    if this_post.author.username == this_user.username:
            context = { 'id' : this_post.id, 'title' : this_post.title, 'text' : this_post.text, 'creation_date' : this_post.created_date, 'author' : this_post.author }
            return render(request, 'blog/post_show.html', context)
    else:
        return Http404("Page not found")
def default(request):
    return HttpResponse("Hey wellcome to blog section")
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
                request.session ['member_id'] = this_user.id
                return HttpResponse("you loged in succesfully")
            else:
                return HttpResponse("username or pass dosent match")
    elif 'member_id' in request.session:
    	user = User.objects.get(id=request.session['member_id'])
    	return HttpResponse("You're loged in as %s " % user)
    else:
        return render(request, 'blog/login.html')
def logout(request):
    request.session.flush()
    return HttpResponse("You logged out")
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