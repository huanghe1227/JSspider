import requests
import hashlib
import time
import random

def md5(word):
    # 加密之前先进行编码
    word = word.encode()
    result = hashlib.md5(word)
    # 返回十六进制数据字符串值
    return result.hexdigest()


def youdao(word):
    url = "http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule"

    # 有道翻译接口必须带cookie才行 多请求几次发现cookie只变化结尾的时间戳
    time_stamp = str(int(time.time()*1000))

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Cookie': f'OUTFOX_SEARCH_USER_ID=277838190@10.108.160.19; OUTFOX_SEARCH_USER_ID_NCOO=1862360513.1103675; JSESSIONID=aaaFORJqWOPYfbQnHu4rx; ___rl__test__cookies={time_stamp}',
        'Host': 'fanyi.youdao.com',
        'Origin': 'http://fanyi.youdao.com',
        'Referer': 'http://fanyi.youdao.com/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
    }

    ts = time_stamp
    bv = md5("5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36")
    salt = time_stamp + str(random.randint(0, 9))
    sign = md5("fanyideskweb" + word + salt + "]BjuETDhU)zqSxf-=B#7m")

    words = {
        'i': word,
        'from': 'AUTO',
        'to': 'AUTO',
        'smartresult': 'dict',
        'client': 'fanyideskweb',
        'salt': salt,
        'sign': sign,
        'lts': ts,
        'bv': bv,
        'doctype': 'json',
        'version': '2.1',
        'keyfrom': 'fanyi.web',
        'action': 'FY_BY_CLICKBUTTION',
    }

    result = requests.post(url, headers=headers, data=words).text
    print(result)


if __name__ == '__main__':
    while True:
        word = input('请输入需要翻译的词汇：')
        youdao(word)
