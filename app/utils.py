import json
import socket
import logging
import threading

from django.shortcuts import HttpResponse
from CIBot.settings import QASNAKE_HOST, QASNAKE_PORT
from app.models import *

logger = logging.getLogger("django")

# 服务工具包 Utils
#   Aux functions for views.py
#


# Section A 业务计算
def qa_dispatcher(data):
    quest = data.get('question')
    if not quest:
        return ''

    # Save Question
    try:
        u = User.objects.get(id=data.get('uid'))
        q = Question.objects.create(user=u, content=quest)
    except:
        q = Question.objects.create(content=quest)  # for anonymous
    # q.keywords.add()
    # q.save()
    logger.info('[Q] new quest, qid=%d', q.id)

    # dispatch SE
    # TODO: try to ASYNC this part!!
    # t = threading.Thread(target=qa_snake, args=(data.get('question'),))
    # t.setDaemon(True)
    # t.start()
    resp = qa_snake(data.get('question'))
    if resp:
        return resp

    # dispatch local-DB

    # dispatch CI

    return '<No ans in QA-Snake>'


def qa_snake(kw):
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((QASNAKE_HOST, QASNAKE_PORT))
        client.settimeout(30)
        client.send(kw.encode('utf8'))
        ans = client.recv(4096).decode('utf8')
        logger.info('[QA-Snake] %s...' % ans[:30])
        return ans
    except:
        return None


# Section B 语法糖 Wrapper
def response_write(jsonData):
    response = HttpResponse(json.dumps(jsonData, ensure_ascii=False))
    return response


def json_load(byteData):
    try:
        strData = isinstance(byteData, bytes) and byteData.decode('utf8') or byteData
        # logger.info('Raw Data: %s' % strData)
        jsonData = json.loads(strData, encoding='utf8', parse_int=int, parse_float=float)
        logger.info('Received Json Data: %s' % jsonData)
        return jsonData
    except :
        raise Exception('Bad Json Data')


# Section C 错误码 Error Code
def die(codeno):
    ERRMSG = {
        200: 'Done',
        400: 'Malformatted Request',
        401: 'Not Authorized',
        403: 'Missing Parameter or TypeError',
        404: 'Resource Not Found',
        405: 'Method Not Allowed',
        500: 'Server Internal Error',
        000: 'Not Implemented Yet',
    }

    return {'errorno': codeno, 'errormsg': ERRMSG.get(codeno) or 'Unkown Error'}


# Section D 默认值配置 Defaults
