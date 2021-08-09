# -*- coding: utf-8 -*-
# Copyright (c) 2007-2019 NovaReto GmbH
# cklinger@novareto.de

import uvclight

from .interfaces import IRCITheme
from zope import schema, interface
from nva.psyquizz.models import IAccount
from nva.psyquizz.browser.forms import CreateAccount, CreateCompany
from nva.psyquizz.browser.forms import IVerifyPassword, ICaptched
from nva.psyquizz.models.interfaces import ICompany


DESC = u"""
Ja, ich habe die Datenschutzhinweise und die Informationen nach Artikel 13 DSGVO gelesen und stimme diesen zu.
Ich willige ein, dass die VBG meine personenbezogenen Daten im Rahmen des bereitgestellten Online-Verfahrens
zur Gefährdungsbeurteilung psychische Belastung am Arbeitsplatz verarbeitet. Mir ist bekannt, dass ich die
Einwilligung jederzeit widerrufen kann. Durch den Widerruf der Einwilligung wird die Rechtmäßigkeit der
aufgrund der Einwilligung bis zum Widerruf erfolgten Verarbeitung nicht berührt.
"""



class IAckForm(interface.Interface):

    ack_form = schema.Bool(
        title=u"Bestätigung",
        description=DESC,
        required=True,
    )

class CreateAccount(CreateAccount):
    uvclight.layer(IRCITheme)

    fields = (uvclight.Fields(IAccount).select('name', 'email', 'password') +
        uvclight.Fields(IVerifyPassword, ICaptched)) + uvclight.Fields(IAckForm)


CreateCompany.fields['mnr'].description = u"Bitte geben Sie hier die ersten acht Stellen Ihrer Mitgliedsnummer bei der VBG ein."
