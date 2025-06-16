#!/bin/bash
# 失败测试用例重试次数
rCount=1
# 失败测试用例执行间隔时间 单位秒
rTime=1
# 报告目录 /data/autotest/report/api/is-ocean-api
rDir="/data/program/autotest/report/api/is-ocean-api"

    # ocean_init 新环境需要执行一次:dcs认领设备初始化+设备节点及设备挂载初始化+设备绑定引擎初始化
run1(){
#    pytest -v --html=${rDir}/01_test_ocean_clean.html --json=${rDir}/01_test_ocean_clean.json testcases/ocean_init/test_ocean_clean.py
    pytest -v --html=${rDir}/01_test_ocean_init.html --json=${rDir}/01_test_ocean_init.json testcases/ocean_init/test_ocean_init.py
    #pytest -v --html=${rDir}/01_test_initMethod.html --json=${rDir}/01_test_initMethod.json  service/application/initMethod.py
    for ((i=0;i<=1;i++))
    do
        pytest -v --html=${rDir}/01_test_struct_data_init.html --json=${rDir}/01_test_struct_data_init.json testcases/struct/struct_data_init/test_struct_data_init.py
        pytest --reruns ${rCount} -v --html=${rDir}/19_test_struct_clean.html --json=${rDir}/19_test_struct_clean.json testcases/ocean_init/test_struct_clean.py
#        pytest -v --html=${rDir}/01_test_struct_properties_init.html --json=${rDir}/01_test_struct_properties_init.json testcases/ocean_init/test_struct_properties_init.py
    done
     pytest -v --html=${rDir}/01_test_device_behavior_roi_init.html --json=${rDir}/01_test_device_behavior_roi_init.json testcases/device/device_behavior/test_device_behavior_roi_init.py
}

    #全结构化图片流数据接入接口
run2(){
    pytest --reruns ${rCount} -v --html=${rDir}/02_test_struct_collect.html --json=${rDir}/02_test_struct_collect.json testcases/struct/struct_common/test_struct_collect.py
    pytest --reruns ${rCount} -v --html=${rDir}/02_test_struct_imgcollect.html --json=${rDir}/02_test_struct_imgcollect.json testcases/struct/struct_common/test_struct_imgcollect.py
#    pytest --reruns ${rCount} -v --html=${rDir}/02_test_struct_data_entry.html --json=${rDir}/02_test_struct_data_entry.json testcases/struct/struct_common/test_data_entry.py
    #全结构化检测、解析接口接口
    pytest --reruns ${rCount} -v --html=${rDir}/02_test_struct_detect.html --json=${rDir}/02_test_struct_detect.json testcases/struct/struct_common/test_struct_detect.py
    pytest --reruns ${rCount} -v --html=${rDir}/02_test_struct_structure.html --json=${rDir}/02_test_struct_structure.json testcases/struct/struct_common/test_struct_structure.py
    #全结构化综合分页查询接口
    pytest --reruns ${rCount} -v --html=${rDir}/02_test_struct_page.html --json=${rDir}/02_test_struct_page.json testcases/struct/struct_common/test_struct_page.py
    pytest --reruns ${rCount} -v --html=${rDir}/02_test_struct_gets.html --json=${rDir}/02_test_struct_gets.json testcases/struct/struct_common/test_struct_gets.py
    pytest --reruns ${rCount} -v --html=${rDir}/02_test_struct_recog.html --json=${rDir}/02_test_struct_recog.json testcases/struct/struct_common/test_struct_recog.py
    pytest --reruns ${rCount} -v --html=${rDir}/02_test_struct_comprehensive_recog.html --json=${rDir}/02_test_struct_comprehensive_recog.json testcases/struct/struct_common/test_struct_comprehensive_recog.py
}


    #全结构化人体分页查询、批量查询、检索接口
