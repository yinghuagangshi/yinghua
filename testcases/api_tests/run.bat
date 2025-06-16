@echo off
:: 失败测试用例重试次数
set rCount=1
:: 失败测试用例执行间隔时间 单位秒
set rTime=1
:: 报告目录 D:\is-ocean-api\report
set rDir="D:\is-ocean-api\report"

#初始化
pytest -s -v --html=%rDir%\test_ocean_init.html testcases\ocean_init\test_ocean_init.py
##报警类接口
#布控报警删除
pytest -s -v --html=%rDir%\test_record_alarm_delete.html testcases\data\data_alarm\test_record_alarm_delete.py
#聚集报警详情
pytest -s -v --html=%rDir%\test_record_alarm_gatherUygursget.html testcases\data\data_alarm\test_record_alarm_gatherUygursget.py
#分页查询聚集报警
pytest -s -v --html=%rDir%\test_record_alarm_gatheruygurspages.html testcases\data\data_alarm\test_record_alarm_gatheruygurspages.py
#查询报警
pytest -s -v --html=%rDir%\test_record_alarm_get.html testcases\data\data_alarm\test_record_alarm_get.py
#查询报警
pytest -s -v --html=%rDir%\test_record_alarm_get_01.html testcases\data\data_alarm\test_record_alarm_get_01.py
#分页查询报警
pytest -s -v --html=%rDir%\test_record_alarm_pages.html testcases\data\data_alarm\test_record_alarm_pages.py
#分页查询报警
pytest -s -v --html=%rDir%\test_record_alarm_pages_01.html testcases\data\data_alarm\test_record_alarm_pages_01.py
#行为报警删除
pytest -s -v --html=%rDir%\test_record_behaviour_alarmdelete.html testcases\data\data_alarm\test_record_behaviour_alarmdelete.py
#行为报警查询
pytest -s -v --html=%rDir%\test_record_behaviour_alarmget.html testcases\data\data_alarm\test_record_behaviour_alarmget.py
#行为报警分页查询
pytest -s -v --html=%rDir%\test_record_behaviour_alarmpages.html testcases\data\data_alarm\test_record_behaviour_alarmpages.py
#头肩报警分页查询
pytest -s -v --html=%rDir%\test_record_shoulder_alarm_pages.html testcases\data\data_alarm\test_record_shoulder_alarm_pages.py
#车辆报警删除
pytest -s -v --html=%rDir%\test_record_vehicle_alarmdelete.html testcases\data\data_alarm\test_record_vehicle_alarmdelete.py
#车辆报警查询
pytest -s -v --html=%rDir%\test_record_vehicle_alarmget.html testcases\data\data_alarm\test_record_vehicle_alarmget.py
#车辆报警分页查询
pytest -s -v --html=%rDir%\test_record_vehicle_alarmpages.html testcases\data\data_alarm\test_record_vehicle_alarmpages.py
#车辆报警详情查询
pytest -s -v --html=%rDir%\test_record_vehicle_property_alarmget.html testcases\data\data_alarm\test_record_vehicle_property_alarmget.py
#人体报警列表查询
pytest -s -v --html=%rDir%\test_recordAlarmBody_list.html testcases\data\data_alarm\test_recordAlarmBody_list.py
#人体报警列表查询
pytest -s -v --html=%rDir%\test_recordAlarmBody_list.html testcases\data\data_alarm\test_recordAlarmBody_list.py

