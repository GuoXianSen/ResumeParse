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
# from utils.post.match import match_job
# from utils.post.match import *
from utils.resumeparse import cvprase


def FileUpload(request, dirs):
    """
    request:请求
    dirs:要上传到那个目录
    """
    import time
    start_time = time.time()
    print("==========================现在开始简历解析部分************************")
    # 获取从前端上传的文件
    image = request.data.getlist('file')
    # 指定刚刚已经生成的文件夹路径，避免重复生成该路径格式为列表
    need_path = request.data.getlist('path')
    # print("*************************************")
    # print("简历路径为：", need_path)
    # C:\\Users\\Clay_Guo\\Desktop\\【软件杯】\\Base\\django-vue-lyadmin\\backend\\media\\platform\\2023-07-14\\20230714165611_308
    # print("格式为：", type(need_path))
    # print("*************************************")
    # 拼接需要修改的路径和文件与文件名

    msg = {}

    notimg_file = []
    img_file = []

    try:
        # 多图片上传，也可单图片 | 目前是上传单个文件
        for img in image:
            # 文件名就是上传的文件是啥名就是啥 例如 16.docx
            img_name = img.name
            need_cv = need_path[0] + "\\" + need_path[0].split('\\')[-1] + "." + img_name.split('.')[-1]
            print("*************************************")
            # C:\Users\Clay_Guo\Desktop\【软件杯】\Base\django-vue-lyadmin\backend\media\platform\2023-07-14\20230714201219_812\20230714201219_812.docx
            print("need_cv 最终的简历的路径为", need_cv)
            print("need_cv 最终的简历的路径为", type(need_cv))
            print("*************************************")
            # 图片类型content-type检查
            if not img.content_type.startswith('image/') and not img.content_type.startswith('application/'):
                print("***************")
                print("！！！文件格式错误")
                print("***************")
                msg['code'] = 400
                msg['msg'] = "请上传正确的文件格式"
                return msg

            print("***************")
            print("文件格式正确")
            print("***************")

            if not img_name.endswith(
                    ('.jpg', '.jpeg', '.png', '.JPG', '.JPEG', '.PNG', '.docx', '.DOCX', '.pdf', '.PDF', '.DOC',
                     '.doc')):
                notimg_file.append(img_name)
            # 文件大小校验
            if img.size > 1024 * 500000:
                msg['code'] = 400
                msg['msg'] = "文件大小不能超过500M"
                return msg
            else:
                curr_time = datetime.datetime.now()
                # 对文件进行重命名  重命名后的文件名如20230625164751_905.doc 时间戳_随机数
                image_name = renameuploadimg(img_name)
                print("$$$$$$$$$$$$$$$$$$$$image_name", image_name, need_path[0].split('\\')[-1])
                # 时间路径 用于创建的当天的文件夹 参考微信文件保存方式
                time_path = curr_time.strftime("%Y-%m-%d")

                img_task_dir = dirs  # 对应models中的上传路径

                # 简历的单独文件夹名字 和重命名后的文件同名 【一份简历保存到一份文件夹中】
                cv_pathname = image_name.split('.')[0]
                ############################################
                ############################################
                ############################################
                # 从这里开始的sub_path 就没有用了
                ############################################
                ############################################
                ############################################
                # \Users\Clay_Guo\Desktop\【软件杯】\Base\django-vue-lyadmin\backend\media\platform\2023-06-25\20230625165209_744
                sub_path = os.path.join(settings.MEDIA_ROOT, img_task_dir, time_path, cv_pathname)

                # if not os.path.exists(sub_path):
                #     os.makedirs(sub_path)

                # 文件绝对路径 C:\Users\Clay_Guo\Desktop\【软件杯】\Base\django-vue-lyadmin\backend\media\platform\2023-07-14\20230714201229_865\20230714201229_865.docx
                image_path = os.path.join(sub_path, image_name)
                print("image_path", image_path)
                # /media/platform/2023-06-25/20230625162928_846.doc
                print("相对路径为：",
                      settings.MEDIA_URL + img_task_dir + "/" + time_path + "/" + cv_pathname + "/" + image_name)

                # web_img_url = settings.MEDIA_URL + img_task_dir + "/" + time_path + "/" + image_name#相对路径/media/xxx/xxxx/xxx.png
                web_img_url = DOMAIN_HOST + settings.MEDIA_URL + img_task_dir + "/" + time_path + "/" + cv_pathname + "/" + image_name  # 绝对路径http://xxx.xxx.com/media/xxx/xxxx/xxx.png
                # http://127.0.0.1:8000/media/platform/2023-07-14/20230714195519_290/20230714195519_290.docx
                # print("web_img_url", web_img_url)
                # 以二进制模式读写入文件 | 现在可以不用写入这个文件了
                # f = open(image_path, 'wb')
                # for i in img.chunks():
                #     f.write(i)
                # f.close()
                img_file.append(web_img_url)
                # print("img_file[0]", img_file[0])
                # img_file[0] http://127.0.0.1:8000/media/platform/2023-07-14/20230714201229_865/20230714201229_865.docx
                # print("////////////////////img_file", img_file, type(img_file))////////////////////img_file

                print("*************************************")
                print("开始对简历进行处理")
                print("*************************************")
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

                # 处理之前拿到的文件夹的数据
                # need_cv是文件的绝对路径
                # need_path[0] 是简历所在文件夹路径
                #

                ##############################
                # 处理doc和docx文件
                ##############################
                if need_cv.endswith(('.doc', '.docx', '.DOC', '.DOCX')):
                    # pass
                    # 有问题 【已解决】 引入pythoncom.CoInitialize() 这是COM编程必须引入的一个对象
                    #################################################################
                    # 给一个绝对路径
                    # 将doc文件保存为一个同名的.pdf文件
                    # 发生异常： (-2147352567, '发生意外。', (
                    # 0, 'Microsoft Word', '很抱歉，找不到您的文件。该项目是否已移动、重命名或删除?\r (C:\\...\\20230714211345_623202307142113...)',
                    # 'wdmain11.chm', 24654, -2146823114), None)

                    # doc2pdf(need_cv)
                    # PDF网络地址
                    #

                    # 注意 这里如果直接将pdfPath=need_cv 那么会导致pdfPath 和need_cv 指向同一个地址 引用同一个对象，修改一个会导致另一个也被修改
                    pdfPath = need_cv[:]
                    pdfPath = pdfPath.replace(".docx", ".pdf").replace(".doc", ".pdf")
                    # print("!!{}文档已转换为PDF".format(pdfPath))
                    print("PDF文件路径为", pdfPath)
                    # doc2pdf处理完毕，得到最终 pdf-->PNG
                    # 简历过来  先创建一个同门文件夹，其余内容都存到其文件夹
                    #
                    # pdf的实际路径（后续操作都是对这个路径进行操作
                    # pdfPath = sub_path + "\\" + image_name.replace(".docx", ".pdf").replace(".doc", ".pdf")
                    ################################################################
                    # 处理PDF 参数 文件夹路径和PDF的绝对路径
                    # proc_pdf(need_path[0], pdfPath)
                    # print("@@@@@@@@@@@@@@@@@ PDF转PNG 成功!")
                    start_time_pdf2png = time.time()

                    ####################################################
                    # 处理PNG 参数（文件夹路径、图片路径
                    proc_img(need_path[0], need_cv, image_name)
                    ####################################################
                    start_time_xy = time.time()
                    print("OCR时间为：", start_time_xy - start_time_pdf2png)
                    res_data = proc_cal(need_cv, img_name)

                ##############################
                # jpg --> png
                # 处理jpg文件
                ##############################
                elif img_file[0].endswith(('jpg', 'jpeg', 'JPG', 'JPEG')):
                    houzhui = os.path.splitext(img_name)[1]
                    print("后缀为：", houzhui)
                    ####################################################
                    # 处理JPG
                    proc_img(sub_path, image_path, image_name, houzhui)
                    ####################################################
                    start_time_xy = time.time()
                    res_data = proc_cal(image_path, img_name)
                ##############################
                # 处理PDF文件 转化为图片
                ##############################
                elif img_file[0].endswith(('.pdf', '.PDF')):
                    # 处理PDF
                    # proc_pdf(sub_path, image_path)
                    # print("@@@@@@@@@@@@@@@@@ PDF转PNG 成功!")
                    ####################################################
                    # 处理PNG  文件夹路径
                    start_time_ocr = time.time()
                    proc_img(need_path[0], need_cv, need_path[0].split('\\')[-1] + "." + img_name.split('.')[-1])
                    ####################################################
                    start_time_xy = time.time()
                    print("PDF简历文件上传时ORC所需时间，", start_time_xy - start_time_ocr)
                    res_data = proc_cal(need_cv, need_path[0].split('\\')[-1] + "." + img_name.split('.')[-1])
                    end_time_xy = time.time()
                    print("PDF简历文件上传时ORC所需时间，", end_time_xy - start_time_xy)
                ##############################
                # 处理PNG图片 直接进行OCR
                ##############################
                elif img_file[0].endswith(('.PNG', '.png')):
                    start_time_ocr = time.time()
                    proc_img(need_path[0], need_cv, need_path[0].split('\\')[-1] + "." + img_name.split('.')[-1])
                    start_time_xy = time.time()
                    print("PNG简历文件上传时ORC所需时间，", start_time_xy - start_time_ocr)
                    res_data = proc_cal(need_cv, need_path[0].split('\\')[-1] + "." + img_name.split('.')[-1])
                    print("==========================================================")
                    print(res_data)
                    # print(job_math(res_data['姓名']))
                    print("==========================================================")

                    end_time_xy = time.time()
                    print("NER时间，", end_time_xy - start_time_xy)
                    # job_match

                else:
                    print("进入到else里面去了")

                # print("跳过检查点5—— 简历处理完毕")

        if notimg_file:
            msg['code'] = 400
            msg['msg'] = '请检查是否支持的文件，失败文件部分如下：{0}'.format(','.join(notimg_file[:10]))
            return msg

        end_time = time.time()
        xy_time = end_time - start_time_xy
        total_time = end_time - start_time

        # res_data['cv_img'] = need_cv
        print("==========================================================")
        print(res_data)
        # print(type(res_data), type(res_data["cv_img"]))
        print("==========================================================")
        print("XY程序总运行时间是{}秒".format(xy_time))
        print("总运行时间是{}秒".format(total_time))

        msg['code'] = 200
        msg['zzz'] = res_data
        # msg['img'] = res_data  # ['/media/xxx/xxx/xxx.png']
        msg['msg'] = '上传成功'
        return msg

    except Exception as e:
        print("发生异常：", str(e))
        traceback.print_exc()
        msg['code'] = 400
        msg['msg'] = '上传失败'
        return msg