run3(){
    pytest --reruns ${rCount} -v --html=${rDir}/03_test_struct_body_page.html --json=${rDir}/03_test_struct_body_page.json testcases/struct/struct_body/test_struct_body_page.py
    pytest --reruns ${rCount} -v --html=${rDir}/03_test_struct_body_gets.html --json=${rDir}/03_test_struct_body_gets.json testcases/struct/struct_body/test_struct_body_gets.py
    pytest --reruns ${rCount} -v --html=${rDir}/03_test_struct_body_recog.html --json=${rDir}/03_test_struct_body_recog.json testcases/struct/struct_body/test_struct_body_recog.py
    pytest --reruns ${rCount} -v --html=${rDir}/03_test_struct_body_track.html --json=${rDir}/03_test_struct_body_track.json testcases/struct/struct_body/test_struct_body_track.py
    #全结构化人脸分页查询、批量查询、检索接口
    pytest --reruns ${rCount} -v --html=${rDir}/03_test_struct_face_page.html --json=${rDir}/03_test_struct_face_page.json testcases/struct/struct_face/test_struct_face_page.py
    pytest --reruns ${rCount} -v --html=${rDir}/03_test_struct_face_gets.html --json=${rDir}/03_test_struct_face_gets.json testcases/struct/struct_face/test_struct_face_gets.py
    pytest --reruns ${rCount} -v --html=${rDir}/03_test_struct_face_recog.html --json=${rDir}/03_test_struct_face_recog.json testcases/struct/struct_face/test_struct_face_recog.py
    pytest --reruns ${rCount} -v --html=${rDir}/03_test_struct_face_track.html --json=${rDir}/03_test_struct_face_track.json testcases/struct/struct_face/test_struct_face_track.py
    #全结构化车辆分页查询、批量查询、检索接口
    pytest --reruns ${rCount} -v --html=${rDir}/03_test_struct_vehicle_page.html --json=${rDir}/03_test_struct_vehicle_page.json testcases/struct/struct_vehicle/test_struct_vehicle_page.py
    pytest --reruns ${rCount} -v --html=${rDir}/03_test_struct_vehicle_gets.html --json=${rDir}/03_test_struct_vehicle_gets.json testcases/struct/struct_vehicle/test_struct_vehicle_gets.py
    pytest --reruns ${rCount} -v --html=${rDir}/03_test_struct_vehicle_recog.html --json=${rDir}/03_test_struct_vehicle_recog.json testcases/struct/struct_vehicle/test_struct_vehicle_recog.py
    #全结构化非车辆分页查询、批量查询、检索接口
    pytest --reruns ${rCount} -v --html=${rDir}/03_test_struct_nonvehicle_page.html --json=${rDir}/03_test_struct_nonvehicle_page.json testcases/struct/struct_nonvehicle/test_struct_nonvehicle_page.py
    pytest --reruns ${rCount} -v --html=${rDir}/03_test_struct_nonvehicle_gets.html --json=${rDir}/03_test_struct_nonvehicle_gets.json testcases/struct/struct_nonvehicle/test_struct_nonvehicle_gets.py
    pytest --reruns ${rCount} -v --html=${rDir}/03_test_struct_nonvehicle_recog.html --json=${rDir}/03_test_struct_nonvehicle_recog.json testcases/struct/struct_nonvehicle/test_struct_nonvehicle_recog.py
}


    # 行为分析任务
