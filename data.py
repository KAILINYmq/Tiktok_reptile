import pymysql
import settings

db = pymysql.connect(host=settings.Host, user=settings.User, password=settings.Password, database=settings.Database)
cursor = db.cursor()

sqlMessage = """INSERT INTO message(user_id,
         good_num, fans_num, video_num, follow_num)
         VALUES (%s,%s,%s,%s,%s)"""
sqlUser = "INSERT INTO users(user_id, birthday) VALUES (%s, %s)"
sqlVideo = "INSERT INTO users_video(user_id,video_time) VALUES (%s, %s)"
sqlSelect = "select user_id from message where user_id=%s"
sqlOnline = "INSERT INTO online_time(old_time, reptile_time, sec_user_id) VALUES (%s, %s, %s)"
sqlUid = "INSERT INTO sec_user_id(uid) VALUES (%s)"
sqlSelectUid = "select uid from sec_user_id limit %s,10"

def dblink():
    # 使用 execute()  方法执行 SQL 查询
    cursor.execute("SELECT VERSION()")
    # 使用 fetchone() 方法获取单条数据.
    data = cursor.fetchone()
    print("Database version : %s " % data)

def Ini():
    global db,cursor
    db = pymysql.connect(host=settings.Host, user=settings.User, password=settings.Password, database=settings.Database)
    cursor = db.cursor()

def dbclose():
    # 关闭数据库连接
    db.close()
