from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from .models import Post, Token
from django.contrib.auth.models import User
from django.utils import timezone
def post_list(request, post_id):
    if request.method == "GET":
        try:
            result_post = Post.objects.get(pk = post_id)
            if not result_post.published_date == None:
                published_status = "published on %s" % result_post.published_date.strftime('%Y-%m-%d %H:%M')
            else:
                published_status = "Not Published"
        except Post.DoesNotExist:
            raise Http404("Post not found")
    context = { 'id' : post_id, 'title' : result_post.title, 'text' : result_post.text, 'creation_date' : result_post.created_date, 'author' : result_post.author, 'published_status' : published_status}
    return render(request, 'blog/post_show.html', context)
@csrf_exempt
def submit_post(request):
    if request.method == "POST":
        p_token = request.POST['token'] 
        this_user = get_object_or_404(Token, token = p_token).user
        text = request.POST['text']
        title = request.POST['title']
        post = Post.objects.create(author = this_user, text = text, title = title)
        return HttpResponse("the post submited with id %d" % post.id)
@csrf_exempt
def delete_post(request):
    if request.method == "POST":
        p_token = request.POST['token']
        this_user = get_object_or_404(Token, token=p_token).user
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
    post_list = [ post for post in Post.objects.filter(author = this_user).order_by('-published_date')]
    context = { 'post_list' : post_list }
    return render(request, 'blog/user_profile.html', context)
def new_post(request):
    news = [ post for post in Post.objects.order_by('-published_date')[:5] ]
    context = { 'post_list' : news }
    return render(request, 'blog/news.html', context)
def user_post(request, p_id, p_user):
    this_user = get_object_or_404(User, username = p_user)
    this_post = get_object_or_404(Post, id = p_id)
    if this_post.author.username == this_user.username:
            if not this_post.published_date == None:
                published_status = "published on %s" % this_post.published_date.strftime('%Y-%m-%d %H:%M')
            else:
                published_status = "Not Published"
            context = { 'id' : this_post.id, 'title' : this_post.title, 'text' : this_post.text, 'creation_date' : this_post.created_date, 'author' : this_post.author, 'published_status' : published_status }
            return render(request, 'blog/post_show.html', context)
    else:
        return Http404("Page not found")
def default(request):
    return HttpResponse("Hey wellcome to blog section")
