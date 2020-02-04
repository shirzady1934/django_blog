from rest_framework import serializers
from blog.models import Post

class PostSerializer(serializers.ModelSerializer):
	author = serializers.SerializerMethodField('get_username')
	class Meta:
		model = Post
		fields = [
		'pk',
		'author',
		'title',
		'text',
		'created_date',
		]
		read_only_fields = ['author', 'created_date']
	def get_username(self, obj):
		return obj.author.username
