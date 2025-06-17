import re

from flask import Flask, request, jsonify
import time
import random
import threading
import os

app = Flask(__name__)

# 模拟配置
MOCK_RESPONSE_DELAY = (0.1, 0.5)  # 最小和最大延迟时间(秒)
MOCK_FAILURE_RATE = 0.1  # 10%的失败率
MOCK_TOKEN = "mock_token_1234567890"

# 车牌识别模拟数据
CAR_PLATE_DATA = {
    "car_001.jpg": {
        "boxes": [[100, 200, 300, 250]],
        "plate_numbers": ["京A12345"]
    },
    "car_002.jpg": {
        "boxes": [[150, 180, 320, 220]],
        "plate_numbers": ["沪B98765"]
    },
    "car_003.jpg": {
        "boxes": [[80, 150, 280, 200]],
        "plate_numbers": ["粤Z54321"]
    }
}

# 共享计数器(用于统计请求量)
request_counter = 0
counter_lock = threading.Lock()


@app.route('/ocr/idcard', methods=['GET', 'POST'])
def mock_ocr():
    global request_counter

    # 模拟处理延迟
    delay = random.uniform(*MOCK_RESPONSE_DELAY)
    time.sleep(delay)

    # 随机模拟失败
    if random.random() < MOCK_FAILURE_RATE:
        return jsonify({"error": "Internal server error"}), 500

    # 线程安全的计数器递增
    with counter_lock:
        request_counter += 1

    # 返回模拟OCR结果
    return jsonify({
        "success": True,
        "result": {
            "content": {
                "result": True,
                "data": {
            "name": "张三",
            "gender": "男",
            "nation": "汉",
            "birth": "1990-01-01",
            "address": "北京市海淀区",
            "id_number": "110105199001011234",
            "request_count": request_counter
        }
            }
        }
    })


@app.route('/ocr/carplate', methods=['GET', 'POST'])
def mock_carplate_ocr():
    global request_counter

    # 模拟处理延迟
    delay = random.uniform(*MOCK_RESPONSE_DELAY)
    time.sleep(delay)

    # 随机模拟失败
    if random.random() < MOCK_FAILURE_RATE:
        return jsonify({"error": "Internal server error"}), 500

    # 线程安全的计数器递增
    with counter_lock:
        request_counter += 1

    # 适配两种请求格式：
    # 1. 客户端async_ocr.py的JSON格式（含base64图片）
    # 2. 传统multipart表单格式
    if request.is_json:
        # 处理async_ocr.py的请求格式
        data = request.get_json()

        # 模拟解码base64图片（实际mock不需要真正解码）
        img_base64 = data.get('img', '')
        if not img_base64:
            return jsonify({"error": "Empty image data"}), 400

        image_file = data.get('imgID', 'unknown.jpg')
        imageID = os.path.basename(image_file)

        print(f"imgid: {imageID}")
    else:
        # 处理传统表单上传
        if 'image' not in request.files:
            return jsonify({"error": "No image provided"}), 400

        image_file = request.files['imageID']
        imageID = os.path.basename(image_file)


    # 查找匹配的车牌数据
    if imageID in CAR_PLATE_DATA:
        data = CAR_PLATE_DATA[imageID]
        response = {
                    "imageID": f"{imageID}",
                    "detected_boxes": data["boxes"],
                    "plate_numbers": data["plate_numbers"],

        }
    else:
        response = {
                    "imageID": f"{imageID}",
                    "detected_boxes": [],
                    "plate_numbers": [],


        }

    return jsonify(response)


@app.route('/sso/oauth/token', methods=['GET', 'POST'])
def mock_oauth():
    global request_counter

    # 模拟处理延迟
    delay = random.uniform(*MOCK_RESPONSE_DELAY)
    time.sleep(delay)

    # 线程安全的计数器递增
    with counter_lock:
        request_counter += 1

    # 返回模拟响应
    return jsonify({
        "access_token": MOCK_TOKEN,
        "token_type": "bearer",
        "expires_in": 3600,
        "scope": "read write",
        "request_count": request_counter,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
    })


@app.route('/stats')
def get_stats():
    return jsonify({
        "total_requests": request_counter,
        "current_time": time.strftime("%Y-%m-%d %H:%M:%S")
    })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, threaded=True)