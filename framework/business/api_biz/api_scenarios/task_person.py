#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Author:  slg
@Time: 2022/11/15
@File: test_person
"""
import os
from loguru import logger

from framework.business.api_biz.api_services.device_api import deviceid
from framework.business.api_biz.api_services.person_api import PersonApi
from framework.utils.file_io import Fileio
from framework.utils.get_ini_conf import Conf
from framework.utils.file_utils import YamlReader


class Task_person():
    '''
    行为分析任务模块
    '''


# ********************** 设置任务任务 **********************

    def person_set(self, outputType,roi,topic,name,camera):
        '''
        outputType:4:呼救5:打架7:刀棍8:吸烟9:打电话10:人员走动11:离岗12:玩手机18:跌倒
                    19:睡岗20:打哈欠22:推搡23:打砸24:打盹25:翻越栏杆28:聚集
        args：roi参数，不传使用默认roi
        '''
        roi_param = YamlReader.read_yaml('data\\api\\person\\person_roi.yaml')
        set_param = YamlReader.read_yaml('data\\api\\person\\person_set.yaml')
        set_param2 = YamlReader.read_yaml('data\\api\\person\\person_set2.yaml')
        i = deviceid({"deviceName":name})
        taskId_list = []
        if i:
            for output_Type in outputType.split(','):
                if output_Type in (10, 11, 28):
                        roi_param['deviceId'] = i
                        roi_param['roiParams'][0]['behaviorType'] = output_Type
                        roi_param['roiParams'][0]['areas'][0]['roiId'] = i + output_Type
                        roi_param['roiParams'][0]['areas'][0]['points'] = roi
                        # 2.发送设置roi的请求-------------------------------------
                        res = PersonApi().person_roi_api(roi_param)
                        if res['code'] == '00000000':
                            logger.info('行人行为分析任务ROI设置成功')
                        else:
                            logger.info(f"行人行为分析任务ROI设置失败：{res['message']}")
                        # 1.创建行人行为任务--------------------------------------
                        set_param['deviceId'] = i
                        set_param['task']['outputType'] = output_Type
                        set_param['task']['roiInfos'][0]['roiId'] = i + output_Type
                        set_param['topic'] = topic
                        if int(output_Type) == 28:
                            if camera:
                                if 'peopleNumberMaxThresgold' and 'peopleNumberMinThreshold' in camera.keys():
                                    set_param['task']['roiInfos'][0]['peopleNumberMaxThresgold'] = camera['peopleNumberMaxThresgold']
                                    set_param['task']['roiInfos'][0]['peopleNumberMinThresgold'] = camera['peopleNumberMinThreshold']
                                else:
                                    logger.info('聚集行人行为必须设置peopleNumberMaxThresgold,peopleNumberMinThresgold参数')

                        # 2.发送新增任务的请求
                        res = PersonApi().person_set_api(set_param)
                        try:
                            del set_param['task']['roiInfos'][0]['peopleNumberMaxThresgold']
                            del set_param['task']['roiInfos'][0]['peopleNumberMinThresgold']
                        except:
                            pass
                        # 3.断言
                        if res['code'] == '00000000':
                            logger.info(f'新增{i}行人行为分析{output_Type}成功')
                            Fileio().write_data(f'person\\{i}行人行为分析{output_Type}任务id.txt', res['data'])
                            taskId_list.append(res['data'])
                        else:
                            logger.info(f"新增{i}行人行为分析{output_Type}失败：{res['message']}")
                else:   # 不需要roi的请求
                    set_param2['deviceId'] = i
                    set_param2['task']['outputType'] = output_Type
                    set_param2['topic'] = topic
                    # 2.发送新增任务的请求
                    res = PersonApi().person_set_api(set_param2)
                    # 3.断言
                    if res['code'] == '00000000':
                        logger.info(f'新增{i}行人行为分析{output_Type}成功')
                        Fileio().write_data(f'person\\{i}行人行为分析{output_Type}任务id.txt', res['data'])
                        taskId_list.append(res['data'])
                    else:
                        logger.info(f"新增{i}行为分析{output_Type}失败：{res['message']}")
        else:
            logger.info('行人行为分析新增失败，设备ID为空')

        return taskId_list

    def del_persontask(self,name,outputType,taskId):
        '''删除行人行为任务'''
        path = os.path.abspath(os.getcwd())
        del_param = YamlReader.read_yaml('data\\api\\person\\person_del.yaml')
        path = path + '\\datas\\taskid\\person'
        id = deviceid(name)
        for root,dirs,files in os.walk(path,topdown=False):
            if files:
                for i in files:
                    n = 0
                    for output_Type in outputType.split(','):
                            if id+'行人行为分析'+output_Type+'任务id' in i:
                                del_param['taskId'] = taskId[n]
                                res = PersonApi().person_del_api(del_param)
                                if res['code'] == '00000000':
                                    logger.info(f'{taskId[n]}行人行为任务删除成功')
                                    os.remove(path + '\\' + i)
                                else:
                                    logger.info(f"{taskId[n]}删除失败:{res['message']}")

                            else:
                                logger.info(f'没有创建的行人行为任务')
                            n += 1
            else:
                logger.info(f'没有行人行为任务')
