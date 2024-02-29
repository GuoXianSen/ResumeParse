import os
import re
import base64
import json

from .ecloud_req import requests2ecloud


def mkdir(path):
    folder = os.path.exists(path)

    if not folder:  # 判断是否存在文件夹如果不存在则创建为文件夹
        os.makedirs(path)


def findAllFile(base):
    for root, ds, fs in os.walk(base):
        for f in fs:
            fullname = os.path.join(root, f)
            yield fullname


def main():
    base = './temp_png'
    result_path = './result'
    num = 1
    for i in findAllFile(base):
        png_name = os.path.basename(i)
        jianli_name = i.replace(base, '').replace(png_name, '').replace('\\', '')

        # 读取png
        image = open(i, "rb")
        image_bytes = image.read()

        # png转base64编码
        image_base64 = base64.b64encode(image_bytes)
        if isinstance(image_base64, bytes):
            image_base64 = str(image_base64, encoding='utf-8')
        image.close()

        # 发送ocr请求
        res = requests2ecloud(image_base64,
                              access_key="3d15919ed577490a831b0339d217e31e",
                              secret_key="b469dcb9ae92428eb0618b2697098062")

        # 结果存成临时json
        f2 = open("temp_json/temp_json.json", 'w')
        f2.write(res)
        f2.close()

        f = open('temp_json/temp_json.json', 'r')
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

        img_json = {jianli_name: page_list}
        b = json.dumps(img_json)

        # 保存json
        mkdir(i.replace(base, result_path).replace(png_name, ''))
        f2 = open(i.replace(base, result_path).replace('.png', '.json'), 'w')
        f2.write(b)
        f2.close()

        # 打印进度
        print('{} finished {}'.format(i, num))
        num += 1


if __name__ == '__main__':
    main()

# 图片
# pdf_image('./dataset_pdf', './dataset_pdf', 5, 5, 0)


# 参数        绝对路径 C:\Users\Clay_Guo\Desktop\【软件杯】\Base\django-vue-lyadmin\backend\media\platform\2023-06-24\20230624174238_628.png
# 返回值      json  文件夹
# json ---> text 存到文件夹
# 绝对路径 ---> XY
#
