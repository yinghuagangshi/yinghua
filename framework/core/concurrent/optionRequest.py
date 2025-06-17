"""
author: slg
"""

from framework.business.ai_perf_biz.ai_perf_api.OCR import ocrThread
from framework.business.ai_perf_biz.ai_perf_api.OCR import async_ocrThread
from framework.business.ai_perf_biz.ai_perf_api.OAUTH import oauthThread
from framework.business.ai_perf_biz.ai_perf_api.OAUTH import async_oauthThread

def choice(request_type, out_queue, condition, **args):
    if request_type == "OCR":
        return request_ocr_id(out_queue, condition, **args)
    elif request_type == "OAUTH":
        return request_auth(out_queue, condition, **args)
    else:
        return None

# 请求ocr识别
def request_ocr_id(out_queue, condition, **args):
    if args["is_async"]:
        # 异步请求
        myThread = async_ocrThread.ocrThread(out_queue, args["repeat_count"])
    else:
        # 同步请求
        myThread = ocrThread.ocrThread(out_queue, args["repeat_count"])

    myThread.set_url(args["url"])
    myThread.loadimagefiles(args["image_files"])
    myThread.set_condition(condition)
    return myThread

# 请求身份证
def request_auth(out_queue, condition, **args):
    if args["is_async"]:
        # 异步请求
        myThread = async_oauthThread.authThread(out_queue, args["repeat_count"])
        HEADERS = {'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8'}
        myThread.set_json_headers(HEADERS)
    else:
        # 同步请求
        myThread = oauthThread.authThread(out_queue, args["repeat_count"])

    myThread.set_account(args["appkey"], args["appsecret"])
    myThread.set_url(args["url"])
    myThread.set_condition(condition)
    return myThread