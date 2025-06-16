from flask import Flask, request, jsonify
import time

app = Flask(__name__)

# 模拟数据库
devices_db = []
tasks_db = {
    "scene_behavior": [],
    "high_altitude": [],
    "perimeter": [],
    "pedestrian": [],
    "vehicle": [],
    "realtime": [],
    "head_shoulder": []
}


# ****************************获取token接口*****************************
@app.route('/sso/oauth/token', methods=['POST'])
def get_token():
    # 模拟认证逻辑
    auth = request.authorization
    if auth and auth.username == 'admin' and auth.password == 'password':
        return jsonify({
            "access_token": "mock_access_token_" + str(int(time.time())),
            "token_type": "bearer",
            "expires_in": 3600,
            "scope": "read write"
        })
    return jsonify({"error": "unauthorized"}), 401


# ****************************设备管理类接口*****************************
@app.route('/api/device/camera/pages', methods=['GET'])
def camera_pages():
    page = request.args.get('page', 1, type=int)
    size = request.args.get('size', 10, type=int)

    # 模拟分页数据
    mock_data = {
        "code": 200,
        "message": "success",
        "data": {
            "total": len(devices_db),
            "list": devices_db[(page - 1) * size: page * size],
            "pageNum": page,
            "pageSize": size
        }
    }
    return jsonify(mock_data)


@app.route('/api/device/camera/get', methods=['GET'])
def get_camera():
    device_id = request.args.get('id')
    # 模拟查找设备
    device = next((d for d in devices_db if d.get('id') == device_id), None)
    if device:
        return jsonify({
            "code": 200,
            "message": "success",
            "data": device
        })
    return jsonify({"code": 404, "message": "device not found"}), 404


@app.route('/ocean/api/device/camera/list', methods=['GET'])
def camera_list():
    return jsonify({
        "code": 200,
        "message": "success",
        "data": devices_db
    })


# ****************************任务类接口*****************************
# 场景行为任务
@app.route('/device/behavior/roi/scenario/add', methods=['POST'])
def scene_roi():
    data = request.json
    return jsonify({
        "code": 200,
        "message": "ROI设置成功",
        "data": {"roi_id": f"scene_roi_{int(time.time())}"}
    })


@app.route('/device/camera/behavior/scenario/add', methods=['POST'])
def scene_set():
    data = request.json
    task_id = f"scene_task_{int(time.time())}"
    tasks_db["scene_behavior"].append({
        "task_id": task_id,
        "config": data
    })
    return jsonify({
        "code": 200,
        "message": "场景行为任务设置成功",
        "data": {"task_id": task_id}
    })


@app.route('/device/camera/behavior/scenario/delete', methods=['POST'])
def scene_del():
    task_id = request.json.get('task_id')
    tasks_db["scene_behavior"] = [t for t in tasks_db["scene_behavior"] if t['task_id'] != task_id]
    return jsonify({
        "code": 200,
        "message": "场景行为任务删除成功"
    })


# 高空抛物任务
@app.route('/motion/roi/set', methods=['POST'])
def motion_roi():
    return jsonify({
        "code": 200,
        "message": "高空抛物ROI设置成功",
        "data": {"roi_id": f"motion_roi_{int(time.time())}"}
    })


@app.route('/motion/add', methods=['POST'])
def motion_set():
    task_id = f"motion_task_{int(time.time())}"
    tasks_db["high_altitude"].append({
        "task_id": task_id,
        "config": request.json
    })
    return jsonify({
        "code": 200,
        "message": "高空抛物任务设置成功",
        "data": {"task_id": task_id}
    })


@app.route('/motion/output/delete', methods=['POST'])
def motion_del():
    task_id = request.json.get('task_id')
    tasks_db["high_altitude"] = [t for t in tasks_db["high_altitude"] if t['task_id'] != task_id]
    return jsonify({
        "code": 200,
        "message": "高空抛物任务删除成功"
    })


# 其他任务类型的接口可以按照类似的方式实现...

# 实时解析任务
@app.route('/device/camera/output/add', methods=['POST'])
def output_set():
    task_id = f"realtime_task_{int(time.time())}"
    tasks_db["realtime"].append({
        "task_id": task_id,
        "config": request.json
    })
    return jsonify({
        "code": 200,
        "message": "实时解析任务设置成功",
        "data": {"task_id": task_id}
    })


@app.route('/device/camera/output/delete', methods=['POST'])
def output_del():
    task_id = request.json.get('task_id')
    tasks_db["realtime"] = [t for t in tasks_db["realtime"] if t['task_id'] != task_id]
    return jsonify({
        "code": 200,
        "message": "实时解析任务删除成功"
    })


@app.route('/device/camera/output/control', methods=['POST'])
def snapshot_restart_stop():
    action = request.json.get('action')
    task_id = request.json.get('task_id')
    return jsonify({
        "code": 200,
        "message": f"任务{task_id}已{action}"
    })


# 初始化一些模拟设备数据
def init_mock_data():
    for i in range(1, 21):
        devices_db.append({
            "id": f"device_{i}",
            "name": f"Camera {i}",
            "ip": f"192.168.1.{i}",
            "status": "online" if i % 2 == 0 else "offline",
            "location": f"Area {i % 5 + 1}"
        })


if __name__ == '__main__':
    init_mock_data()
    app.run(host='0.0.0.0', port=10006, debug=True)