def ImageUpload2(request, paramsname, dirs):
    """
    根据指定的名称参数名获取上传的文件
    request:请求
    paramsname:为formData中提交数据的名称
    dirs:要上传到那个目录
    """
    image = request.data.getlist(paramsname)
    msg = {}
    if not image:
        msg['code'] = 400
        msg['msg'] = "上传的图片不能为空"
        return msg

    notimg_file = []
    img_file = []
    try:
        # 多图片上传，也可单图片
        for img in image:
            img_name = img.name
            # 图片类型content-type检查
            if not img.content_type.startswith('image/'):
                msg['code'] = 400
                msg['msg'] = "请上传正确的图片格式"
                return msg

            if not img_name.endswith(
                    ('.jpg', '.jpeg', '.png', 'gif', '.bmp', '.JPG', '.JPEG', '.PNG', 'GIF', '.BMP')):
                notimg_file.append(img_name)

            if img.size > 1024 * 50000:
                msg['code'] = 400
                msg['msg'] = "图片大小不能超过50M"
                return msg

            else:
                curr_time = datetime.datetime.now()
                image_name = renameuploadimg(img_name)
                time_path = curr_time.strftime("%Y-%m-%d")
                img_task_dir = dirs  # 对应models中的上传路径
                sub_path = os.path.join(settings.MEDIA_ROOT, img_task_dir, time_path)
                if not os.path.exists(sub_path):
                    os.makedirs(sub_path)
                image_path = os.path.join(sub_path, image_name)
                # web_img_url = settings.MEDIA_URL + img_task_dir + "/" + time_path + "/" + image_name#相对路径/media/xxx/xxxx/xxx.png
                web_img_url = DOMAIN_HOST + settings.MEDIA_URL + img_task_dir + "/" + time_path + "/" + image_name  # 绝对路径http://xxx.xxx.com/media/xxx/xxxx/xxx.png
                f = open(image_path, 'wb')
                for i in img.chunks():
                    f.write(i)
                f.close()
                img_file.append(web_img_url)

        if notimg_file:
            msg['code'] = 400
            msg['msg'] = '请检查是否支持的图片，失败文件部分如下：{0}'.format(','.join(notimg_file[:10]))
            return msg

        msg['code'] = 200
        msg['img'] = img_file  # ['/media/xxx/xxx/xxx.png']
        msg['msg'] = '上传成功'
        return msg

    except Exception as e:
        msg['code'] = 400
        msg['msg'] = '图片上传失败'
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
    print("======PDF转PNG结束………………………………………………………")
    res = "SUCCESS"
    return res


