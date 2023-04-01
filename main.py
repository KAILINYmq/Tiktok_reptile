import time, random, datetime
import settings
from reptile.fans_reptile import fans_main
from reptile.Online_reptile import Online_main
from log import get_logger
from data import db, cursor, dblink, dbclose, sqlUser,sqlVideo,sqlMessage,sqlSelect, sqlOnline, sqlUid, Ini, sqlSelectUid

pageLen = []
nowTime = datetime.datetime.now()
logger = get_logger()

def Fire():
    # 1. 链接数据库
    dblink()
    # 2. 执行爬虫获取数据
    datas, minTime, OnlineTime, SecUidDate = fans_main()
    print(datas)
    for uid in SecUidDate:
        # 存储uid
        try:
            cursor.execute(sqlUid, uid)
            db.commit()
        except:
            print("Main SecUidDate Error!")
            db.rollback()
    # for data in datas:
    #     # 3.数据入库
    #     try:
    #         if cursor.execute(sqlSelect, data["Uid"]) is 0:
    #             cursor.execute(sqlMessage, (data["Uid"],
    #                                         data["UserMessage"]["good"],
    #                                         data["UserMessage"]["fans"],
    #                                         data["UserMessage"]["videoNum"],
    #                                         data["UserMessage"]["follow"]))
    #             cursor.execute(sqlUser, (data["Uid"], data["Birthday"]))
    #             for videoTime in data["videoTime"]:
    #                 cursor.execute(sqlVideo, (data["Uid"], videoTime))
    #         db.commit()
    #     except:
    #         print("Main Error!")
    #         db.rollback()
    # for data in OnlineTime:
    #     # 3.1 在线状态数据入库
    #     try:
    #         cursor.execute(sqlOnline, (data["OldTime"], nowTime))
    #         db.commit()
    #     except:
    #         print("Main Online Error!")
    #         logger.error("Main Online Error!")
    #         db.rollback()
    # 3.1 获取下一页数据
    if minTime is not 0 and minTime not in pageLen:
        settings.maxTime = minTime
        pageLen.append(minTime)
        time.sleep(random.randint(1, 10))
        Fire()

def Online_time():
    # 测试数据库链接
    try:
        dblink()
        logger.debug("MySQL Start")
    except:
        logger.error("MySQL Start")
        Ini()
    # 读取10条数据
    for i in range(1, 57):
        SecUidDate = []
        cursor.execute(sqlSelectUid, ((i - 1) * 10))
        datas = cursor.fetchall()
        for data in datas:
            SecUidDate.append(data[0])
        # 获取在线时间
        if len(SecUidDate) > 0:
            try:
                OnlineTime = Online_main(settings.sec_user_id, SecUidDate)
                # 存储数据
                for data in OnlineTime:
                    print(data)
                    try:
                        cursor.execute(sqlOnline, (data["OldTime"], nowTime, data["UserId"]))
                        db.commit()
                    except:
                        print("Main Online Error!")
                        logger.error("Main Online Error!")
                        db.rollback()
            except Exception as e:
                print("Online Error!")
                logger.error("Online Error!")

if __name__ == '__main__':
    print("Reptile Start")
    logger.debug("Reptile Start")
    # while True:
    try:
    #         time_now = time.strftime("%H:%M", time.localtime())
    #         if time_now in ["08:30", "13:00", "23:30"]:
    #             logger.debug(time_now+"run.")
        nowTime = datetime.datetime.now()
        Online_time()
    # Fire()
    #             time.sleep(3600)
    except:
        # 4.关闭数据库链接
        # dbclose()
        logger.error("Tiempo fijo Error!")