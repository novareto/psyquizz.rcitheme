# -*- coding: utf-8 -*-

from grokcore.component import provider
from zope.interface import Interface
from uvc.themes.btwidgets import IBootstrapRequest
from nva.psyquizz.models import deferred_vocabularies
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary
from nva.psyquizz.models.interfaces import IAccount


class IVBGTheme(IBootstrapRequest):
     pass


@provider(IContextSourceBinder)
def vocab_type(context):
    rc = [SimpleTerm('1', '1', u'Zeitarbeit'),
        SimpleTerm('2', '2', u'Bildungseinrichtungen'),
        SimpleTerm('3', '3', u'Bühnen und Studios'),
        SimpleTerm('4', '4', u'Keramische und Glas-Industrie'),
        SimpleTerm('5', '5', u'Kirchen'),
        SimpleTerm('6', '6', u'Kreditinstitute und Spielstätten'),
        SimpleTerm('7', '7', u'ÖPNV/Bahnen'),
        SimpleTerm('8', '8', u'Sicherungsdienstleistungen'),
        SimpleTerm('9', '9', u'Sport'),
        SimpleTerm('15', '15', u'sonstige'),
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