run4(){
    pytest --reruns ${rCount} -v --html=${rDir}/04_test_device_camera_behavior_set.html --json=${rDir}/04_test_device_camera_behavior_set.json testcases/device/device_behavior/test_device_camera_behavior_set.py
    pytest --reruns ${rCount} -v --html=${rDir}/04_test_device_camera_behavior_add.html --json=${rDir}/04_test_device_camera_behavior_add.json testcases/device/device_behavior/test_device_camera_behavior_add.py
    pytest --reruns ${rCount} -v --html=${rDir}/04_test_device_camera_behavior_pages.html --json=${rDir}/04_test_device_camera_behavior_pages.json testcases/device/device_behavior/test_device_camera_behavior_pages.py
    pytest --reruns ${rCount} -v --html=${rDir}/04_test_device_camera_behavior_list.html --json=${rDir}/04_test_device_camera_behavior_list.json testcases/device/device_behavior/test_device_camera_behavior_list.py
    pytest --reruns ${rCount} -v --html=${rDir}/04_test_device_camera_behavior_delete.html --json=${rDir}/04_test_device_camera_behavior_delete.json testcases/device/device_behavior/test_device_camera_behavior_delete.py
    pytest --reruns ${rCount} -v --html=${rDir}/04_test_device_camera_behavior_control.html --json=${rDir}/04_test_device_camera_behavior_control.json testcases/device/device_behavior/test_device_camera_behavior_control.py
    pytest --reruns ${rCount} -v --html=${rDir}/device_camera_behavior_edit.html --json=${rDir}/device_camera_behavior_edit.json testcases/device/device_behavior/test_device_camera_behavior_edit.py
}

    # 设备管理与数据采集类接口：像机管理
run5(){
    pytest --reruns ${rCount} -v --html=${rDir}/05_test_camera_add.html --json=${rDir}/05_test_camera_add.json testcases/device/device_camera/test_camera_add.py
    pytest --reruns ${rCount} -v --html=${rDir}/05_test_camera_delete.html --json=${rDir}/05_test_camera_delete.json testcases/device/device_camera/test_camera_delete.py
    pytest --reruns ${rCount} -v --html=${rDir}/05_test_camera_edit.html --json=${rDir}/05_test_camera_edit.json testcases/device/device_camera/test_camera_edit.py
    pytest --reruns ${rCount} -v --html=${rDir}/05_test_camera_get.html --json=${rDir}/05_test_camera_get.json testcases/device/device_camera/test_camera_get.py
    pytest --reruns ${rCount} -v --html=${rDir}/05_test_camera_list.html --json=${rDir}/05_test_camera_list.json testcases/device/device_camera/test_camera_list.py
    pytest --reruns ${rCount} -v --html=${rDir}/05_test_camera_listByTree.html --json=${rDir}/05_test_camera_listByTree.json testcases/device/device_camera/test_camera_listByTree.py
    pytest --reruns ${rCount} -v --html=${rDir}/05_test_camera_pages.html --json=${rDir}/05_test_camera_pages.json testcases/device/device_camera/test_camera_pages.py
    pytest --reruns ${rCount} -v --html=${rDir}/05_test_camera_pagesByTree.html --json=${rDir}/05_test_camera_pagesByTree.json testcases/device/device_camera/test_camera_pagesByTree.py
}
#    # 设备管理与数据采集类接口：离线视频管理
#run6(){
#    pytest --reruns ${rCount} -v --html=${rDir}/06_test_video_add.html --json=${rDir}/06_test_video_add.json testcases/device/device_video/test_video_add.py
#    pytest --reruns ${rCount} -v --html=${rDir}/06_test_video_delete.html --json=${rDir}/06_test_video_delete.json testcases/device/device_video/test_video_delete.py
#    pytest --reruns ${rCount} -v --html=${rDir}/06_test_video_edit.html --json=${rDir}/06_test_video_edit.json testcases/device/device_video/test_video_edit.py
#    pytest --reruns ${rCount} -v --html=${rDir}/06_test_video_get.html --json=${rDir}/06_test_video_get.json testcases/device/device_video/test_video_get.py
#    pytest --reruns ${rCount} -v --html=${rDir}/06_test_video_list.html --json=${rDir}/06_test_video_list.json testcases/device/device_video/test_video_list.py
#    pytest --reruns ${rCount} -v --html=${rDir}/06_test_video_pages.html --json=${rDir}/06_test_video_pages.json testcases/device/device_video/test_video_pages.py
#    pytest --reruns ${rCount} -v --html=${rDir}/06_test_video_file_delete.html --json=${rDir}/06_test_video_file_delete.json testcases/device/device_video/test_video_file_delete.py
#    pytest --reruns ${rCount} -v --html=${rDir}/06_test_video_file_refresh.html --json=${rDir}/06_test_video_file_refresh.json testcases/device/device_video/test_video_file_refresh.py
#}

    # 设备管理与数据采集类接口：引擎绑定
