"""
    @Name: 
        user.py
    @Desc:
        this file is used to do sql operations about users
    @Class:
        User_Login: table of users login information
        User_Info: table of users themselves information
"""

from .sql import *


class User_Login:
    """
    用户登录表
    """
    table_name = "user_login"
    email = "email" # primary key
    uid = "UID"
    password = "password"

    @staticmethod
    def getRecordByKey(_email):
        return getTuplesByEqualCond(User_Login.table_name, [User_Login.email], [_email])

    @staticmethod
    def insert(_email, _uid, _password):
        key = "{}, {}, {}".format(User_Login.email, User_Login.uid, User_Login.password)
        values = "'{}', {}, '{}'".format(_email, _uid, _password)
        sql_insert(User_Login.table_name, values, key)

    @staticmethod
    def isLegal(_email: str, _password: str) -> bool:
        """
        判断是否是合法账号密码
        """
        record = User_Login.getRecordByKey(_email)
        if len(record) == 0:
            return False
        else:
            return record[0][User_Login.password] == _password

    @staticmethod
    def register(_name, _email, _password)->bool:
        """ 如果存在已注册账号返回 False 否则返回 True """
        if len(User_Login.getRecordByKey(_email)) != 0:
            return False
        else:
            # insert into usr_info
            User_Info.insert(_name)
            uid = getLastRecord(User_Info.table_name, User_Info.uid)[User_Info.uid]
            print(uid)
            User_Login.insert(_email, uid, _password)
            return True
    
    @staticmethod
    def changePassword(_email, _newpassword):
        sql_update(User_Login.table_name, "{}='{}'".format(User_Login.email, _email), **{User_Login.password:_newpassword})
    
    @staticmethod
    def getUidByEmail(_email):
        res = getTuplesByEqualCond(User_Login.table_name, [User_Login.email], [_email])
        if len(res) == 0:
            return 0 # 查无此人
        return res[0][User_Login.uid]

    @staticmethod
    def getEmailByUid(_uid):
        return getTuplesByEqualCond(User_Login.table_name, [User_Login.uid], [_uid])
        


class User_Info:
    """
    用户信息表
    """
    table_name = "user_info"
    uid = "UID" # primary key
    avatar = "avatar"
    name = "name"
    description = "description"

    @staticmethod
    def show():
        return str(sql("desc {}".format((User_Info.table_name))))

    @staticmethod
    def getRecordByKey(_uid):
        return getTuplesByEqualCond(User_Info.table_name, [User_Info.uid], [_uid])[0]

    @staticmethod
    def insert(_name, _description=''):
        key = "{}, {}".format(User_Info.name, User_Info.description)
        values = "'{}', '{}'".format(_name, _description)
        sql_insert(User_Info.table_name, values, key)

    @staticmethod
    def update(_uid, _name, _avatar, _desc):
        key_value = {User_Info.name:_name, User_Info.avatar:_avatar, User_Info.description:_desc}
        sql_update(User_Info.table_name, "{}='{}'".format(User_Info.uid, _uid), **key_value)