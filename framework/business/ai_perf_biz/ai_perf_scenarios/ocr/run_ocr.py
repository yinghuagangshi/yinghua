from framework.core.concurrent.runMultiProcess import StartMultiRequest

def run_ocr():
    args = {}  # 参数字典
    request_type = "OCR"

    args["process_count"] = 1  # 进程数，-1采用默认CPU内核数
    args["thread_count"] = 1  # 每个进程内部创建线程数
    args["repeat_count"] = 1  # 一个线程内部重复请求次数
    args["is_async"] = True  # http异步请求还是同步请求

    if request_type == "OCR":
        args["url"] = "http://localhost:5000/ocr/carplate"
        args["image_files"] = r"E:\自动化\auto_2025\yinghua\data\ai_perf\images"  # 目录或单张图片
        args["label_file"] = r"E:\自动化\auto_2025\yinghua\data\ai_perf\labels\labels.txt"
    else:
        args["url"] = "http://localhost:5000/sso/oauth/token"
        args["appkey"] = "67b05ab60d4e4e329bcc5db895e9e620"
        args["appsecret"] = "0630402006ba4ac6aaa003b8abb6e9c3"

    StartMultiRequest(request_type, **args)


if __name__ == '__main__':  # ⚠️ 必须添加这一行！
    run_ocr()