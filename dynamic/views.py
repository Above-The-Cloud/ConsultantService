import json
import traceback

from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from dynamic.models import Dynamic, Comment, Reply
from user.models import User


@csrf_exempt
def create(request):
    res = {'code': 0, 'msg': 'success', 'data': {}}
    if not {'user_id','content'}.issubset(request.POST.keys()):
        return HttpResponse(json.dumps({'code': -1, 'msg': 'error-1|unexpected params!', 'data': []}))
    try:
        params = request.POST.dict()
        dis=Dynamic.objects.create(**params)
        res['data']['id']=dis.id
    except Exception as e:
        traceback.print_exc()
        return HttpResponse(json.dumps({'code': -2, 'msg': e, 'data': []}))
    return HttpResponse(json.dumps(res))

@csrf_exempt
def createComment(request):
    res = {'code': 0, 'msg': 'success', 'data': {}}
    if not {'user_id','dynamic_id','content'}.issubset(request.POST.keys()):
        return HttpResponse(json.dumps({'code': -1, 'msg': 'error-1|unexpected params!', 'data': []}))
    try:
        params = request.POST.dict()
        dis=Comment.objects.create(**params)
        res['data']['id']=dis.id
    except Exception as e:
        traceback.print_exc()
        return HttpResponse(json.dumps({'code': -2, 'msg': e, 'data': []}))
    return HttpResponse(json.dumps(res))

@csrf_exempt
def createReply(request):
    res = {'code': 0, 'msg': 'success', 'data': {}}
    if not {'user_id','comment_id','content'}.issubset(request.POST.keys()):
        return HttpResponse(json.dumps({'code': -1, 'msg': 'error-1|unexpected params!', 'data': []}))
    try:
        params = request.POST.dict()
        dis=Reply.objects.create(**params)
        res['data']['id']=dis.id
    except Exception as e:
        traceback.print_exc()
        return HttpResponse(json.dumps({'code': -2, 'msg': e, 'data': []}))
    return HttpResponse(json.dumps(res))


@csrf_exempt
def update(request):
    res = {'code': 0, 'msg': 'success', 'data': []}
    if not {'dynamic_id','update'}.issubset(request.POST.keys()):
        return HttpResponse(json.dumps({'code': -1, 'msg': 'error-1|unexpected params!', 'data': []}))
    try:
        Dynamic.objects.filter(id=request.POST['dynamic_id']).update(**json.loads(request.POST['update']))
    except Exception as e:
        traceback.print_exc()
        return HttpResponse(json.dumps({'code': -2, 'msg': e, 'data': []}))
    return HttpResponse(json.dumps(res))

@csrf_exempt
def delete(request):
    res = {'code': 0, 'msg': 'success', 'data': []}
    if not {'id'}.issubset(request.POST.keys()):
        return HttpResponse(json.dumps({'code': -1, 'msg': 'error-1|unexpected params!', 'data': []}))
    try:
        Dynamic.objects.filter(id=request.POST['id']).update(status=0)
    except Exception as e:
        traceback.print_exc()
        return HttpResponse(json.dumps({'code': -2, 'msg': e, 'data': []}))
    return HttpResponse(json.dumps(res))

@csrf_exempt
def deleteComment(request):
    res = {'code': 0, 'msg': 'success', 'data': []}
    if not {'id'}.issubset(request.POST.keys()):
        return HttpResponse(json.dumps({'code': -1, 'msg': 'error-1|unexpected params!', 'data': []}))
    try:
        Comment.objects.filter(id=request.POST['id']).update(status=0)
    except Exception as e:
        traceback.print_exc()
        return HttpResponse(json.dumps({'code': -2, 'msg': e, 'data': []}))
    return HttpResponse(json.dumps(res))

@csrf_exempt
def deleteReply(request):
    res = {'code': 0, 'msg': 'success', 'data': []}
    if not {'id'}.issubset(request.POST.keys()):
        return HttpResponse(json.dumps({'code': -1, 'msg': 'error-1|unexpected params!', 'data': []}))
    try:
        Reply.objects.filter(id=request.POST['id']).update(status=0)
    except Exception as e:
        traceback.print_exc()
        return HttpResponse(json.dumps({'code': -2, 'msg': e, 'data': []}))
    return HttpResponse(json.dumps(res))

