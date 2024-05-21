"""
@Time: 2024/5/21 11:11
@Auth: EnderTheCoder
@Email: ggameinvader@gmail.com
@File: get_user_info.py
@IDE: PyCharm
@Motto：The only one true Legendary Grandmaster.
"""
from request import EncryptedRequest


class UserInfoRequest(EncryptedRequest):
    def __init__(self, username):
        super().__init__({
            'uuid': 'wdrunandroid_134453',
            'cols': 'top 1 userid,username,userzt,wetx,userzb,usercsny,gamesytl,gamesydl,x,y,usergj,usersf,usercs,usercq,userdlzh,userdlmm,userlxdh,userdzyj,gpszt,jtsl,hysl,tdrs,zfbzh,zhye,his_table,hyyj,hycj,tdcj,tdyj,ver,yqm,sbly,wechatserviceid,iswechatnote,vipqxtdcyys,vipqxhyys,weunid,wechatid,(select top 1 wechatserviceid from JYAC_HYT.dbo.user_info where userid=86) as wdwxtzid',
            'tablename': 'JYAC_HYT.dbo.user_info nolock',
            'OrderBy': 'userid desc',
            'strwhere': f"and userzt=0 and userdlzh='{username}'"
        })