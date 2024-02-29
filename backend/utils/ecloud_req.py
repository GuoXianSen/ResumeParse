# -*-coding:utf-8-*-
import uuid
import requests
import hmac
from hashlib import sha1
from hashlib import sha256
import urllib
import copy
import time
import json

# # 填写您的accesskey 和secretKey
# access_key = "a74d25c0b5334d6dbdb36dc456fccdd6"
# secret_key = "a608eaeabbbc43f7939a961a686e9610"


# 签名计算
def sign(http_method, playlocd, servlet_path, secret_key):
    time_str = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.localtime())
    playlocd['Timestamp'] = time_str
    parameters = copy.deepcopy(playlocd)
    parameters.pop('Signature')
    sorted_parameters = sorted(parameters.items(), key=lambda parameters: parameters[0])
    canonicalized_query_string = ''
    for (k, v) in sorted_parameters:
        canonicalized_query_string += '&' + percent_encode(k) + '=' + percent_encode(v)
    string_to_sign = http_method + '\n' \
                     + percent_encode(servlet_path) + '\n' \
                     + sha256(canonicalized_query_string[1:].encode('utf-8')).hexdigest()

    key = ("BC_SIGNATURE&" + secret_key).encode('utf-8')
    string_to_sign = string_to_sign.encode('utf-8')
    signature = hmac.new(key, string_to_sign, sha1).hexdigest()
    return signature


# 参数编码
def percent_encode(encode_str):
    encode_str = str(encode_str)
    res = urllib.parse.quote(encode_str.encode('utf-8'), '')
    res = res.replace('+', '%20')
    res = res.replace('*', '%2A')
    res = res.replace('%7E', '~')
    return res


def requests2ecloud(imagebase64, access_key, secret_key):

    # http method
    method = 'POST'
    # 目标域名 端口
    url = r"https://api-wuxi-1.cmecloud.cn:8443/api/ocr/v1/generic"
    # 请求url
    path = '/api/ocr/v1/generic'
    # 可以不改
    headers = {'Content-Type': 'application/json'}
    # 签名公参，如果有其他参数，同样在此添加
    querystring = {"AccessKey": access_key, "Timestamp": "2020-12-11T16:27:01Z", "Signature": "",
                   "SignatureMethod": "HmacSHA1", "SignatureNonce": "", "SignatureVersion": "V2.0"}

    # 请求body

    payload = {'image': imagebase64}

    # 生成SignatureNonce
    querystring['SignatureNonce'] = uuid.uuid4()
    # 生成签名
    querystring['Signature'] = sign(method, querystring, path, secret_key)

    res = requests.post(url, headers=headers, params=querystring, json=payload)
    return res.text

    # # 转化为curl命令
    #
    # ci = curlify.to_curl(test.request)
    #
    # print('============================================================')
    #
    # # 将request转换成curl
    #
    # print(ci)
    #
    # print('============================================================')
    #
    # print('url : %s' % url)
    #
    # result = json.loads(test.text)
    #
    # print(result)
    #
    # try:
    #
    #     assert result.get('state') == 'OK'
    #
    #     print('response: %s' % json.dumps(result, indent=4, ensure_ascii=False))
    #
    # except AssertionError as ae:
    #
    #     print(json.dumps(result, indent=4, ensure_ascii=False))