##设备类接口
#初始化设备roi
pytest -s -v --html=%rDir%\test_device_behavior_roi_init.html testcases\device\device_behavior\test_device_behavior_roi_init.py
#设置行为分析任务（增量）
pytest -s -v --html=%rDir%\test_device_camera_behavior_add.html testcases\device\device_behavior\test_device_camera_behavior_add.py
#行为分析任务启停
pytest -s -v --html=%rDir%\test_device_camera_behavior_control.html testcases\device\device_behavior\test_device_camera_behavior_control.py
#行为分析任务删除
pytest -s -v --html=%rDir%\test_device_camera_behavior_delete.html testcases\device\device_behavior\test_device_camera_behavior_delete.py
#行为分析任务列表查询
pytest -s -v --html=%rDir%\test_device_camera_behavior_list.html testcases\device\device_behavior\test_device_camera_behavior_list.py
#行为分析任务分页查询
pytest -s -v --html=%rDir%\test_device_camera_behavior_pages.html testcases\device\device_behavior\test_device_camera_behavior_pages.py
#设置行为分析任务（全量）
pytest -s -v --html=%rDir%\test_device_camera_behavior_set.html testcases\device\device_behavior\test_device_camera_behavior_set.py
#新增虚拟相机
pytest -s -v --html=%rDir%\test_camera_add.html testcases\device\device_camera\test_camera_add.py
#删除虚拟相机
pytest -s -v --html=%rDir%\test_camera_delete.html testcases\device\device_camera\test_camera_delete.py
#编辑虚拟相机
pytest -s -v --html=%rDir%\test_camera_edit.html testcases\device\device_camera\test_camera_edit.py
#查询虚拟相机
pytest -s -v --html=%rDir%\test_camera_get.html testcases\device\device_camera\test_camera_get.py
#列表查询虚拟相机
pytest -s -v --html=%rDir%\test_camera_list.html testcases\device\device_camera\test_camera_list.py
#设备树列表查询虚拟相机
pytest -s -v --html=%rDir%\test_camera_listByTree.html testcases\device\device_camera\test_camera_listByTree.py
#分页查询虚拟相机
pytest -s -v --html=%rDir%\test_camera_pages.html testcases\device\device_camera\test_camera_pages.py
#设备树分页查询虚拟相机
pytest -s -v --html=%rDir%\test_camera_pagesByTree.html testcases\device\device_camera\test_camera_pagesByTree.py
#设备认领
pytest -s -v --html=%rDir%\test_device_dcs_claim.html testcases\device\device_dcs\test_device_dcs_claim.py
#查询未挂载的设备
pytest -s -v --html=%rDir%\test_device_devicetree_getUnmount.html testcases\device\device_devicetree\test_device_devicetree_getUnmount.py
#批量挂载的设备
pytest -s -v --html=%rDir%\test_device_devicetree_mountbatch.html testcases\device\device_devicetree\test_device_devicetree_mountbatch.py
#批量移动设备
pytest -s -v --html=%rDir%\test_device_devicetree_movebatch.html testcases\device\device_devicetree\test_device_devicetree_movebatch.py
#批量卸载设备
pytest -s -v --html=%rDir%\test_device_devicetree_unloadbatch.html testcases\device\device_devicetree\test_device_devicetree_unloadbatch.py
#批量绑定引擎
pytest -s -v --html=%rDir%\test_engine_batchBind.html testcases\device\device_engine\test_engine_batchBind.py
#批量解除绑定引擎
pytest -s -v --html=%rDir%\test_engine_batchUnBind.html testcases\device\device_engine\test_engine_batchUnBind.py
#绑定引擎
pytest -s -v --html=%rDir%\test_engine_bind.html testcases\device\device_engine\test_engine_bind.py
#设备绑定引擎关系列表查询
pytest -s -v --html=%rDir%\test_engine_bind_list.html testcases\device\device_engine\test_engine_bind_list.py
#设备树设备绑定引擎关系列表查询
pytest -s -v --html=%rDir%\test_engine_bind_listByTree.html testcases\device\device_engine\test_engine_bind_listByTree.py
#设备解绑引擎
pytest -s -v --html=%rDir%\test_engine_unbind.html testcases\device\device_engine\test_engine_unbind.py
#实时解析任务新增（增量）
pytest -s -v --html=%rDir%\test_camera_output_add.html testcases\device\device_output\device_output_camera\test_camera_output_add.py
#实时解析任务启停
pytest -s -v --html=%rDir%\test_camera_output_control.html testcases\device\device_output\device_output_camera\test_camera_output_control.py
#实时解析任务删除
pytest -s -v --html=%rDir%\test_camera_output_delete.html testcases\device\device_output\device_output_camera\test_camera_output_delete.py
#实时解析任务编辑
pytest -s -v --html=%rDir%\test_camera_output_edit.html testcases\device\device_output\device_output_camera\test_camera_output_edit.py
#实时解析任务列表查询
pytest -s -v --html=%rDir%\test_camera_output_list.html testcases\device\device_output\device_output_camera\test_camera_output_list.py
#实时解析任务分页查询
pytest -s -v --html=%rDir%\test_camera_output_pages.html testcases\device\device_output\device_output_camera\test_camera_output_pages.py
#实时解析任务新增（全量）
pytest -s -v --html=%rDir%\test_camera_output_set.html testcases\device\device_output\device_output_camera\test_camera_output_set.py

