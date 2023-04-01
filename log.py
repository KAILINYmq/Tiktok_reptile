import logging,os

rdir = os.path.dirname(os.path.abspath(__file__))
log_dir = rdir + '/log/record.log'
def get_logger():
    fh = logging.FileHandler(log_dir,encoding='utf-8') #创建一个文件流并设置编码utf8
    logger = logging.getLogger() #获得一个logger对象，默认是root
    logger.setLevel(logging.DEBUG)  #设置最低等级debug
    fm = logging.Formatter("%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s")  #设置日志格式
    logger.addHandler(fh) #把文件流添加进来，流向写入到文件
    fh.setFormatter(fm) #把文件流添加写入格式
    return logger