run7(){
    pytest --reruns ${rCount} -v --html=${rDir}/07_test_engine_bind.html --json=${rDir}/07_test_engine_bind.json testcases/device/device_engine/test_engine_bind.py
    pytest --reruns ${rCount} -v --html=${rDir}/07_test_engine_bind_list.html --json=${rDir}/07_test_engine_bind_list.json testcases/device/device_engine/test_engine_bind_list.py
    pytest --reruns ${rCount} -v --html=${rDir}/07_test_engine_unbind.html --json=${rDir}/07_test_engine_unbind.json testcases/device/device_engine/test_engine_unbind.py
    pytest --reruns ${rCount} -v --html=${rDir}/07_test_engine_batchBind.html --json=${rDir}/07_test_engine_batchBind.json testcases/device/device_engine/test_engine_batchBind.py
    pytest --reruns ${rCount} -v --html=${rDir}/07_test_engine_batchUnBind.html --json=${rDir}/07_test_engine_batchUnBind.json testcases/device/device_engine/test_engine_batchUnBind.py
    pytest --reruns ${rCount} -v --html=${rDir}/07_test_engine_bind_listByTree.html --json=${rDir}/07_test_engine_bind_listByTree.json testcases/device/device_engine/test_engine_bind_listByTree.py
}

    #布控拓展
run11(){
    pytest --reruns ${rCount} -v --html=${rDir}/11_test_monitor_add.html --json=${rDir}/11_test_monitor_add.json testcases/application/application_monitor/test_monitor_add.py
    pytest --reruns ${rCount} -v --html=${rDir}/11_test_monitor_add_aloneface.html --json=${rDir}/11_test_monitor_add_aloneface.json testcases/application/application_monitor/test_monitor_add_aloneface.py
    pytest --reruns ${rCount} -v --html=${rDir}/11_test_monitor_advanced_get.html --json=${rDir}/11_test_monitor_advanced_get.json testcases/application/application_monitor/test_monitor_advanced_get.py
    pytest --reruns ${rCount} -v --html=${rDir}/11_test_monitor_advanced_pages.html --json=${rDir}/11_test_monitor_advanced_pages.json testcases/application/application_monitor/test_monitor_advanced_pages.py
    pytest --reruns ${rCount} -v --html=${rDir}/11_test_monitor_advanced_querydevice.html --json=${rDir}/11_test_monitor_advanced_querydevice.json testcases/application/application_monitor/test_monitor_advanced_querydevice.py
    pytest --reruns ${rCount} -v --html=${rDir}/11_test_monitor_batchDelete.html --json=${rDir}/11_test_monitor_batchDelete.json testcases/application/application_monitor/test_monitor_batchDelete.py
    pytest --reruns ${rCount} -v --html=${rDir}/11_test_monitor_delete.html --json=${rDir}/11_test_monitor_delete.json testcases/application/application_monitor/test_monitor_delete.py
    pytest --reruns ${rCount} -v --html=${rDir}/11_test_monitor_edit.html --json=${rDir}/11_test_monitor_edit.json testcases/application/application_monitor/test_monitor_edit.py
    pytest --reruns ${rCount} -v --html=${rDir}/11_test_monitor_edit_aloneface.html --json=${rDir}/11_test_monitor_edit_aloneface.json testcases/application/application_monitor/test_monitor_edit_aloneface.py
    pytest --reruns ${rCount} -v --html=${rDir}/11_test_monitor_get_aloneface.html --json=${rDir}/11_test_monitor_get_aloneface.json testcases/application/application_monitor/test_monitor_get_aloneface.py
    pytest --reruns ${rCount} -v --html=${rDir}/11_test_monitor_status_edit.html --json=${rDir}/11_test_monitor_status_edit.json testcases/application/application_monitor/test_monitor_status_edit.py
}

    #报警数据
