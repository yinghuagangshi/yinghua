import time
from framework.utils.global_control import LogLevel
from framework.business.api_biz.api_scenarios.task_person import Task_person as test_id
from framework.utils.file_utils import YamlReader

camera=YamlReader().read_yaml(r"data/api/camera_config.yaml")
def test_persontask(self, camera, key="personbehavior", name="cameraName"):
    """ 行人行为任务 """
    topic = camera[key]['topic']
    roi = camera[key]['roi']
    fun_test = "task_person"
    outputType = camera[key]['type']

    # 先判断是否有time字段，若没有则创建立即执行任务，有就获取开始停止时间。
    try:
        read_config_time = camera[key]['time']
        for t in read_config_time:
            config_starttime = self.fomat_time(t['starttime'])
            config_endtimep = self.fomat_time(t['endtime'])
            # 将格式化后的开始停止时间转成时间戳，用于后续判断
            start_time = self.stamp_time(config_starttime)  # 配置文件里，当前任务的开始时间
            end_time = self.stamp_time(config_endtimep)  # 配置文件里，当前任务的结束时间
            try:  # 非首次创建任务
                taskId = camera['person_taskid']
                if start_time <= int(time.time() * 1000) <= end_time:
                    if end_time == int(time.time() * 1000):
                        # print('当前时间等于配置文件读到的结束时间', int(time.time() * 1000), '开始时间', start_time, '结束时间', end_time)
                        self.showLog(LogLevel.INFO.value, name + '-' + key + " 删除行人任务")
                        test_id.del_persontask(self, name, outputType, taskId)
                        del camera['person_taskid']
                        del camera['person_match_endtime']
                        break
                    else:
                        # print('当前时间不是任务结束时间', int(time.time() * 1000), '开始时间', start_time, '结束时间', end_time)
                        break
                elif int(time.time() * 1000) > end_time:
                    if end_time == int(camera['person_match_endtime']):
                        # print('配置文件结束时间与当前任务创建时停止时间一致', int(time.time() * 1000), '开始时间', start_time, '结束时间', end_time)
                        self.showLog(LogLevel.INFO.value, name + '-' + key + " 删除行人任务")
                        test_id.del_persontask(self, name, outputType, taskId)
                        del camera['person_taskid']
                        del camera['person_match_endtime']
                        break
                    else:
                        # print('当前时间与创建此任务时的停止时间不一致', int(time.time() * 1000), '开始时间', start_time, '结束时间', end_time)
                        pass
                elif int(time.time() * 1000) < start_time:
                    # print('当前时间小于开始时间', int(time.time() * 1000), '开始时间', start_time, '结束时间', end_time)
                    break
            except KeyError:  # 首次创建任务
                if start_time <= int(time.time() * 1000) < end_time:
                    # print('当前时间大于开始时间小于结束时间', int(time.time() * 1000), '开始时间', start_time, '结束时间', end_time)
                    self.showLog(LogLevel.INFO.value, name + " 创建行人任务")
                    taskid = test_id.person_set(self, outputType, roi, topic, name, camera[key])  # 调取创建行人任务接口
                    camera['person_taskid'] = taskid
                    camera['person_match_endtime'] = end_time
                    if not taskid:
                        msg = name + " 请求错误，没有返回行人任务id"
                        self.showLog(LogLevel.ERROR.value, msg)
                    break

                elif int(time.time() * 1000) < start_time:
                    break
                else:
                    pass

    except KeyError:  # 没有time字段
        try:
            camera['person_taskid']
        except:
            # print('没有time字段，当前时间：', int(time.time() * 1000))
            taskid = test_id.person_set(self, outputType, roi, topic, name, camera[key])
            camera['person_taskid'] = taskid

if __name__ == "__main__":
    test_persontask(camera, key="personbehavior", name="cameraName")