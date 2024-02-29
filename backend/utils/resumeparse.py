# -*- coding: utf-8 -*-
import json
import math
import os
import datetime
from pprint import pprint

from dateutil.relativedelta import relativedelta
from paddlenlp import Taskflow

'''
pip install paddlenlp
pip install LAC

'''


# ocrjson文件转列表 path为文件夹地址
def readOCRjson(path):
    cvs = []
    files = os.listdir(path)
    for filename in files:
        if filename.endswith(".json"):
            with open(path + filename, 'r', encoding='utf-8') as fp:
                cv = json.load(fp)
                cvs.append(cv)
    return cvs


# 判断文字框是否在同一行
def is_samerow(posa, posb):
    # 左上，右上，右下，左下
    xa = []
    ya = []
    xb = []
    yb = []
    for index in posa:
        xa.append(index["x"])
        ya.append(index["y"])
    for index in posb:
        xb.append(index["x"])
        yb.append(index["y"])
    # 首先检查文本框是否为水平方向
    if is_horizontal(posa) == "horizontal" and is_horizontal(posa) == is_horizontal(posb):
        # 判断是否在同一行中,且字体高度一致(误差不超过5)
        if abs(yb[0] - ya[0]) < 5 and abs(yb[3] - ya[3]) < 5:
            return True
        else:
            return False
    return False


# 判断文本框是否属于同一列


# 判断文字方向（上下方向 左右方向）
def is_horizontal(pos):
    # 左上，右上，右下，左下
    x = []
    y = []
    for index in pos:
        x.append(index["x"])
        y.append(index["y"])
    # 长大于宽则为左右顺序，否则为上下顺序，单个字默认为左右顺序
    if (x[1] - x[0] > y[2] - y[1]):
        return "horizontal"
    else:
        return "vertical"


def get_info(text, ie, filename):
    # 将整理后的抽取结果返回为字典
    schema_dict = {}
    schema_dict["文件名"] = filename
    # 抽取简历信息
    a = ie(text)
    for i in schema:
        if i in a[0]:
            if i == "工作时间":
                schema_dict[i] = []
                for j in range(0, len(a[0][i])):
                    schema_dict[i].append(a[0][i][j]["text"])
            else:
                schema_dict[i] = a[0][i][0]['text']

        else:
            schema_dict[i] = ''
    return schema_dict


# 直接txt转化为关键信息字典
def txt2json(txtpath, ie):
    result = []
    files = os.listdir(txtpath)
    for filename in files:
        if filename.endswith(".txt"):
            text = ""
            with open(txtpath + filename, 'r', encoding='utf-8') as fp:
                text = fp.read()

            result.append(get_info(text, ie, filename))
            print(get_info(text, ie, filename))
    return result


"""
单个简历--->

"""


# OCRjson数据转为txt文件
def ocrjson2txt(cvs):
    jsons = []
    # 简历页数
    for cv in cvs:
        text = []
        for page in cv:
            TXTpath = r'.\train_data'
            savepath = TXTpath + "\\" + page + ".txt"
            res = ''
            txtfile = open(savepath, "w", encoding='utf-8')
            # 文字框列表
            for pos in cv[page]:
                # 单个文字框为字典，key为文本，value为坐标信息
                for txt in pos:
                    # 文字信息
                    txtfile.write(txt + " ")