run12(){
    pytest --reruns ${rCount} -v --html=${rDir}/12_test_record_alarm_delete.html --json=${rDir}/12_test_record_alarm_delete.json testcases/data/data_alarm/test_record_alarm_delete.py
    pytest --reruns ${rCount} -v --html=${rDir}/12_test_record_alarm_gatherUygursget.html --json=${rDir}/12_test_record_alarm_gatherUygursget.json testcases/data/data_alarm/test_record_alarm_gatherUygursget.py
    pytest --reruns ${rCount} -v --html=${rDir}/12_test_record_alarm_gatheruygurspages.html --json=${rDir}/12_test_record_alarm_gatheruygurspages.json testcases/data/data_alarm/test_record_alarm_gatheruygurspages.py
    pytest --reruns ${rCount} -v --html=${rDir}/12_test_record_alarm_get_01.html --json=${rDir}/12_test_record_alarm_get_01.json testcases/data/data_alarm/test_record_alarm_get_01.py
    pytest --reruns ${rCount} -v --html=${rDir}/12_test_record_alarm_pages.html --json=${rDir}/12_test_record_alarm_pages.json testcases/data/data_alarm/test_record_alarm_pages.py
    pytest --reruns ${rCount} -v --html=${rDir}/12_test_record_alarm_pages_01.html --json=${rDir}/12_test_record_alarm_pages_01.json testcases/data/data_alarm/test_record_alarm_pages_01.py
    pytest --reruns ${rCount} -v --html=${rDir}/12_test_record_behaviour_alarmdelete.html --json=${rDir}/12_test_record_behaviour_alarmdelete.json testcases/data/data_alarm/test_record_behaviour_alarmdelete.py
    pytest --reruns ${rCount} -v --html=${rDir}/12_test_record_behaviour_alarmget.html --json=${rDir}/12_test_record_behaviour_alarmget.json testcases/data/data_alarm/test_record_behaviour_alarmget.py
    pytest --reruns ${rCount} -v --html=${rDir}/12_test_record_behaviour_alarmpages.html --json=${rDir}/12_test_record_behaviour_alarmpages.json testcases/data/data_alarm/test_record_behaviour_alarmpages.py
    pytest --reruns ${rCount} -v --html=${rDir}/12_test_record_vehicle_alarmdelete.html --json=${rDir}/12_test_record_vehicle_alarmdelete.json testcases/data/data_alarm/test_record_vehicle_alarmdelete.py
    pytest --reruns ${rCount} -v --html=${rDir}/12_test_record_vehicle_alarmget.html --json=${rDir}/12_test_record_vehicle_alarmget.json testcases/data/data_alarm/test_record_vehicle_alarmget.py
    pytest --reruns ${rCount} -v --html=${rDir}/12_test_record_vehicle_alarmpages.html --json=${rDir}/12_test_record_vehicle_alarmpages.json testcases/data/data_alarm/test_record_vehicle_alarmpages.py
    pytest --reruns ${rCount} -v --html=${rDir}/12_test_recordVehicleAlarm_get.html --json=${rDir}/12_test_recordVehicleAlarm_get.json testcases/data/data_alarm/test_recordVehicleAlarm_get.py
    pytest --reruns ${rCount} -v --html=${rDir}/12_test_recordAlarmBody_list.html --json=${rDir}/12_test_recordAlarmBody_list.json testcases/data/data_alarm/test_recordAlarmBody_list.py
}

    # 设备树：设备树节点
