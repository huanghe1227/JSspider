import execjs
import json
import re
import time, datetime
import requests


def get_crypto(data):
    with open('cloud.js', encoding='utf-8') as f:
        could_js = f.read()

    js = execjs.compile(could_js)

    result = js.call('encSeckey', data)

    return result

def get_post_data(page, id, cursor):
    data = {
        "rid": "R_SO_4_" + f"{id}",
        "threadId": "R_SO_4_" + f"{id}",
        "pageNo": f"{page}",
        "pageSize": "20",
        "cursor": f"{cursor}",
        "offset": "0",
        "orderType": "1",
        "csrf_token": ""
    }
    data = json.dumps(data)
    data = re.sub('\s', '', data)
    return data


def get_comment(data):
    data_dict = {
        'params': data["encText"],
        'encSecKey': data["encSecKey"]
    }
    url = "https://music.163.com/weapi/comment/resource/comments/get?csrf_token="
    headers = {
        'content-type': 'application/x-www-form-urlencoded',
        'referer': 'https://music.163.com/song',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36',
        'origin': 'https://music.163.com',
    }
    response = requests.post(url, headers=headers, data=data_dict).text
    result = json.loads(response)
    return result


# 解析普通评论
def parse_comment_json(data, music_id):
    try:
        comments = data["data"]["comments"]
        cursor = data["data"]["cursor"]
        for comment in comments:
            content = comment["content"]
            content = re.sub('\s', ' ', content)
            nickname = comment["user"]["nickname"]
            userId = comment["user"]["userId"]
            comment_time = comment["time"]
            timeStamp = int(comment_time/1000)
            dateArray = datetime.datetime.fromtimestamp(timeStamp)
            otherStyleTime = dateArray.strftime("[%Y--%m--%d %H:%M:%S]")
            print(nickname + '(id: ' + str(userId) + ')' + ':  ' + content + otherStyleTime)
            with open(f'./data/歌曲ID：{music_id}评论.txt', 'a', encoding='utf-8') as f:
                f.write(nickname + '(id: ' + str(userId) + ')' + ':  ' + content + otherStyleTime + '\n')
        return cursor

    except:
        print(data)


#  解析热门评论
def parse_hot_comment(data):
    hot_comments = data["data"]["hotComments"]
    for hot_comment in hot_comments:
        content = hot_comment["content"]
        content = re.sub('\s', ' ', content)
        nickname = hot_comment["user"]["nickname"]
        userId = hot_comment["user"]["userId"]
        comment_time = hot_comment["time"]
        timeStamp = int(comment_time/1000)
        dateArray = datetime.datetime.fromtimestamp(timeStamp)
        otherStyleTime = dateArray.strftime("[%Y--%m--%d %H:%M:%S]")
        print(nickname + '(id: ' + str(userId) + ')' + ':  ' + content + otherStyleTime)
        with open('./data/网易云音乐热评.txt', 'a', encoding='utf-8') as f:
            f.write(nickname + '(id: ' + str(userId) + ')' + ':  ' + content + otherStyleTime + '\n')




if __name__ == '__main__':
    music_id_list = [208902,]
    for music_id in music_id_list:
        cursor = int(time.time() * 1000)
        for page in range(1, 100):
            data = get_post_data(page, music_id, cursor)
            result = get_crypto(data)
            music_comment = get_comment(result)
            if page == 1:
                parse_hot_comment(music_comment)
            cursor = parse_comment_json(music_comment, music_id)

            time.sleep(1)
