from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from blogs.models import Blog
import json
from datetime import datetime
from django.core.cache import cache
import hashlib
from .RedisClient import RedisClient
import pickle
# Create your views here.


blogs = {
    1 : {
		"id": 1,
		"title": "bbcchidsbc",
		"content": "bcbb",
		"author": "nnn",
		"created_at": "2023-04-12 10:02:53+00:00",
		"updated_at": "2023-04-12 10:02:55+00:00"
	},
    2 : {
		"id": 2,
		"title": "bbcchidsbc",
		"content": "bcbb",
		"author": "nnn",
		"created_at": "2023-04-12 10:02:53+00:00",
		"updated_at": "2023-04-12 10:02:55+00:00"
	},
    3 : {
		"id": 3,
		"title": "bbcchidsbc",
		"content": "bcbb",
		"author": "nnn",
		"created_at": "2023-04-12 10:02:53+00:00",
		"updated_at": "2023-04-12 10:02:55+00:00"
	},
    4 : {
		"id": 4,
		"title": "bbcchidsbc",
		"content": "bcbb",
		"author": "nnn",
		"created_at": "2023-04-12 10:02:53+00:00",
		"updated_at": "2023-04-12 10:02:55+00:00"
	},
    5 : {
		"id": 5,
		"title": "bbcchidsbc",
		"content": "bcbb",
		"author": "nnn",
		"created_at": "2023-04-12 10:02:53+00:00",
		"updated_at": "2023-04-12 10:02:55+00:00"
	},
}

def get_blogs(request : HttpRequest):
    
    # blogs = Blog.objects.all().values()
    # for blog in blogs:
    #     blog['created_at'] = str(blog['created_at'])
    #     blog['updated_at'] = str(blog['updated_at'])
    tmp = []
    for key in blogs.keys():
        tmp.append(blogs[key])
    reponse = HttpResponse(json.dumps(list(tmp)), content_type = 'application/json')
    return reponse


def get_blog(request : HttpRequest):

    blog_id = request.GET.get('id')
    tmp = [blogs[int(blog_id)]]

    # blogs = Blog.objects.filter(id = blog_id).values()

    hexahash = hashlib.md5(str(blog_id).encode()).hexdigest()
    
    if hexahash in cache:
        print(f'Response from cache for {blog_id}')
        reponse = HttpResponse(json.dumps(pickle.loads(cache.get(hexahash))), content_type = 'application/json')
        return reponse
    
    # if(RedisClient.is_cached(hexahash)):
    #     print(RedisClient.get_cache(hexahash))
    #     data = pickle.loads((RedisClient.get_cache(hexahash)))
    #     response = HttpResponse(json.dumps(data), content_type = 'application/json')
    #     # response = HttpResponse([json.loads(RedisClient.get_cache(hexahash))], content_type = 'application/json')
    #     return response
    
    # for blog in blogs:
    #     blog['created_at'] = str(blog['created_at'])
    #     blog['updated_at'] = str(blog['updated_at'])

    reponse = HttpResponse(json.dumps(list(tmp)), content_type = 'application/json')
    # pikl = pickle.dumps(list(blogs), protocol=0)
    pikl = pickle.dumps(list(tmp), protocol=0)
    print(f"Caching the repsonse for id = {blog_id}")
    cache.set(hexahash, pikl)
    # RedisClient.cache(hexahash, pikl)
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
