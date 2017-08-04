# -*- coding: utf-8 -*-

from sqlalchemy import *

from codeMarbleWeb.model.language import Language

from codeMarbleWeb.database import dao

def insert_language(language):
    return Language(language=language)

def select_languabe(languageIndex=None):
    return dao.query(Language).\
        filter(Language.languageIndex == languageIndex if languageIndex else Language.languageIndex != languageIndex)