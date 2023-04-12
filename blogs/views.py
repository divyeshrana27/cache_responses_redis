from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from blogs.models import Blog
import json
from datetime import datetime
import hashlib
from .RedisClient import RedisClient
import pickle
# Create your views here.

def get_blogs(request : HttpRequest):
    
    blogs = Blog.objects.all().values()
    for blog in blogs:
        blog['created_at'] = str(blog['created_at'])
        blog['updated_at'] = str(blog['updated_at'])

    reponse = HttpResponse(json.dumps(list(blogs)), content_type = 'application/json')
    return reponse


def get_blog(request : HttpRequest):

    blog_id = request.GET.get('id')
    blogs = Blog.objects.filter(id = blog_id).values()

    hexahash = hashlib.md5(str(blogs.query).encode()).hexdigest()
    if(RedisClient.is_cached(hexahash)):
        data = pickle.loads(str.encode(RedisClient.get_cache(hexahash)))
        response = HttpResponse(json.dumps(data), content_type = 'application/json')
        # response = HttpResponse([json.loads(RedisClient.get_cache(hexahash))], content_type = 'application/json')
        return response
    
    for blog in blogs:
        blog['created_at'] = str(blog['created_at'])
        blog['updated_at'] = str(blog['updated_at'])

    reponse = HttpResponse(json.dumps(list(blogs)), content_type = 'application/json')
    pikl = pickle.dumps(list(blogs), protocol=0)
    RedisClient.cache(hexahash, pikl)
    # RedisClient.cache(hexahash, str(json.dumps(list(blogs))))

    return reponse



def create_blog(request : HttpRequest):
    body = json.loads(request.body.decode('utf-8'))

    blog = Blog(
        id = body['id'],
        title = body['title'],
        content = body['content'],
        author = body['author'],
        created_at = (body['created_at']),
        updated_at = (body['updated_at'])
    )
    blog.save()
    response = HttpResponse('okay', content_type = 'application/json')
    return response
