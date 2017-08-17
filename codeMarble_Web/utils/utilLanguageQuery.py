# -*- coding: utf-8 -*-

from sqlalchemy import *

from codeMarble_Web.model.language import Language

from codeMarble_Web.database import dao

def insert_language(language):
    return Language(language=language)

def select_language(languageIndex=None, language=None):
    if language:
        return dao.query(Language). \
            filter(Language.language == language)

    return dao.query(Language).\
                filter(Language.languageIndex == languageIndex if languageIndex else Language.languageIndex != languageIndex)