# -*- coding: utf-8 -*-

"""
@Remark: 自定义文件上传（JPEG、PNG、PDF、DOCX四种格式
"""
import base64
import json
import math
import os
import glob
import datetime
import traceback

import fitz
import pythoncom
from dateutil.relativedelta import relativedelta
from django.conf import settings

from utils.all2png import doc2pdf, pdf_image

from win32com.client import Dispatch
from utils.common import renameuploadimg, getfulldomian
from config import DOMAIN_HOST
from utils.ecloud_req import requests2ecloud
from utils.resumeparse import cvprase


def ImageUploadInstant(request, dirs):
    """
    request:请求
    dirs:要上传到那个目录
    """
    print("=============================#############################")
    print("====================先返回图片")
    print("=============================#############################")
    import time
    start_time = time.time()

    image = request.data.getlist('file')

    msg = {}
    if not image:
        print("文件不是图片格式")
        msg['code'] = 400
        msg['msg'] = "上传的图片不能为空"
        return msg

    notimg_file = []
    img_file = []
    try:

        # 多图片上传，也可单图片
        for img in image:

            img_name = img.name

            if not img.content_type.startswith('image/') and not img.content_type.startswith('application/'):
                msg['code'] = 400
                msg['msg'] = "请上传正确的文件格式"
                return msg

            if not img_name.endswith(
                    ('.jpg', '.jpeg', '.png', '.JPG', '.JPEG', '.PNG', '.docx', '.DOCX', '.pdf', '.PDF', '.DOC',
                     '.doc')):
                notimg_file.append(img_name)

            if img.size > 1024 * 500000:
                msg['code'] = 400
                msg['msg'] = "文件大小不能超过500M"
                return msg

            # 文件大小符合规范
            else:
                curr_time = datetime.datetime.now()
                # 对文件进行重命名
                image_name = renameuploadimg(img_name)

                time_path = curr_time.strftime("%Y-%m-%d")
                img_task_dir = dirs  # 对应models中的上传路径

                # print(image_name)  # 20230625164751_905.doc
                # 简历的单独文件夹名字 和重命名后的文件同名
                cv_pathname = image_name.split('.')[0]

                sub_path = os.path.join(settings.MEDIA_ROOT, img_task_dir, time_path, cv_pathname)
                # \Users\Clay_Guo\Desktop\【软件杯】\Base\django-vue-lyadmin\backend\media\platform\2023-06-25\20230625165209_744
                # print("sub_path", sub_path)

                if not os.path.exists(sub_path):
                    os.makedirs(sub_path)

                # 文件路径
                image_path = os.path.join(sub_path, image_name)
                print("image_path:", image_path)
                # print("image_path", image_path)
                # /media/platform/2023-06-25/20230625162928_846.doc
                # print("相对路径为：", settings.MEDIA_URL + img_task_dir + "/" + time_path + "/" + cv_pathname + "/" + image_name)

                # web_img_url = settings.MEDIA_URL + img_task_dir + "/" + time_path + "/" + image_name#相对路径/media/xxx/xxxx/xxx.png
                web_img_url = DOMAIN_HOST + settings.MEDIA_URL + img_task_dir + "/" + time_path + "/" + cv_pathname + "/" + image_name  # 绝对路径http://xxx.xxx.com/media/xxx/xxxx/xxx.png
                f = open(image_path, 'wb')
                for i in img.chunks():
                    f.write(i)
                f.close()
                img_file.append(web_img_url)

                # print("跳过检查点4—— 开始对简历进行处理")
                # 对上传之后的简历进行处理
                """        
                首先将各种格式的简历统一处理成png格式
                png格式调用移动OCR进行识别
                将识别结果以json格式进行保存  json-->txt  By 许逸非
                PaddleNLP进行 NER                      By 徐旸
                将年龄、工作年限等信息进行处理             By 郭寅之
                将相应的结果返回给前端
                前端进行渲染到相应的文本框中
                用户点击确认，完成此简历的自动录入
                """
                # 读取简历，判断格式 all2png
                # doc docx ---> pdf   转化为PDF  重写一份保存
                # print("img_file[0]", img_file[0])
                res_data = {}
                img_data = []
                ##############################
                # 处理doc和docx文件
                ##############################
                if img_file[0].endswith(('.doc', '.docx', '.DOC', '.DOCX')):
                    # pass
                    # 有问题 【已解决】 引入pythoncom.CoInitialize() 这是COM编程必须引入的一个对象
                    #################################################################
                    # 给一个绝对路径
                    # 将doc文件保存为一个同名的.pdf文件
                    # convert(image_path, image_path.replace("docx", "pdf"))
                    doc2pdf(image_path)
                    # print("!!!!!!!!!!!!!!!!!!!!!!!!!!!{}文档已转换为PDF".format(img_file[0]))
                    # doc2pdf处理完毕，得到最终 pdf-->PNG
                    # 简历过来  先创建一个同门文件夹，其余内容都存到其文件夹
                    #
                    # pdf的实际路径（后续操作都是对这个路径进行操作
                    pdfPath = sub_path + "\\" + image_name.replace(".docx", ".pdf").replace(".doc", ".pdf")

                    # print("PDF文件路径为", pdfPath)
                    ################################################################
                    # 处理PDF
                    proc_pdf(sub_path, pdfPath)

                    file_list = glob.glob(os.path.join(sub_path, "*.png"))
                    for i in range(len(file_list)):
                        img_url = DOMAIN_HOST + settings.MEDIA_URL + img_task_dir + "/" + time_path + "/" + cv_pathname + "/" + str(
                            i) + ".png"
                        img_data.append(img_url)
                    res_data['img_list'] = img_data
                    res_data[
                        'cv_img'] = DOMAIN_HOST + settings.MEDIA_URL + img_task_dir + "/" + time_path + "/" + cv_pathname + "/" + "0.png"

                    res_data['path'] = sub_path  # 返回对应的文件夹路径方便fileupload中读取到刚上传的文件

                    msg['code'] = 200
                    msg['zzz'] = res_data
                    msg['msg'] = '上传成功'
                    print("=============================#############################")
                    print("图片SUCCESS 返回成功")
                    print("=============================#############################")
                    return msg
                ##############################
                # jpg --> png
                # 处理jpg文件
                ##############################
                elif img_file[0].endswith(('jpg', 'jpeg', 'JPG', 'JPEG')):
                    ####################################################
                    # 处理JPG
                    ####################################################
                    img_url = [
                        DOMAIN_HOST + settings.MEDIA_URL + img_task_dir + "/" + time_path + "/" + cv_pathname + "/" + cv_pathname + ".jpg"]

                    res_data['img_list'] = img_url
                    res_data[
                        'cv_img'] = DOMAIN_HOST + settings.MEDIA_URL + img_task_dir + "/" + time_path + "/" + cv_pathname + "/" + cv_pathname + ".jpg"

                    res_data['path'] = sub_path  # 返回对应的文件夹路径

                    msg['code'] = 200
                    msg['zzz'] = res_data
                    msg['msg'] = '上传成功'
                    print("=============================#############################")
                    print("图片SUCCESS 返回成功")
                    print("=============================#############################")
                    end_time_png = time.time()
                    print("上传图片总耗时：", end_time_png - start_time)
                    return msg
                ##############################
                # 处理PDF文件 转化为图片
                ##############################
                elif img_file[0].endswith(('.pdf', '.PDF')):
                    # 处理PDF PDF-->PNG
                    proc_pdf(sub_path, image_path)
                    print("***************")
                    print(" PDF转PNG 成功!")
                    print("***************")

                    file_list = glob.glob(os.path.join(sub_path, "*.png"))
                    for i in range(len(file_list)):
                        img_url = DOMAIN_HOST + settings.MEDIA_URL + img_task_dir + "/" + time_path + "/" + cv_pathname + "/" + str(
                            i) + ".png"
                        img_data.append(img_url)
                    res_data['img_list'] = img_data
                    res_data[
                        'cv_img'] = DOMAIN_HOST + settings.MEDIA_URL + img_task_dir + "/" + time_path + "/" + cv_pathname + "/" + "0.png"

                    res_data['path'] = sub_path  # 返回对应的文件夹路径

                    msg['code'] = 200
                    msg['zzz'] = res_data
                    msg['msg'] = '上传成功'
                    print("=============================#############################")
                    print("图片SUCCESS 返回成功")
                    print("=============================#############################")
                    end_time_pdf = time.time()
                    print("处理PDF简历总耗时：", end_time_pdf - start_time)
                    return msg
                ##############################
                # 如果是PNG图片 直接向前端返回即可
                ##############################
                elif img_file[0].endswith(('.PNG', '.png')):
                    img_url = [
                        DOMAIN_HOST + settings.MEDIA_URL + img_task_dir + "/" + time_path + "/" + cv_pathname + "/" + cv_pathname + ".png"]

                    res_data['img_list'] = img_url
                    res_data[
                        'cv_img'] = DOMAIN_HOST + settings.MEDIA_URL + img_task_dir + "/" + time_path + "/" + cv_pathname + "/" + cv_pathname + ".png"

                    res_data['path'] = sub_path  # 返回对应的文件夹路径

                    msg['code'] = 200
                    msg['zzz'] = res_data
                    msg['msg'] = '上传成功'
                    print("=============================#############################")
                    print("图片SUCCESS 返回成功")
                    print("=============================#############################")
                    end_time_png = time.time()
                    print("上传图片总耗时：", end_time_png - start_time)
                    return msg
                else:
                    print("进入到else里面去了")

                print("跳过检查点5—— 简历处理完毕")

        if notimg_file:
            msg['code'] = 400
            msg['msg'] = '请检查是否支持的文件，失败文件部分如下：{0}'.format(','.join(notimg_file[:10]))
            return msg
        start_time_xy = time.time()
        end_time = time.time()
        xy_time = end_time - start_time_xy
        total_time = end_time - start_time

        res_data[
            'cv_img'] = DOMAIN_HOST + settings.MEDIA_URL + img_task_dir + "/" + time_path + "/" + cv_pathname + "/" + "0.png"
        print("XY程序总运行时间是{}秒".format(xy_time))
        print("总运行时间是{}秒".format(total_time))

        msg['code'] = 200
        msg['zzz'] = res_data
        msg['img'] = res_data  # ['/media/xxx/xxx/xxx.png']
        msg['msg'] = '上传成功'
        return msg

    except Exception as e:
        print("发生异常：", str(e))
        traceback.print_exc()
        msg['code'] = 400
        msg['msg'] = '上传失败'
        return msg


def proc_pdf(sub_path, filepath):
    # 打开PDF文件
    pdf = fitz.open(filepath)
    # 逐页读取PDF
    for pg in range(0, pdf.page_count):
        page = pdf[pg]
        # 设置缩放和旋转系数
        trans = fitz.Matrix(4, 4).prerotate(0)
        pm = page.get_pixmap(matrix=trans, alpha=False)
        # 开始写图像
        pm.save(sub_path + '\\' + str(pg) + ".png")

    pdf.close()
    # print("======PDF转PNG结束………………………………………………………")
    res = "SUCCESS"
    return res
