# -*- coding: utf-8 -*-

import logging
import uvclight
#from os import path
from fanstatic import Library, Resource  #, Group
from nva.psyquizz.models.interfaces import IQuizzSecurity
from grokcore.component import context, Subscription
from zope.interface import Interface, implementer
from nva.psyquizz.models.quizz.quizz5 import IQuizz5


library = Library('psyquizz.rcitheme', 'static')
rcicss = Resource(library, 'rci.css')


def get_template(name):
    return uvclight.get_template(name, __file__)


@implementer(IQuizzSecurity)
class SecurityCheck(Subscription):
    context(Interface)

    def check(self, name, quizz, context):
        if IQuizz5.implementedBy(quizz):
            return True
        return False 
