from sqlalchemy import and_, not_, or_

from codeMarbleWeb.database import dao
from codeMarbleWeb.model.notice import Notice


def insert_notice(userIndex, content):
    return Notice(userIndex=userIndex, content=content, isRead=False)

def select_notice(userIndex):
    return dao.query(Notice).\
                filter(Notice.userIndex == userIndex)

def update_notice_read(noticeIndex, userIndex):
    return dao.query(Notice).\
                filter(and_(Notice.noticeIndex == noticeIndex,
                            Notice.userIndex == userIndex)).\
                update(dict(isRead = True))