@csrf_exempt
def list(request):
    res = {'code': 0, 'msg': 'success', 'data': {}}
    try:
        params = request.POST.dict()
        page=0
        size=20
        if 'page' in params:
            page=params['page']
            params.pop('page')
        if 'size' in params:
            size=params['size']
            params.pop('size')
        params['status']=1
        res['data']['count']=Dynamic.objects.filter(**params).count()
        res['data']['dynamics']=[]
        qset=Dynamic.objects.filter(**params).order_by('-ctime')[page*size:(page+1)*size]
        dynamics=json.loads(serializers.serialize("json", qset))
        # print(dynamics)
        for dynamic in dynamics:
            data_row=dynamic['fields']
            data_row['dynamic_id']=dynamic['pk']
            data_row['images']=json.loads(data_row['images'])
            try:
                data_row['user_info'] = json.loads(serializers.serialize("json", User.objects.filter(id=dynamic['fields']['user_id'])))[0]['fields']
                data_row['user_info'].pop('password')
                data_row['user_info'].pop('status')
                data_row['user_info'].pop('ctime')
                data_row['user_info'].pop('mtime')
            except:
                print('User %d not exists!'%(dynamic['fields']['user_id']))
                data_row['user_info']={
                    "username": "用户不存在",
                    "phone": "000",
                    "gender": 1,
                    "avatar": "http://consultant.yiwangchunyu.wang/media/system/avatar.jpg"
                }
            data_row['user_info']['user_id']=dynamic['fields']['user_id']
            res['data']['dynamics'].append(data_row)
    except Exception as e:
        traceback.print_exc()
        return HttpResponse(json.dumps({'code': -2, 'msg': e, 'data': []}))
    return HttpResponse(json.dumps(res))

@csrf_exempt
def listComment(request):
    res = {'code': 0, 'msg': 'success', 'data': {}}
    if not {'dynamic_id'}.issubset(request.POST.keys()):
        return HttpResponse(json.dumps({'code': -1, 'msg': 'error-1|unexpected params!', 'data': []}))
    try:
        params = request.POST.dict()
        page=0
        size=20
        if 'page' in params:
            page=params['page']
            params.pop('page')
        if 'size' in params:
            size=params['size']
            params.pop('size')
        params['status']=1
        res['data']['count']=Comment.objects.filter(**params).count()
        res['data']['comments']=[]
        qset=Comment.objects.filter(**params).order_by('-ctime')[page*size:(page+1)*size]
        cmts=json.loads(serializers.serialize("json", qset))
        # print(dynamics)
        for cmt in cmts:
            data_row=cmt['fields']
            data_row['comment_id']=cmt['pk']
            data_row['images']=json.loads(data_row['images'])
            try:
                data_row['user_info'] = \
                json.loads(serializers.serialize("json", User.objects.filter(id=cmt['fields']['user_id'])))[0][
                    'fields']
                data_row['user_info'].pop('password')
                data_row['user_info'].pop('status')
                data_row['user_info'].pop('ctime')
                data_row['user_info'].pop('mtime')
            except:
                print('User %d not exists!' % (cmt['fields']['user_id']))
                data_row['user_info'] = {
                    "username": "用户不存在",
                    "phone": "000",
                    "gender": 1,
                    "avatar": "http://consultant.yiwangchunyu.wang/media/system/avatar.jpg"
                }
            data_row['user_info']['user_id'] = cmt['fields']['user_id']
            res['data']['comments'].append(data_row)
    except Exception as e:
        traceback.print_exc()
        return HttpResponse(json.dumps({'code': -2, 'msg': e, 'data': []}))
    return HttpResponse(json.dumps(res))

@csrf_exempt
def listReply(request):
    res = {'code': 0, 'msg': 'success', 'data': {}}
    if not {'comment_id'}.issubset(request.POST.keys()):
        return HttpResponse(json.dumps({'code': -1, 'msg': 'error-1|unexpected params!', 'data': []}))
    try:
        params = request.POST.dict()
        page=0
        size=20
        if 'page' in params:
            page=params['page']
            params.pop('page')
        if 'size' in params:
            size=params['size']
            params.pop('size')
        params['status']=1
        res['data']['count']=Reply.objects.filter(**params).count()
        res['data']['replys']=[]
        qset=Reply.objects.filter(**params).order_by('-ctime')[page*size:(page+1)*size]
        rpls=json.loads(serializers.serialize("json", qset))
        # print(dynamics)
        for rpl in rpls:
            data_row=rpl['fields']
            data_row['reply_id']=rpl['pk']
            try:
                data_row['user_info'] = \
                json.loads(serializers.serialize("json", User.objects.filter(id=rpl['fields']['user_id'])))[0][
                    'fields']
                data_row['user_info'].pop('password')
                data_row['user_info'].pop('status')
                data_row['user_info'].pop('ctime')
                data_row['user_info'].pop('mtime')
            except:
                print('User %d not exists!' % (rpl['fields']['user_id']))
                data_row['user_info'] = {
                    "username": "用户不存在",
                    "phone": "000",
                    "gender": 1,
                    "avatar": "http://consultant.yiwangchunyu.wang/media/system/avatar.jpg"
                }
            data_row['user_info']['user_id'] = rpl['fields']['user_id']
            res['data']['replys'].append(data_row)
    except Exception as e:
        traceback.print_exc()
        return HttpResponse(json.dumps({'code': -2, 'msg': e, 'data': []}))
    return HttpResponse(json.dumps(res))