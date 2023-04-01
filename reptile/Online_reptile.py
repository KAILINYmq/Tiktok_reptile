import requests, time, gzip, json, random, datetime
import urllib.request as request
import urllib.parse as parse

import settings


def construct_api(user_id, _rticket, ts, sec_user_id):
    """
    api 构造函数
    :param user_id: 用户的id
    :param _rticket: 时间戳
    :param ts: 时间戳
    :param sec_user_id: 用户的加密的id
    :return: api
    """
    fans_api = "https://aweme.snssdk.com/aweme/v1/im/user/active/status/?version_name=15.2.0&" \
            "ts={}&device_type=SM-N935F&iid=1355042122629533&app_type=normal&" \
            "resolution=720*1280&aid=1128&app_name=aweme&appTheme=dark&_rticket={}&" \
            "device_platform=android&version_code=150200&dpi=240&openudid=d4258bf9c3605799&minor_status=0&" \
            "cdid=cdbe27e5-1425-4d02-8c59-2b0f6e72521f&cpu_support64=false&ssmix=a&os_api=19&mcc_mnc=46007&" \
            "device_id=58916287376&device_brand=samsung&manifest_version_code=150201&os_version=4.4.2&" \
            "host_abi=armeabi-v7a&update_version_code=15209900&ac=wifi&language=zh&" \
            "uuid=359090010212254&channel=aweGW".format(ts, _rticket)
    return fans_api

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
            # Entity
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
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

def get_user_detail_info(cookie, query, token, user_agent, user_id, sec_user_id, gorgon, SecUidDate):
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
      data = {
        'source': 'following_list',
        'sec_user_ids': SecUidDate,
        'conv_ids':[]
      }
      _rticket = str(time.time() * 1000).split(".")[0]
      ts = str(time.time()).split(".")[0]
      api = construct_api(user_id, _rticket, ts, sec_user_id)
      headers = construct_header(api, user_id, sec_user_id, cookie, query, token, user_agent, _rticket, ts, gorgon)
      print(api)
      datas = parse.urlencode(data).replace("+","").replace("%27","%22").encode()
      req = request.Request(url=api, data=datas)
      for key in headers:
          req.add_header(key, headers[key])
      req.add_header("Content-Length", len(datas))
      with request.urlopen(req) as f:
          dataValue = f.read()
      return gzip.decompress(dataValue).decode()

def Online_main(sec_user_id, SecUidDate):
    returnData = []
    try:
        res = get_user_detail_info(settings.cookie, settings.query, settings.token, settings.user_agent, settings.user_id,
                                   sec_user_id, settings.gorgon, SecUidDate)
        js = json.loads(res.encode('utf-8', 'replace'))
        print(js)
        for tim in js['data']:
            data = {}
            data["OldTime"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(tim['last_active_time']))
            data["UserId"] = tim['sec_user_id']
            returnData.append(data)
    except Exception as e:
        print("Online Error!！")
    return returnData

def test_Online(SecUidDate):
    """Online 单独运行函数"""
    OnlineTime = []
    if len(SecUidDate) > 0:
        try:
            OnlineTime = Online_main(settings.sec_user_id,SecUidDate)
        except Exception as e:
            print("Online Error!")

if __name__ == '__main__':
    res = get_user_detail_info(settings.cookie, settings.query, settings.token, settings.user_agent, settings.user_id,
                               settings.sec_user_id, settings.gorgon, ["MS4wLjABAAAAILtfKT21mIIWjskaIiVVjJ6VgN-a7PdavuSNhEr11uU","MS4wLjABAAAAcpz66NE2XcwhdeiHwsJlwMSDmm5fuk8gOmBzxTOxih2spKgTwDuZb4RCNT61zJW3"])
    print("--------json数据--------")
    js = json.loads(res.encode('utf-8', 'replace'))
    print(js)
    for tim in js['data']:
        timeArray = time.localtime(tim['last_active_time'])
        otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
        print(otherStyleTime)
        print(tim['sec_user_id'])
        print("-------------------------------------")