run13(){
    pytest --reruns ${rCount} -v --html=${rDir}/13_test_device_treenode_add.html --json=${rDir}/13_test_device_treenode_add.json testcases/device/device_treenode/test_device_treenode_add.py
    pytest --reruns ${rCount} -v --html=${rDir}/13_test_device_treenode_deletebatch.html --json=${rDir}/13_test_device_treenode_deletebatch.json testcases/device/device_treenode/test_device_treenode_deletebatch.py
    pytest --reruns ${rCount} -v --html=${rDir}/13_test_device_treenode_move.html --json=${rDir}/13_test_device_treenode_move.json testcases/device/device_treenode/test_device_treenode_move.py
    pytest --reruns ${rCount} -v --html=${rDir}/13_test_device_treenode_nodeslist.html --json=${rDir}/13_test_device_treenode_nodeslist.json testcases/device/device_treenode/test_device_treenode_nodeslist.py
}

    # 设备树：设备挂载
run14(){
    pytest --reruns ${rCount} -v --html=${rDir}/14_test_device_devicetree_getUnmount.html --json=${rDir}/14_test_device_devicetree_getUnmount.json testcases/device/device_devicetree/test_device_devicetree_getUnmount.py
    pytest --reruns ${rCount} -v --html=${rDir}/14_test_device_devicetree_mountbatch.html --json=${rDir}/14_test_device_devicetree_mountbatch.json testcases/device/device_devicetree/test_device_devicetree_mountbatch.py
    pytest --reruns ${rCount} -v --html=${rDir}/14_test_device_devicetree_movebatch.html --json=${rDir}/14_test_device_devicetree_movebatch.json testcases/device/device_devicetree/test_device_devicetree_movebatch.py
    pytest --reruns ${rCount} -v --html=${rDir}/14_test_device_devicetree_unloadbatch.html --json=${rDir}/14_test_device_devicetree_unloadbatch.json testcases/device/device_devicetree/test_device_devicetree_unloadbatch.py
}

    # 设备ROI管理
run15(){
    pytest --reruns ${rCount} -v --html=${rDir}/15_test_device_behavior_roi_query.html --json=${rDir}/15_test_device_behavior_roi_query.json testcases/device/device_roi/test_device_behavior_roi_query.py
    pytest --reruns ${rCount} -v --html=${rDir}/15_test_device_behavior_roi_set.html --json=${rDir}/15_test_device_behavior_roi_set.json testcases/device/device_roi/test_device_behavior_roi_set.py
    pytest --reruns ${rCount} -v --html=${rDir}/15_test_device_output_roi_query.html --json=${rDir}/15_test_device_output_roi_query.json testcases/device/device_roi/test_device_output_roi_query.py
    pytest --reruns ${rCount} -v --html=${rDir}/15_test_device_output_roi_set.html --json=${rDir}/15_test_device_output_roi_set.json testcases/device/device_roi/test_device_output_roi_set.py
}

#  # 属性布控
#run16(){
#    pytest --reruns ${rCount} -v --html=${rDir}/16_test_monitor_add_propertymonitor.html --json=${rDir}/16_test_monitor_add_propertymonitor.json testcases/application/application_property_monitor/test_monitor_add_propertymonitor.py
##    pytest --reruns ${rCount} -v --html=${rDir}/16_test_monitor_edit_propertymonitor.html --json=${rDir}/16_test_monitor_edit_propertymonitor.json testcases/application/application_property_monitor/test_monitor_edit_propertymonitor.py
#    pytest --reruns ${rCount} -v --html=${rDir}/16_test_monitor_get_propertymonitor.html --json=${rDir}/16_test_monitor_get_propertymonitor.json testcases/application/application_property_monitor/test_monitor_get_propertymonitor.py
#    pytest --reruns ${rCount} -v --html=${rDir}/16_test_monitor_query_monitorproperty.html --json=${rDir}/16_test_monitor_query_monitorproperty.json testcases/application/application_property_monitor/test_query_monitor_property.py
#    pytest --reruns ${rCount} -v --html=${rDir}/16_test_property_monitor_add.html --json=${rDir}/16_test_property_monitor_add.json testcases/application/application_property_monitor/test_property_monitor_add.py
#    pytest --reruns ${rCount} -v --html=${rDir}/16_test_property_monitor_edit.html --json=${rDir}/16_test_property_monitor_edit.json testcases/application/application_property_monitor/test_property_monitor_edit.py
#
#}

  # 数据布控