"""
image_path是去文件绝对路径
"""


def proc_img(sub_path, image_path, image_name, houzhui=".png"):
    ####################################################
    # PNG ---> JSON
    myhouzhui = "*" + houzhui
    file_list = glob.glob(os.path.join(sub_path, myhouzhui))
    text = []
    for file in file_list:
        # print(file)
        # 读取图片文件
        image = open(file, "rb")
        image_bytes = image.read()

        # png转base64编码
        image_base64 = base64.b64encode(image_bytes)
        # print("image_base64图片的base64编码为：", image_base64)
        if isinstance(image_base64, bytes):
            image_base64 = str(image_base64, encoding='utf-8')
        image.close()

        # 发送ocr请求
        res = requests2ecloud(image_base64,
                              access_key="3d15919ed577490a831b0339d217e31e",
                              secret_key="b469dcb9ae92428eb0618b2697098062")

        # print("开始写入Json……")
        # 结果存成临时json
        f2 = open(sub_path + "\\" + "temp_json.json", 'w', encoding="utf-8")
        f2.write(res)
        f2.close()
        # print("Json……写入成功")

        f = open(sub_path + "\\" + "temp_json.json", 'r', encoding="utf-8")
        content = f.read()
        res = json.loads(content)
        f.close()
        word_pos = {}
        page_list = []

        # 提取json中需要的部分
        if 'body' in res:
            body = res['body']
            content = body['content']
            prism_wordsInfo = content['prism_wordsInfo']

            for k in range(len(prism_wordsInfo)):
                block = prism_wordsInfo[k]
                position = block['position']
                word = block['word']
                word_pos[word] = position
        page_list.append(word_pos)

        img_json = {image_name: page_list}
        b = json.dumps(img_json)

        # 保存json
        # mkdir(i.replace(base, result_path).replace(png_name, ''))
        f2 = open(file.replace('.png', '.json'), 'w')
        # print(f2)
        f2.write(b)
        f2.close()

    # 删除temp文件
    os.remove(sub_path + "\\" + "temp_json.json")

    file_list = glob.glob(os.path.join(sub_path, "*.json"))

    for file in file_list:
        # print("file", file)
        f = open(file, 'r')
        content = f.read()
        # 文件夹下所有json
        res = json.loads(content)

        for key, value in res.items():
            temp_text = list(value[0].keys())
        text = text + temp_text

    txt_path = image_path.lower().replace('.docx', '.txt').replace('.pdf', '.txt').replace('.png', '.txt').replace(
        '.jpg', '.txt')
    print("txt路径：", txt_path)
    txtfile = open(txt_path, "w", encoding='utf-8')
    # print(textname)
    for txt in text:
        # 文字信息
        txtfile.write(txt + " ")
    txtfile.close()
    print("##################################")
    print("txt文件写入成功……")
    # print(txtfile)
    print("##################################")


