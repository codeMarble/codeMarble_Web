from sqlalchemy import and_, not_, or_

from codeMarbleWeb.database import dao
from codeMarbleWeb.model.user import User


def insert_user(userId, password, nickName, eMail, authority='user'):
    User(userId=userId, password=password, nickName=nickName, eMail=eMail, authority=authority)
    # data insert example
    # try:
    #     dao.add(insert_user(xx, xx, xx, xx, xx))
    #     dao.commit()
    # except Exception as e:
    #     dao.rollback()

def select_user(userIndex=None, userId=None, nickName=None):
    if userIndex:
        return dao.query(User).\
                    filter(User.userIndex == userIndex)

    elif userId:
        return dao.query(User).\
                    filter(User.userId ==userId)

    elif nickName:
        return dao.query(User).\
                    filter(User.nickName == nickName)

    else:
        dao.query(User)

def update_user(userIndex, password=None, nickName=None, eMail=None, authority=None):
    return dao.query(User).\
                filter(User.userIndex == userIndex).\
                update(dict(password = password if password else User.password,
                            nickName = nickName if nickName else User.nickName,
                            eMail = eMail if eMail else User.eMail,
                            authority = authority if authority else User.authority))
    # data update example
    # try:
    #     update_user(xx, xx, xx, xx)
    #     dao.commit()
    #
    # except Exception as e:
    #     dao.rollback()