run17(){
    pytest --reruns ${rCount} -v --html=${rDir}/17_test_data_monitor_add.html --json=${rDir}/17_test_data_monitor_add.json testcases/application/application_data_monitor/test_data_monitor_add.py
    pytest --reruns ${rCount} -v --html=${rDir}/17_test_data_monitor_control.html --json=${rDir}/17_test_data_monitor_control.json testcases/application/application_data_monitor/test_data_monitor_control.py
    pytest --reruns ${rCount} -v --html=${rDir}/17_test_data_monitor_delete.html --json=${rDir}/17_test_data_monitor_delete.json testcases/application/application_data_monitor/test_data_monitor_delete.py
    pytest --reruns ${rCount} -v --html=${rDir}/17_test_data_monitor_get.html --json=${rDir}/17_test_data_monitor_get.json testcases/application/application_data_monitor/test_data_monitor_get.py
    pytest --reruns ${rCount} -v --html=${rDir}/17_test_data_monitor_pages.html --json=${rDir}/17_test_data_monitor_pages.json testcases/application/application_data_monitor/test_data_monitor_pages.py
    pytest --reruns ${rCount} -v --html=${rDir}/17_test_data_monitor_update.html --json=${rDir}/17_test_data_monitor_update.json testcases/application/application_data_monitor/test_data_monitor_update.py
}

  # 数据报警
run18(){
    pytest --reruns ${rCount} -v --html=${rDir}/18_test_data_data_alarm.html --json=${rDir}/18_test_data_data_alarm.json testcases/data/data_data_alarm/test_data_data_alarm.py
}
run19(){
    pytest --reruns ${rCount} -v --html=${rDir}/19_test_struct_headshoulder_count.html --json=${rDir}/19_test_struct_headshoulder_count.json testcases/struct/struct_headshoulder/test_struct_headshoulder_count.py
    pytest --reruns ${rCount} -v --html=${rDir}/19_test_struct_headshoulder_density.html --json=${rDir}/19_test_struct_headshoulder_density.json testcases/struct/struct_headshoulder/test_struct_headshoulder_density.py
    pytest --reruns ${rCount} -v --html=${rDir}/19_test_struct_headshoulder_heatmap.html --json=${rDir}/19_test_struct_headshoulder_heatmap.json testcases/struct/struct_headshoulder/test_struct_headshoulder_heatmap.py
   # pytest --reruns ${rCount} -v --html=${rDir}/19_test_struct_statistic_dayCount.html --json=${rDir}/19_test_struct_statistic_dayCount.json testcases/struct/struct_statistic/test_struct_statistic_dayCount.py
    #pytest --reruns ${rCount} -v --html=${rDir}/19_test_struct_statistic_deviceDayCount.html --json=${rDir}/19_test_struct_statistic_deviceDayCount.json testcases/struct/struct_statistic/test_struct_statistic_deviceDayCount.py
    pytest --reruns ${rCount} -v --html=${rDir}/19_test_struct_clean.html --json=${rDir}/19_test_struct_clean.json testcases/ocean_init/test_struct_clean.py
}
run20(){
    #pytest --reruns ${rCount} -v --html=${rDir}/20_test_test_struct_statistic_allCount.html --json=${rDir}/20_test_test_struct_statistic_allCount.json testcases/struct/struct_statistic/test_struct_statistic_allCount.py
    pytest --reruns ${rCount} -v --html=${rDir}/20_test_struct_clean.html --json=${rDir}/20_test_struct_clean.json testcases/ocean_init/test_struct_clean.py
    pytest --reruns ${rCount} -v --html=${rDir}/20_test_struct_field_mapping_list.html --json=${rDir}/20_test_struct_field_mapping_list.json testcases/struct/struct_common/test_struct_field_mapping_list.py
    pytest --reruns ${rCount} -v --html=${rDir}/20_test_struct_correlation_search.html --json=${rDir}/20_test_struct_correlation_search.json testcases/struct/struct_common/test_struct_correlation_search.py

  }
   #终端新增删除（154版本未开放）
