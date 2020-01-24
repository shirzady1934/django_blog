from django.http import HttpResponse, HttpResponseRedirect
def blog(request):
    return HttpResponseRedirect('/blog')
