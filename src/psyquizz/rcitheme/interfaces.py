# -*- coding: utf-8 -*-

from grokcore.component import provider
from nva.psyquizz.models import deferred_vocabularies
from nva.psyquizz.models.interfaces import IAccount
from uvc.themes.btwidgets import IBootstrapRequest
from zope.interface import Interface
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary


class IRCITheme(IBootstrapRequest):
     pass


@provider(IContextSourceBinder)
def vocab_type(context):
    rc = [SimpleTerm('1', '1', u'Baustoffe - Steine – Erden'),
        SimpleTerm('2', '2', u'Bergbau'),
        SimpleTerm('3', '3', u'Chemische Industrie'),
        SimpleTerm('4', '4', u'Lederindustrie'),
        SimpleTerm('5', '5', u'Papierherstellung und Ausrüstung'),
        SimpleTerm('6', '6', u'Zucker'),
    ]
    return SimpleVocabulary(rc)


@provider(IContextSourceBinder)
def vocab_employees(context):
    rc = [SimpleTerm('1', '1', u'Weniger als 10'),
        SimpleTerm('2', '2', u'10-49 Ma'),
        SimpleTerm('3', '3', u'50-249 Ma'),
        SimpleTerm('4', '4', u'250-499 Ma'),
        SimpleTerm('5', '5', u'Größer 500 Ma')
    ]
    return SimpleVocabulary(rc)


deferred_vocabularies['type'] = vocab_type
deferred_vocabularies['employees'] = vocab_employees