run21(){
    pytest --reruns ${rCount} -v --html=${rDir}/21_test_device_terminal_regist.html --json=${rDir}/21_test_device_terminal_regist.json testcases/terminal/test_device_terminal_regist.py
    pytest --reruns ${rCount} -v --html=${rDir}/21_test_device_terminal_delete.html --json=${rDir}/21_test_device_terminal_delete.json testcases/terminal/test_device_terminal_delete.py

}

#   # wifi探针设备管理(1.6.0.2新增)
#run22(){
#    pytest --reruns ${rCount} -v --html=${rDir}/22_test_wifiDevice_add.html --json=${rDir}/22_test_wifiDevice_add.json testcases/device/device_wifiDevice/test_wifiDevice_add.py
#    pytest --reruns ${rCount} -v --html=${rDir}/22_test_wifiDevice_edit.html --json=${rDir}/22_test_wifiDevice_edit.json testcases/device/device_wifiDevice/test_wifiDevice_edit.py
#    pytest --reruns ${rCount} -v --html=${rDir}/22_test_wifiDevice_delete.html --json=${rDir}/22_test_wifiDevice_delete.json testcases/device/device_wifiDevice/test_wifiDevice_delete.py
#    pytest --reruns ${rCount} -v --html=${rDir}/22_test_wifiDevice_get.html --json=${rDir}/22_test_wifiDevice_get.json testcases/device/device_wifiDevice/test_wifiDevice_get.py
#    pytest --reruns ${rCount} -v --html=${rDir}/22_test_wifiDevice_pages.html --json=${rDir}/22_test_wifiDevice_pages.json testcases/device/device_wifiDevice/test_wifiDevice_pages.py
#}
#
#   # wifi探针信息数据查询(1.6.0.2新增)
#run23(){
#    pytest --reruns ${rCount} -v --html=${rDir}/23_test_capture_wifi_gets.html --json=${rDir}/23_test_capture_wifi_gets.json testcases/struct/capture_wifi/test_capture_wifi_gets.py
#    pytest --reruns ${rCount} -v --html=${rDir}/23_test_capture_wifi_page.html --json=${rDir}/23_test_capture_wifi_page.json testcases/struct/capture_wifi/test_capture_wifi_page.py
#}

  # 头肩布控(1.6.0.2新增)
#run24(){
#    pytest --reruns ${rCount} -v --html=${rDir}/24_test_dispositions_headshoulder_add.html --json=${rDir}/24_test_dispositions_headshoulder_add.json testcases/application/application_dispositions_headshoulder/test_dispositions_headshoulder_add.py
#    pytest --reruns ${rCount} -v --html=${rDir}/24_test_dispositions_headshoulder_update.html --json=${rDir}/24_test_dispositions_headshoulder_update.json testcases/application/application_dispositions_headshoulder/test_dispositions_headshoulder_update.py
#    pytest --reruns ${rCount} -v --html=${rDir}/24_test_dispositions_headshoulder_pages.html --json=${rDir}/24_test_dispositions_headshoulder_pages.json testcases/application/application_dispositions_headshoulder/test_dispositions_headshoulder_pages.py
#    pytest --reruns ${rCount} -v --html=${rDir}/24_test_dispostions_delete.html --json=${rDir}/24_test_dispostions_delete.json testcases/application/application_dispositions_con/test_dispostions_delete.py
#    pytest --reruns ${rCount} -v --html=${rDir}/24_test_dispostions_status_edit.html --json=${rDir}/24_test_dispostions_status_edit.json testcases/application/application_dispositions_con/test_dispostions_status_edit.py
#}

run1
for sub_shell in $(seq 2 24);do
    run${sub_shell} &
    echo "正在执行run${sub_shell}"
done
wait
#exit 0
