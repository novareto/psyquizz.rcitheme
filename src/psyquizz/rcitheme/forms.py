# -*- coding: utf-8 -*-
# Copyright (c) 2007-2019 NovaReto GmbH
# cklinger@novareto.de

import uvclight

from .interfaces import IRCITheme
from zope import schema, interface
from nva.psyquizz.models import IAccount
from nva.psyquizz.browser.forms import CreateAccount, CreateCompany, CreateCourse
from nva.psyquizz.browser.forms import IVerifyPassword, ICaptched
from nva.psyquizz.models.interfaces import ICompany


DESC = u"""
Ja, ich habe die Datenschutzhinweise und die Informationen nach Artikel 13 DSGVO gelesen und stimme diesen zu.
Ich willige ein, dass die VBG meine personenbezogenen Daten im Rahmen des bereitgestellten Online-Verfahrens
zur Gefährdungsbeurteilung psychische Belastung am Arbeitsplatz verarbeitet. Mir ist bekannt, dass ich die
Einwilligung jederzeit widerrufen kann. Durch den Widerruf der Einwilligung wird die Rechtmäßigkeit der
aufgrund der Einwilligung bis zum Widerruf erfolgten Verarbeitung nicht berührt.
"""



ABOUT_TEXT = u"""
<p>Liebe Kolleginnen und Kollegen,</p>
<p> herzlich Willkommen zu unserer Befragung „psyBel: Psychische Belastung erkennen – gesunde Arbeitsbedingungen gestalten“! </p>
<p>Bitte beantworten Sie alle Fragen des Fragebogens.
Beim Beantworten der Fragen kann es hilfreich sein, nicht zu lange über die einzelnen Fragen
nachzudenken. Meist ist der erste Eindruck auch der treffendste.</p>
<p>Wir möchten nochmal darauf hinweisen, dass Ihre Angaben absolut vertraulich behandelt werden. Ein Rückschluss auf einzelne Personen wird nicht möglich sein.</p>
<p>Sollten Sie Fragen oder Anmerkungen haben, wenden Sie sich bitte an:</p>
 <p>   <span> A n s p r e c h p a r t n e r   &nbsp;    und   &nbsp     K o n t a k t d a t e n </span> </p>
<p>Wir freuen uns auf Ihre Rückmeldungen!</p>
"""


class IAckForm(interface.Interface):

    ack_form = schema.Bool(
        title=u"Bestätigung",
        description=DESC,
        required=True,
    )

class CreateCourse(CreateCourse):
    uvclight.layer(IRCITheme)

    @property
    def fields(self):
        fields = super(CreateCourse, self).fields
        fields['about'].defaultValue = ABOUT_TEXT
        return fields.omit('extra_questions')


class CreateAccount(CreateAccount):
    uvclight.layer(IRCITheme)
    title = label = "Registrierung"
    description = u"Hier können Sie einen neun Benutzer registrieren."

    fields = (uvclight.Fields(IAccount).select('name', 'email', 'password')) + uvclight.Fields(IVerifyPassword) + uvclight.Fields(IAckForm)


CreateCompany.fields['mnr'].title = u"Mitgliedsnummer (z.B. 50.000.492.022)."
CreateCompany.fields['mnr'].description = u"Bitte geben Sie hier Ihrer Mitgliedsnummer bei der BG RCI ein."

CreateCompany.fields['exp_db'].description = u"""Ich stimme einer anonymisierten Erfassung meiner Umfrageergebnisse in einer Gesamtdatenbank zu.
Erfasst werden Branche, Anzahl der Beschäftigten sowie Gesamtergebnisse der Befragung. Dies
ermöglicht die Ableitung branchenspezifischer Präventionsangebote sowie die Erstellung von
Referenzwerten. Es ist kein Rückschluss auf einzelne Unternehmen oder Personen möglich."""
