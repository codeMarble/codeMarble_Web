from sqlalchemy import and_, not_, or_

from codeMarble_Web.database import dao
from codeMarble_Web.model.user import User


def insert_user(userId, password, nickName, eMail, authority='user'):
    print userId, password, nickName, eMail, authority
    return User(userId=userId,
                password=password,
                nickName=nickName,
                eMail=eMail,
                lastMatchDate=None,
                authority=authority)


def select_user(userIndex=None, userId=None, nickName=None, authority=None):
    if userIndex:
        return dao.query(User).\
                    filter(User.userIndex == userIndex)

    elif userId:
        return dao.query(User).\
                    filter(User.userId ==userId)

    elif nickName:
        return dao.query(User).\
                    filter(User.nickName == nickName)

    elif authority:
        return dao.query(User).\
                    filter(User.authority == authority)

    else:
        dao.query(User)


def update_user(userIndex, password=None, nickName=None, eMail=None, lastMatchDate=None, authority=None):
    return dao.query(User).\
                filter(User.userIndex == userIndex).\
                update(dict(password = password if password else User.password,
                            nickName = nickName if nickName else User.nickName,
                            eMail = eMail if eMail else User.eMail,
                            lastMatchDate = lastMatchDate if lastMatchDate else User.lastMatchDate,
                            authority = authority if authority else User.authority))
    # data update example
    # try:
    #     update_user(xx, xx, xx, xx)
    #     dao.commit()
    #
    # except Exception as e:
    #     dao.rollback()