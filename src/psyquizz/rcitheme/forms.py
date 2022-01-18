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
<p> herzlich Willkommen zu unserer Befragung „psyBel: Psychische Belastung erkennen – gesunde Arbeitsbedingungen gestalten“! Danke, dass Sie uns dabei unterstützen!</p>
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
CreateCompany.fields['mnr'].description = u"""Bitte tragen Sie hier die ersten acht Ziffern Ihrer Mitgliedsnummer ohne Zwischenpunkte ein (z.B.
50000492). So können wir sicherstellen, dass nur Mitgliedsbetriebe unserer Berufsgenossenschaft diesen
Service nutzen und somit keine Kosten durch nicht bei uns versicherte Betriebe entstehen. Ihre
Mitgliedsnummer wird nicht dauerhaft gespeichert. Ein Rückschluss auf Ihren Betrieb ist zu keinem
Zeitpunkt möglich."""

CreateCompany.fields['exp_db'].description = u"""Hier haben Sie die Möglichkeit, uns die Nutzung Ihrer Daten zu Forschungszwecken zu ermöglichen.
Indem Sie uns angeben, aus welcher Branche Ihr Betrieb stammt und wieviel Beschäftigte Sie haben,
helfen Sie uns bei der Entwicklung passgenauer Präventionsangebote für unsere Mitgliedsbetriebe. Bitte
beachten Sie, eine Rückführung der Daten auf Ihren Betrieb ist zu keinem Zeitpunkt möglich. Wir
speichern lediglich die Anzahl der Beschäftigten, die Branche sowie die Ergebnisse des Fragebogens."""

CreateCompany.fields['employees'].description = u"""Falls Sie der Nutzung Ihrer Daten zu Forschungszwecken zugestimmt haben, geben Sie bitte hier an, wie
viele Personen in Ihrem Betrieb beschäftigt sind."""

CreateCompany.fields['type'].title = u"Betriebsgegenstand:"
CreateCompany.fields['type'].description=u"""Bitte geben Sie hier an, welcher Branche Ihr Betrieb am ehesten zuzuordnen ist. Orientieren Sie sich hier
am Geschäftszweck Ihres Betriebes."""