#头肩解析任务启停
pytest -s -v --html=%rDir%\test_headshoulder_output_control.html testcases\device\device_output\device_output_headshoulder\test_headshoulder_output_control.py
#头肩解析任务删除
pytest -s -v --html=%rDir%\test_headshoulder_output_delete.html testcases\device\device_output\device_output_headshoulder\test_headshoulder_output_delete.py
#头肩解析任务列表查询
pytest -s -v --html=%rDir%\test_headshoulder_output_list.html testcases\device\device_output\device_output_headshoulder\test_headshoulder_output_list.py
#头肩解析任务分页查询
pytest -s -v --html=%rDir%\test_headshoulder_output_pages.html testcases\device\device_output\device_output_headshoulder\test_headshoulder_output_pages.py
#头肩解析任务新增（全量）
pytest -s -v --html=%rDir%\test_headshoulder_output_set.html testcases\device\device_output\device_output_headshoulder\test_headshoulder_output_set.py
#头肩解析任务roi设置
pytest -s -v --html=%rDir%\test_headshoulder_output_roi_set.html testcases\device\device_output\device_output_headshoulder\test_headshoulder_output_roi_set.py
#行为分析任务roi设置
pytest -s -v --html=%rDir%\test_device_behavior_roi_query.html testcases\device\device_roi\test_device_behavior_roi_query.py
#行为分析任务roi设置-入侵
pytest -s -v --html=%rDir%\test_device_behavior_roi_set.html testcases\device\device_roi\test_device_behavior_roi_set.py
#解析任务roi查询
pytest -s -v --html=%rDir%\test_device_output_roi_query.html testcases\device\device_roi\test_device_output_roi_query.py
#解析任务roi设置
pytest -s -v --html=%rDir%\test_device_output_roi_set.html testcases\device\device_roi\test_device_output_roi_set.py
#新增设备树节点
pytest -s -v --html=%rDir%\test_device_treenode_add.html testcases\device\device_treenode\test_device_treenode_add.py
#批量删除设备树节点
pytest -s -v --html=%rDir%\test_device_treenode_deletebatch.html testcases\device\device_treenode\test_device_treenode_deletebatch.py
#移动设备树节点
pytest -s -v --html=%rDir%\test_device_treenode_move.html testcases\device\device_treenode\test_device_treenode_move.py
#查询设备树节点
pytest -s -v --html=%rDir%\test_device_treenode_nodeslist.html testcases\device\device_treenode\test_device_treenode_nodeslist.py
##全结构化
#全结构化人员行为分页查询
pytest -s -v --html=%rDir%\test_struct_behavior_page.html testcases\struct\struct_behavior\test_struct_behavior_page.py
#全结构化人体批量查询
pytest -s -v --html=%rDir%\test_struct_body_gets.html testcases\struct\struct_body\test_struct_body_gets.py
#全结构化人体分页查询
pytest -s -v --html=%rDir%\test_struct_body_pages.html testcases\struct\struct_body\test_struct_body_pages.py
#全结构化人体检索
pytest -s -v --html=%rDir%\test_struct_body_recog.html testcases\struct\struct_body\test_struct_body_recog.py
#全结构化人体轨迹检索
pytest -s -v --html=%rDir%\test_struct_body_track.html testcases\struct\struct_body\test_struct_body_track.py

#抓拍照接入
pytest -s -v --html=%rDir%\test_data_entry.html testcases\struct\struct_common\test_data_entry.py
#新增人体采集流水
pytest -s -v --html=%rDir%\test_struct_collect.html testcases\struct\struct_common\test_struct_collect.py
#人脸检索人体踪迹检索
pytest -s -v --html=%rDir%\test_struct_comprehensive_recog.html testcases\struct\struct_common\test_struct_comprehensive_recog.py
#关联查询
pytest -s -v --html=%rDir%\test_struct_correlation_search.html testcases\struct\struct_common\test_struct_correlation_search.py
#检测所有类型的图片
pytest -s -v --html=%rDir%\test_struct_detect.html testcases\struct\struct_common\test_struct_detect.py
#全结构化字段字典列表
pytest -s -v --html=%rDir%\test_struct_field_mapping_list.html testcases\struct\struct_common\test_struct_field_mapping_list.py
#全结构化批量查询
pytest -s -v --html=%rDir%\test_struct_gets.html testcases\struct\struct_common\test_struct_gets.py
#全景照片数据采集
pytest -s -v --html=%rDir%\test_struct_imgcollect.html testcases\struct\struct_common\test_struct_imgcollect.py
#全结构化人脸综合分页查询,抓拍流水数据查询
pytest -s -v --html=%rDir%\test_struct_page.html testcases\struct\struct_common\test_struct_page.py
#全结构化检索,抓拍流水数据查询
pytest -s -v --html=%rDir%\test_struct_recog.html testcases\struct\struct_common\test_struct_recog.py
#人抓拍流水根据参数过滤入库
pytest -s -v --html=%rDir%\test_struct_savedata_params.html testcases\struct\struct_common\test_struct_savedata_params.py
#解析所有类型的图片
pytest -s -v --html=%rDir%\test_struct_structure.html testcases\struct\struct_common\test_struct_structure.py
#初始化全结构化采集流水
pytest -s -v --html=%rDir%\test_struct_data_init.html testcases\struct\struct_data_init\test_struct_data_init.py

