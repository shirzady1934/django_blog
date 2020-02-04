from blog.api.serializers import PostSerializer
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from blog.models import Post

@api_view(['GET'])
@permission_classes([])
def all_post(request):
	queryset = Post.objects.all()
	serializer = PostSerializer(queryset, many=True)
	return Response(serializer.data)

@api_view(['GET'])
@permission_classes([])
def detail_post(request, pk):
	try:
		post = Post.objects.get(pk=pk)
	except Post.DoesNotExist:
		return Response({'status': "Not found!"})

	serializer = PostSerializer(post)
	return Response(serializer.data)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_post(request, pk):
	try:
		post = Post.objects.get(pk=pk)
	except Post.DoesNotExist:
		return Response({'status': 'Not found!'})
	user = request.user
	if post.author != user:
		return Response({'response' : 'You dont have permission to edit this post!'})
	serializer = PostSerializer(post, data=request.data)
	context = {}
	if serializer.is_valid():
		serializer.save()
		context= serializer.data
		context['success'] = 'update successful!'
		return Response(context) 
	return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_post(request, pk):
	try:
		post = Post.objects.get(pk=pk)
	except Post.DoesNotExist:
		return Response({'status': "Not found!"})
	user = request.user
	if post.author != user:
		return Response({'success' : 'Error you dont have permission to delete this post!'})
	post.delete()
	return Response({'success': 'delete was successful!'})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_post(request):
	user = request.user
	post = Post(author=user)
	serializer = PostSerializer(post, data=request.data)
	if serializer.is_valid():
		serializer.save()
		return Response(serializer.data) 
	return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