def proc_cal(image_path, img_name):
    ################################################################
    # 徐旸代码功能 命名实体识别
    # 这里需要注意，如果上传的是doc文件将出问题，需要改动【20230712已完成】
    ################################################################
    image_path = image_path.lower().replace('.docx', '.txt').replace('.pdf', '.txt').replace('.png', '.txt').replace(
        '.jpg', '.txt')
    text = open(image_path, "r", encoding='utf-8')
    print("**********************文件打开成功")
    txt = text.read()
    res_data = cvprase(txt, img_name)
    # print("text", text, img_name)
    print("res_data:", res_data)

    print(type(res_data))

    if not res_data['年龄']:
        print("###############################")
        print("简历中无年龄信息 需人工计算")
        print("###############################")
        if not res_data["出生日期"]:
            res_data['年龄'] = 0
        res_data['年龄'] = int(datetime.datetime.now().year) - int(res_data['出生日期'][:4]) + 1

    if "岁" in str(res_data["年龄"]):
        res_data["年龄"] = res_data["年龄"].split("岁")[0]

    # 计算工作年限
    total_year = 0
    work_years = 0
    work_month = 0
    try:
        for work_time in res_data['工作时间']:
            print(work_time)
            if '-' in work_time and "至今" not in work_time:
                time1, time2 = work_time.split('-')
                # print(time1, time2)

                # 定义起始日期和结束日期
                start_date = datetime.datetime.strptime(time1, '%Y.%m')
                end_date = datetime.datetime.strptime(time2, '%Y.%m')

                # 计算工作年限
                delta = relativedelta(end_date, start_date)

                work_years += delta.years
                work_month += delta.months
                print("这段工作时间的年限为", work_years, work_month)

                total_year += work_years
            elif "至今" in work_time and "-" not in work_time:
                time1 = work_time.split('至今')[0]
                print("time1的时间为：", time1)

                # 获取当前日期和时间
                now = datetime.datetime.now()

                # 格式化为指定的数据格式
                time2 = now.strftime("%Y.%m")

                print("time2的时间为", time2)
                # 定义起始日期和结束日期
                start_date = datetime.datetime.strptime(time1, '%Y.%m')
                end_date = datetime.datetime.strptime(time2, '%Y.%m')

                # 计算工作年限
                delta = relativedelta(end_date, start_date)
                work_years += delta.years
                work_month += delta.months
                print("这段工作时间的年限为", work_years, work_month)
                # total_year += work_years
            elif "至今" in work_time and "-" in work_time:
                time1 = work_time.split('-')[0]
                print("time1的时间为：", time1)

                # 获取当前日期和时间
                now = datetime.datetime.now()

                # 格式化为指定的数据格式
                time2 = now.strftime("%Y.%m")

                # print("time2的时间为", time2 )
                # 定义起始日期和结束日期
                start_date = datetime.datetime.strptime(time1, '%Y.%m')
                end_date = datetime.datetime.strptime(time2, '%Y.%m')

                # 计算工作年限
                delta = relativedelta(end_date, start_date)
                work_years += delta.years
                work_month += delta.months
                print("这段工作时间的年限为", work_years, work_month)

        total_year = work_years + math.ceil(work_month / 12)
        print("{}的总的工作年限为{}".format(res_data['姓名'], total_year))
        res_data['工作年限'] = total_year
    except Exception as e:
        print("发生异常：", str(e))
        traceback.print_exc()
        res_data['工作年限'] = 0
    return res_data

# 632 行
