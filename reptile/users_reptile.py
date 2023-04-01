import requests, time, gzip, json
import urllib.request as request

import settings


def getGorgon(api, headers):
    '''
    获取gorgon的方法
    :param api: 抖音的api请求
    :param headers: 抖音的header请求
    :return: gorgon
    '''
    gorgon_host = "http://106.12.205.72:8080/gorgon"
    headers['api'] = api
    res = requests.get(gorgon_host, headers=headers)
    # 因为后面爬取数据还要用到headers，所以我们在获取到gorgon之后要把headers里面的api字段给它去掉
    del headers['api']
    # print("gorgon-status: ", res.status_code)
    res = json.loads(res.content)
    # print(res.keys())
    gorgon = res.get("gorgon")
    # print(res['status'])
    if res['status']=='0':
        pass
        # print("gorgon:", gorgon)
    else:
        print("获取gorgon失败，失败原因是:")
        print(res['msg'])
    return gorgon

def construct_api(user_id, _rticket, ts, sec_user_id):
    """
    api 构造函数
    :param user_id: 用户的id
    :param _rticket: 时间戳
    :param ts: 时间戳
    :param sec_user_id: 用户的加密的id
    :return: api
    """
    user_api = "https://aweme.snssdk.com/aweme/v1/user/profile/other/?" \
                "sec_user_id={}&" \
                "address_book_access=1&from=0&" \
                "source=UserProfileFragment_initUserData&" \
                "publish_video_strategy_type=2&" \
                "user_avatar_shrink=188_188&user_cover_shrink=750_422&" \
                "vs_play_count_hotfix=true&version_name=15.2.0&" \
                "ts={}&device_type=SM-N935F&" \
                "iid=1355042122629533&app_type=normal&" \
                "resolution=1280*720&" \
                "aid=1128&app_name=aweme&" \
                "appTheme=dark&_rticket={}&" \
                "device_platform=android&version_code=150200&" \
                "dpi=240&openudid=d4258bf9c3605799&" \
                "minor_status=0&cdid=051cbf12-37d1-4a38-aa3e-b7de8c6abf92&" \
                "cpu_support64=false&ssmix=a&os_api=19&mcc_mnc=46007&" \
                "device_id=58916287376&device_brand=samsung&" \
                "manifest_version_code=150201&os_version=4.4.2&" \
                "host_abi=armeabi-v7a&update_version_code=15209900&ac=wifi&" \
                "language=zh&uuid=359090010212254&channel=aweGW".format(sec_user_id, ts, _rticket)
    return user_api

def construct_header(apiurl, user_id, sec_user_id, cookie, query, token, user_agent, _rticket, ts, gorgon):
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
            # Client
            "Accept-Encoding": "gzip",
            "User-Agent": user_agent,
            # Cookies
            "Cookie": cookie,
            # Miscellaneous
            "passport-sdk-version": "18",
            "sdk-version": "2",
            "X-Argus": "vzQJYW8dgj4rl4wIpXbxiYg1hddvYGTSURNhE5v6Kn53m40DzTvQUPw3F1K/jiaJ56SN5UgGLj7gVNHm5peUneCChLZ55SKlnBnaSaEn2PgxIvBeb4Yo5hwnAZNezUbPUDS3lW98LkCVfDBBE6AAMfQ2+QSOqqFNxS/Tykhen0MhPKL3hnBpqdQDA+mILfq8uIsGlHJspObxAMKMONTE+YelifwSNbQhLTreZS8fUEKcik0GT5jrelbGg9aXfHSFsxXjYlLD093m0xLzUrRIRao6",
            "X-Khronos": ts,
            "X-Ladon": "40XKNHMsz2ON4JhiGuCRzRasgjoDgAIPvy4MM/koWe3Qu9hn",
            "X-SS-REQ-TICKET": _rticket,
            "x-tt-dt": "AAAYEQMUCKYIMPSYCO33L5Y35BZF6X2HE4LFDAV57H4HZIVEJ6SU5WZYG4KQSDLEZ7BMS2XUQG36IHDLL63FQYBUIZC6ZHSS4DIXJ5ZOEL2JGTAISDEUMQEKHRQMGD62JYN5SQSFNDX4KW32LRNXLIA",
            "X-Tt-Token": token,
            "X-Tyhon": "fUNwf7ijeXz+4EBx1aRiXMWxRHC8uGdJ6Zld2fk=",
            "X-SS-QUERIES": query,
            # Transport
            "Connection": "Keep-Alive",
            "Host": "aweme.snssdk.com"
      }
      gorgonData = getGorgon(apiurl, headers)
      headers["X-Gorgon"] = gorgonData
      return headers

def get_user_detail_info(cookie, query, token, user_agent, user_id, sec_user_id, gorgon):
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
      api = construct_api(user_id, _rticket, ts, sec_user_id)
      headers = construct_header(api, user_id, sec_user_id, cookie, query, token, user_agent, _rticket, ts, gorgon)
      print(api)
      req = request.Request(api)
      for key in headers:
          req.add_header(key, headers[key])

      with request.urlopen(req) as f:
          data = f.read()
      return gzip.decompress(data).decode()

def users_main(sec_user_id):
    data = {}
    try:
        res = get_user_detail_info(settings.cookie, settings.query, settings.token, settings.user_agent, settings.user_id,
                                   sec_user_id, settings.gorgon)
        js = json.loads(res.encode('utf-8', 'replace'))
        print(js)
        data["good"] = js["user"]["total_favorited"]
        data["follow"] = js["user"]["following_count"]
        data["fans"] = js["user"]["mplatform_followers_count"]
        data["videoNum"] = js["user"]["aweme_count"]
    except Exception as e:
        print("users Error!")
        pass
    return data

if __name__ == '__main__':
    res = get_user_detail_info(settings.cookie, settings.query, settings.token, settings.user_agent, settings.user_id, "MS4wLjABAAAAUjkYlN_ZMTdaK2XF8_haXcxeqQQbyj85OMkeWCZ97bY", settings.gorgon)
    print("--------json数据--------")
    js = json.loads(res.encode('utf-8', 'replace'))
    print(js)
    print("获赞="+str(js["user"]["total_favorited"]))
    print("关注="+str(js["user"]["following_count"]))
    print("粉丝="+str(js["user"]["mplatform_followers_count"]))
    print("作品数="+str(js["user"]["aweme_count"]))
    print(json.dumps(js, indent=4))