#全结构人脸批量查询
pytest -s -v --html=%rDir%\test_struct_face_gets.html testcases\struct\struct_face\test_struct_face_gets.py
#全结构人脸分页查询
pytest -s -v --html=%rDir%\test_struct_face_page.html testcases\struct\struct_face\test_struct_face_page.py
#全结构人脸检索
pytest -s -v --html=%rDir%\test_struct_face_gets.html testcases\struct\struct_face\test_struct_face_gets.py
#全结构人脸轨迹检索
pytest -s -v --html=%rDir%\test_struct_face_gets.html testcases\struct\struct_face\test_struct_face_gets.py
#指定区域人数统计
pytest -s -v --html=%rDir%\test_struct_headshoulder_count.html testcases\struct\struct_headshoulder\test_struct_headshoulder_count.py
#人流密度指数统计
pytest -s -v --html=%rDir%\test_struct_headshoulder_density.html testcases\struct\struct_headshoulder\test_struct_headshoulder_density.py
#指定区域内人群热力图统计
pytest -s -v --html=%rDir%\test_struct_headshoulder_heatmap.html testcases\struct\struct_headshoulder\test_struct_headshoulder_heatmap.py
#全结构化非机动车批量查询
pytest -s -v --html=%rDir%\test_struct_nonvehicle_gets.html testcases\struct\struct_nonvehicle\test_struct_nonvehicle_gets.py
#全结构化非机动车分页查询
pytest -s -v --html=%rDir%\test_struct_nonvehicle_page.html testcases\struct\struct_nonvehicle\test_struct_nonvehicle_page.py
#全结构化非机动车检索
pytest -s -v --html=%rDir%\test_struct_nonvehicle_recog.html testcases\struct\struct_nonvehicle\test_struct_nonvehicle_recog.py
#抓拍数据全量统计
pytest -s -v --html=%rDir%\test_struct_statistic_allCount.html testcases\struct\struct_statistic\test_struct_statistic_allCount.py
#抓拍数据按天统计
pytest -s -v --html=%rDir%\test_struct_statistic_dayCount.html testcases\struct\struct_statistic\test_struct_statistic_dayCount.py
#抓拍数据按设备统计
pytest -s -v --html=%rDir%\test_struct_statistic_deviceCount.html testcases\struct\struct_statistic\test_struct_statistic_deviceCount.py
#查询90天的数据
pytest -s -v --html=%rDir%\test_struct_statistic_deviceDayCount.html testcases\struct\struct_statistic\test_struct_statistic_deviceDayCount.py
#抓拍数据按设备统计
pytest -s -v --html=%rDir%\test_struct_statistic_hourCount.html testcases\struct\struct_statistic\test_struct_statistic_hourCount.py
#全结构化机动车批量查询
pytest -s -v --html=%rDir%\test_struct_vehicle_gets.html testcases\struct\struct_vehicle\test_struct_vehicle_gets.py
#全结构化机动车分页查询
pytest -s -v --html=%rDir%\test_struct_vehicle_page.html testcases\struct\struct_vehicle\test_struct_vehicle_page.py
#全结构化机动车检索
pytest -s -v --html=%rDir%\test_struct_vehicle_recog.html testcases\struct\struct_vehicle\test_struct_vehicle_recog.py
##统计类
#聚类任务第一次聚类
pytest -s -v --html=%rDir%\increment_baseTree.html testcases\tactic\cluster_task\increment_baseTree.py
##终端设备
#终端删除
pytest -s -v --html=%rDir%\test_device_terminal_delete.html testcases\terminal\tactic_face_dossier\test_device_terminal_delete.py
#终端注册
pytest -s -v --html=%rDir%\test_device_terminal_regist.html testcases\terminal\tactic_face_dossier\test_device_terminal_regist.py