# 保存txt文件的地址
text = """生日：1995.04.06 地址：上海浦东新区 郭芳天 电话:13800138000 求职目标：市场总监-专注品牌 邮箱：service@500d.me 教育背景 2013.07-2017.06 上海外国语大学 市场营销（本科) 主修课程：管理学、微观经济学、宏观经济学、管理信息系统、统计学、会计学、财务管理、市场营销、经济法、消费者 行为学、国际市场营销。 校园实践 2014.05-2017.06 辩论队（队长） 内容描述： 负责50余人团队的日常训练、选拔及团队建设； 作为负责人对接多项商业校园行活动，如《奔跑吧兄弟》上海外国语大学站录制、《时代周末》校园行 斗寻圈/Y祟间 2014.11-2017.06 沟通与交流协会 协助上海沟通协会创立上海外国语大学分部，从零开始组建初期团队 策划协会会员制，选拔、培训协会导师，推出一系列沟通课程。 工作经历 2019.12-至今 翔汇投资控股集团 副总监 工作描述： 负责协助集团旗下事业部开展各项工作，制定品牌传播方案； 结合集团与事业部发展，制定营销策略、广告策略、品牌策略和公关策略，并组织推进执行 制定和执行媒体投放计划，跟踪和监督媒体投放效果，进行数据分析与撰写报告 研究行业发展动态，定期进行市场调查,为产品更新提供建议 2018.12-2019.12 市场及运营总监 源清设计有限公司 工作描述 根据公司发展情况进行战略调整，配合前端销售部门搭建销售渠道 研究行业发展动态，定期进行市场调查,为产品更新提供建议； 负责公司部门(营运、品牌策划)制度规范，负责组织及监管市场部关于对外合作、推广策划以相关工作的落实 2017.12-2018.12 市场副总监 枫辰设计俱乐部 负责事业部产品对外推广和宣传，制定各种整合营销的活动； 执行媒体投放计划，跟踪和监督媒体投放效果，进行数据分析撰写报告 向市场总监提供营销支持，并协助相关的公关事宜。 项目经历 枫辰设计设计集团品牌升级发布会 集团全新品牌logo及VI上线，在多渠道进行了传播； 企业VIP客户群体逾60人，结合了线上发布、线下体验 后续媒体报道持续升温，子品牌结合明星代言人制造话题营销，为期3周 源清设计设计商业模式发布会 整场活动以会议＋洽谈双重模式进行，首日以介绍源清内部平台资源优势，政府背景优势等为主，一对多推介会进行推 广普及； 现场签署地方合作意向书，如：新疆、江西、浙江等优秀企业商户 以中国的波尔多为宣传点，主推旗下新疆大型项目，制造营销、品牌热点 翔汇投资控股集团6A自媒体生态圈建设 本项目重构了公司现有微信企业号的功能与架构。 提高公众号的关注粉丝量的同时，对于有客户进行统一宣传，统一管理 奖项荣誉 2016年新长城上海外国语大学自强社优秀社员 2015年三下乡"社会实践活动《优秀学生* 2015年上海外国语大学学生田经运动会10人立定跳远团体赛第三名 2015年学生军事技能训练《优秀学员 2015年上海外国语大学盼盼杯烘焙食品创意大赛优秀奖 2014年高校大学生主题征文一等奖 2014年上海外国语大学青春"微博文征集大赛二等奖 技能证书 普通话一级甲等 通过全国计算机二级考试，熟练运用office相关软件。 熟练使用绘声绘色软件，剪辑过各种类型的电影及班级视频 大学英语四/六级（CET-4/6），良好听说读写能力，快速浏览英语专业书籍 兴趣爱好 阅读/旅行/跑步羽毛球/爬山烹饪 自我评价 拥有多年的市场管理及品牌营销经验，卓越的规划、组织、策划、方案执行和团队领导能力，积累较强的人际关系处理能 力和商务谈判技巧，善于沟通，具备良好的合作关系掌控能力与市场开拓能力； 敏感的商业和市场意识，具备优秀的资源整合能力、业务推进能力； 思维敏捷，有培训演讲能力，懂激励艺术，能带动团队的积极性；擅长协调平衡团队成员的竞争与合作的关系，善于通过 培训提高团队综合能力和凝聚力 """
text2 = """郭寅之 15061131871guoyinzhi@foxmail.com https://guoxia isen.github.io 当24岁 中共党员 教育经历 南京邮电大学 2022.092025.06 电子信息硕士计算机学院、软件学院、网络空间安全学院 南京 相关课程：随机过程（95）、最优化方法(94)、算法分析与设计(90 常州工学院 2017.092021.06 软件工程本科计算机信息工程学院 常州 GPA:4.2/5(专业前4‰3/90） 实习经历 博世创新与软件开发中心 2021.03-2021.05 SoftwareEngIneeringInternPjM 无锡 PS 开发环境：Java、IDEA、MySQL8.0、小程序、SourceTree、Git.thymeleaf、Bibucke 项目描述：项目名为Co npetenceMaster，对BCSC员工CoC技能与当前正在开发的项目进行统计与 可视化，方便进行项目人员人岗匹配 工作内容:参与了项目中的需求分析、设计和开发工作。后端开发中，使用Spr ng框架和MyBatis实现 id连接池来管理数据库连 了与数据库的交互，负责搭建和维护项目中的数据库连接池， 其中使用dr 接，优化 以及echarts数据可视化工作，用雷达图 项目的性能；前 开发中，负责 微信小程序开发， 可视化员 CoC技术栈。 个人收获:在实习期间，学习了如何在团队中协作开发Java项目，以及如何使用常见的开发工具和框 架，如Git、Spring和MyBatis。深入了解了Java应用程序的设计和实现，提高了编程能力和团队协作 能力。 项目经历 2020.12-2020.12 智慧校园平台开发 组长 项目地址:https://github.com/guoxiansen/ntelligentCampu 开发环境Python3、fiask、Java、MySQL57、Layuit、微信小程序、Pycharm、IDE 项目描述:微信小程序端作为前台，模块包括校园资讯、校园商城、商品管理、用户管理、教务信息 健康码管理等，通过管理后台对小程序端的校园商城、校园资讯数据进行管理。 工作内容:负责整个项目的整体规划设计、原型设计、数据库设计到最终的测试以 (及上线部署。 主要进 行后 端开发，包括利用Layui框架编写管理后台，面向接口编程，供前端调用：利用Python肥取教务信 口供前端页面使用。 息(课表和成绩）以json数据格式进行传输，利用flask 做成接 Cup3D足球机器人的开发与设计 Rob 2018.092020.08 负责人 开发环境：Ubuntu、Python、Pycharm、Eclipse、 13 项目描述:在Ubuntu下的SimSpark3D仿真环境中，设计NAO足球机器人来实现与人类足球运动一样 的11v11的竞赛。 工作内容：主要负 双足 机器人 器人 利月 lChain 步态 及 ier框架中DDPG 逻辑决策层的研究 射门以 算法对机器人的步态进行优化，参加Ro boCup机器人世界杯中国赛并获得3D仿真组 二等奖。 专业技能 4、Java。了解爬虫技术及Django框架，熟悉C＋＋STL 编程语言：熟悉Python，了解Golang、C/C＋ C＋-11常用特性（智能指针等)，了解Go 常用容器、 ang的GMP模型，map、slice数据结构。 算法基础：熟悉常见的数据结构和算法，如排序算法(快速排序、归并排序等）和搜索算法(DFS BFS等）。 ux:RHCE红帽认证工程师，能够在Li ux下使用So uT ket进行网络编程，了解/O多路复用技术 计算机网络：熟悉OSI七层网络模型，掌握HTTP、TCP/UDP、IP、ARP、DHCP等常见网络协议 操作系统：熟悉操作系统的进程间通信、内存管理等知识 数据库：了解关系数据库MySQL的索引、事务、锁机制，以及非关系数据库Redis的基本数据结构、过 期淘汰策略。 设计模式:了解常见的设计模式，例如单例模式、工厂模式、观察者模式等 存储:了解主流RAID技术，raid0/1/10/5以及新型条带化raid技术 工具:了解Git、VSCode、VIM等开发/调试工具的使用。 外语：英语六级(CET-6)，能够快速阅读英文文献和英文开发文档 荣誉奖项 2023.04 第十四届蓝桥杯省赛Python研究生组三等奖 南京邮电大学学业奖学金三等奖 2022.09 RoboCup机器人世界杯中国赛仿真3D组二等奖 2021.05 2020.11 个人总结 。有快速学习和解决问题的能力，良好的团队合作意识 。性格开朗、适应能力强，能快速的融入到工作中，服从管理 热爱技术上的研究，经常上Google、掘金、知乎、Github浏览学习 喜欢技术上的总结与分享，坚持写个人技术博客 """

txtpath = "./train_data/"
schema = ['姓名', '年龄', "出生日期", "工作时间", "学历", "毕业院校", "求职目标", "主修专业"]
# D:\LEARNING\CODE\CV-Parser\model_best
# ie = Taskflow('information_extraction', schema=schema, task_path=r'E:\model_best')
ie = Taskflow('information_extraction', schema=schema, task_path=r'D:\LEARNING\CODE\CV-Parser\model_best')


# txt2json(txtpath, ie)
# print(get_info(text2, ie, "123"))


def cvprase(text, filename):
    # ie = Taskflow('information_extraction', schema=schema, task_path=r'E:\model_best')
    return get_info(text, ie, filename)


if __name__ == '__main__':
    res_data = {'文件名': '123', '姓名': '林雅南', '年龄': 28, '出生日期': '1996.05',
                '工作时间': ['2020.08-2021.09', '2021.09-至今', '2019.12-2020.08', '2018.08-2019.12'], '学历': '本科',
                '毕业院校': '华南师范大学', '求职目标': '市场总监', '主修专业': '市场营销', '工作年限': 3}
    total_year = 0
    work_years = 0
    work_month = 0
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

            # print("time2的时间为", time2)
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
