
class Config:
    """
    Flask配置
    """
    SECRET_KEY = 'adaosfk1203rsdmdkfh3*rsfsg'

    # 数据库
    SQLALCHEMY_DATABASE_URI = 'mysql://root:123456@127.0.0.1:3306/mangguo_vip?charset=utf8'
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    DEBUG = True