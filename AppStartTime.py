#coding=utf-8

###########################################################
# FileName:AppStartTime.py
# Author:CathyZhang
# Date:2017-5-27
# Function Description: 获取app启动时间（首次启动、二次启动）
###########################################################

import os
import time
import platform


def get_activity():
    '''
    adb shell dumpsys activity top | findstr ACTIVITY
    获取当前界面的Activity
    '''
    activity = os.popen('adb shell dumpsys activity top | findstr ACTIVITY').readline().split()[1]

    return activity


def app_start_time(activity, startType, seek, num):
    '''
    启动应用命令： adb shell am start
    -S: force stop the target app before starting the activity
    -W: wait for launch to complete
    关闭应用命令： adb shell am force-stop pkgname
    '''

    if startType == '1st':
        cmd = 'adb shell am start -S -W -n ' + activity + ' | ' + seek + ' TotalTime'
        time_list = get_start_time(cmd, num)
        time_ave = sum(time_list) / len(time_list)
        print u'首次启动平均耗时： %d, 最大值： %d' % (time_ave, max(time_list))

    elif startType == '2nd':
        activity1 = get_activity()
        if activity1 == activity:
            os.popen('adb shell input keyevent 4')

        cmd = 'adb shell am start -W -n ' + activity + ' | ' + seek + ' TotalTime'
        time_list = get_start_time(cmd, num)
        time_ave = sum(time_list) / len(time_list)
        print u'二次启动平均耗时： %d, 最大值： %d' % (time_ave, max(time_list))

    else:
        print u'请检查选择的启动类型是否正确'


def get_start_time(cmd, num):
    n = 0
    time_list = []

    while n < int(num):
        total_time = os.popen(cmd).readline().split(':')[1]
        time_list.append(int(total_time))
        n += 1
        time.sleep(1)
        os.system('adb shell input keyevent 4')  # 按返回键

    print time_list
    return time_list


if __name__ == '__main__':

    if platform.system() == 'Windows':
        seek = 'findstr'

    else:
        seek = 'grep'
        
    raw_input(u'请启动被测应用，启动后按Enter键继续：')    # 此种编码方式在命令行下执行py文件时，中文显示为乱码
    # raw_input('请启动被测应用，启动后按Enter键继续：'.decode('utf-8').encode('gbk'))  # 此种方式在pycharm中执行脚本时，中文显示为乱码
    activity = get_activity()
    print activity
    startType = raw_input(u'计算首次启动时间请输入"1st"，计算二次启动时间请输入"2nd"输入后按Enter键继续: ')
    num = raw_input(u'请输入执行次数，按Enter键继续： ')

    app_start_time(activity, startType, seek, num)

