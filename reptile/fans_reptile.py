import requests, time, gzip, json
import urllib.request as request
from log import get_logger
import settings
from reptile.users_reptile import users_main
from reptile.video_reptile import video_main
from reptile.Online_reptile import Online_main

logger = get_logger()

def construct_api(user_id, _rticket, ts, sec_user_id, maxTime):
    """
    api 构造函数
    :param user_id: 用户的id
    :param _rticket: 时间戳
    :param ts: 时间戳
    :param sec_user_id: 用户的加密的id
    :return: api
    """
    fans_api = "https://aweme.snssdk.com/aweme/v1/user/follower/list/?" \
               "user_id={}" \
               "&max_time={}" \
               "&count=20&offset=2&source_type=1" \
               "&address_book_access=1&gps_access=1&vcd_count=0" \
               "&version_name=16.2.0" \
               "&device_type=SM-N935F" \
               "&iid=281949533382471" \
               "&app_type=normal" \
               "&resolution=720*1280" \
               "&aid=1128&app_name=aweme&appTheme=light" \
               "&device_platform=android" \
               "&version_code=160200" \
               "&dpi=240" \
               "&openudid=d4258bf9c3605799" \
               "&minor_status=0" \
               "&cdid=99268e6c-16d3-4f35-a58c-8e481ad092cc" \
               "&cpu_support64=false&ssmix=a&os_api=19&mcc_mnc=46007" \
               "&device_id=58916287376" \
               "&device_brand=samsung" \
               "&manifest_version_code=160201" \
               "&os_version=4.4.2&host_abi=armeabi-v7a&update_version_code=16209900&ac=wifi" \
               "&language=zh&uuid=359090010212254&channel=tengxun_1128_0531" \
               "&_rticket={}" \
               "&ts={}" \
               "&sec_user_id={}" \
               "&is_android_pad=0".format(user_id, maxTime, _rticket, ts, sec_user_id)
    return fans_api

def construct_header(user_id, sec_user_id, cookie, query, token, user_agent, _rticket, ts, gorgon):
      """
      构造请求头，需要传入的参数如下
      :param user_id: 要爬取的用户的uid
      :param sec_user_id: 要爬取的用户的加密的id
      :param cookie: cookie
      :param query: 请求的query
      :param token: 你的token
      :param user_agent: 请求的user_agent
      :param _rticket: 时间戳（毫秒级）
      :param ts: 时间戳（秒级）
      :return: 构造好的请求头：headers
      """
      headers = {
            "Host": "aweme-eagle.snssdk.com",
            "Connection": "keep-alive",
            "Cookie": cookie,
            "Accept-Encoding": "gzip",
            "X-SS-QUERIES": query,
            "X-SS-REQ-TICKET": _rticket,
            "X-Tt-Token": token,
            "sdk-version": "1",
            "User-Agent": user_agent
      }
      headers["X-Khronos"] = ts
      headers["X-Gorgon"] = gorgon
      return headers

def get_user_detail_info(cookie, query, token, user_agent, user_id, sec_user_id, gorgon, maxTime):
      """
      爬取用户数据
      :param cookie: 你自己的cookie
      :param query: 你自己的query
      :param token: 你自己的token
      :param user_agent: 你自己的User-Agent
      :param user_id: 用户的uid
      :param sec_user_id: 用户的加密的uid
      :return: response
      """
      _rticket = str(time.time() * 1000).split(".")[0]
      ts = str(time.time()).split(".")[0]
      api = construct_api(user_id, _rticket, ts, sec_user_id, maxTime)
      headers = construct_header(user_id, sec_user_id, cookie, query, token, user_agent, _rticket, ts, gorgon)
      print(api)
      print(headers)
      req = request.Request(api)
      for key in headers:
          req.add_header(key, headers[key])

      with request.urlopen(req) as f:
          data = f.read()
      return gzip.decompress(data).decode()

def fans_main():
    Message = []
    OnlineTime = []
    SecUidDate = []
    res = get_user_detail_info(settings.cookie, settings.query, settings.token, settings.user_agent, settings.user_id,
                               settings.sec_user_id, settings.gorgon, settings.maxTime)
    # js = json.loads(res.encode('utf-8', 'replace').decode('unicode-escape'))
    js = json.loads(res.encode('utf-8', 'replace'))
    print("--------json数据fans--------")
    print(js)
    # print("MaxTime=" + str(js["max_time"]))
    for data in js["followers"]:
        returnData = {}
        try:
            returnData["Uid"] = data["uid"]
            returnData["Birthday"] = data["birthday"]
            # 1. 获取用户数据
            # returnData["UserMessage"] = users_main(data["sec_uid"])
            # 2. 获取视频数据
            # returnData["videoTime"] = video_main(data["sec_uid"])
            SecUidDate.append(data["sec_uid"])
        except Exception as e:
            logger.error("fans Error!")
            print("fans Error!")
        Message.append(returnData)
    # 获取在线状态
    if len(SecUidDate) > 0:
        try:
            OnlineTime = Online_main(settings.sec_user_id,SecUidDate)
        except Exception as e:
            print("Online Error!")
            logger.error("Online Error!")
    return Message, js["min_time"], OnlineTime, SecUidDate

if __name__ == '__main__':
    res = get_user_detail_info(settings.cookie, settings.query, settings.token, settings.user_agent, settings.user_id, settings.sec_user_id, settings.gorgon, settings.maxTime)
    # js = json.loads(res.encode('utf-8', 'replace').decode('unicode-escape'))
    js = json.loads(res.encode('utf-8', 'replace'))
    print("--------json数据--------")
    print(js)
    # print(json.dumps(js, indent=4))
    print("--------NickName--------")
    print("MaxTime="+str(js["max_time"]))
    print("MixTime="+str(js["min_time"]))
    for data in js["followers"]:
        try:
            print("Nickname="+data["nickname"])
            print("Uid="+data["uid"])
            print("Birthday="+data["birthday"])
            print("Sec_uid="+data["sec_uid"])
            print("-"*50)
        except Exception as e:
            print("fans error!")
            pass