# -*- coding: utf-8 -*-
import uvclight
import itertools
from zope import interface
from zope import schema
from . import get_template
from .interfaces import IRCITheme, IRCIRegTheme
from dolmen.forms.base.actions import Action, Actions
from nva.psyquizz.interfaces import ICompanyRequest
from nva.psyquizz.browser.invitations import DownloadLetter, DEFAULT
from nva.psyquizz.browser.frontpages import AccountHomepage
from nva.psyquizz.emailer import SecureMailer, ENCODING
from dolmen.forms.base import FAILURE
from dolmen.forms.base.widgets import FieldWidget
from cromlech.file import FileField
from dolmen.widget.file import FileSchemaField
from zope.interface import Interface
from zope.schema import interfaces as schema_interfaces
from dolmen.forms.base.datamanagers import ObjectDataManager
import xlrd
from nva.psyquizz.apps.company import AnonIndex
from nva.psyquizz.browser.forms import CreateAccount
from nva.psyquizz.browser.invitations import ExampleText
from nva.psyquizz.browser.results import Quizz5Charts
from .forms import CreateAccount


class Quizz5Charts(Quizz5Charts):
    uvclight.layer(IRCITheme)
    description = u"""
    <p>
      Hier sehen Sie die Auswertung für alle Beschäftigten.
    </p>
    <p>
      Durch Auswahl einer oder mehrerer Auswertungsgruppen haben Sie die
      Möglichkeit sich eine detaillierte Auswertung anzeigen zu lassen.
      (Bitte beachten Sie: Einzelne Auswertungsgruppen können erst ausgewählt
      werden, wenn für diese Auswertungsgruppe mindestens sieben ausgefüllte
      Fragebögen vorliegen.)
    </p>
    <p>
      Informationen über den weiteren Umgang mit den Ergebnissen finden Sie auf der Homepage des psyBel
Programms ab Schritt 4: Bewerten des Risikos - BG RCI
    </p>
    """
    #template = uvclight.get_template('quizz5_result.pt', __file__)


class ExampleText(ExampleText):
    uvclight.layer(IRCITheme)

    @property
    def template(self):
        template = "example_text.pt"
        #if self.context.strategy == "fixed":
        #    template = "example_text_fixed.pt"
        return uvclight.get_template(template, __file__)


class CreateAccount(CreateAccount):
    uvclight.layer(IRCIRegTheme)

    #@property
    #def fields(self):
    #    fields = super(CreateAccount, self).fields
    #    return fields.omit('captcha')


class AnonIndex(AnonIndex):
    uvclight.layer(IRCITheme)
    template = get_template('anon_index_new.pt')



class RCIAccountHomepage(AccountHomepage):
    uvclight.layer(IRCITheme)

    template = get_template('frontpage.pt')


class Datenschutz(uvclight.Page):
    uvclight.context(interface.Interface)
    uvclight.layer(ICompanyRequest)
    uvclight.auth.require('zope.Public')

    template = get_template('datenschutz.cpt')


class Impressum(uvclight.Page):
    uvclight.name('impressum')
    uvclight.context(interface.Interface)
    uvclight.layer(IRCITheme)
    uvclight.auth.require('zope.Public')

    template = get_template('impressum.cpt')


class IEmailer(interface.Interface):
    emails = FileField(title=u"Recipients", required=False)


class EmailAction(Action):

    def tokens(self, form):
        url = form.application_url() + '/befragung'
        for a in itertools.chain(
                form.context.complete, form.context.uncomplete):
            yield url, str(a.access)

    def emails(self, xls):
        workbook = xlrd.open_workbook(file_contents=xls.file.read())
        sheet = workbook.sheet_by_index(0)
        for i in range(0, sheet.nrows):
            yield sheet.cell(i, 0).value

    @staticmethod
    def send(smtp, text, tokens, *recipients):
        mailer = SecureMailer(smtp)  # BBB
        from_ = 'extranet@bgetem.de'
        title = (u'FIX ME').encode(ENCODING)

        with mailer as sender:
            for email in recipients:
                url, token = next(tokens)
                body = "%s\r\n\r\nDie Internetadresse lautet: <b> %s/befragung</b> <br/> Ihr Kennwort lautet: <b> %s</b>" % (text.encode('utf-8'), url, token)
                mail = mailer.prepare(from_, email, title, body, body)
                sender(from_, email, mail.as_string())

    def __call__(self, form):
        data, errors = form.extractData()
        if errors:
            form.flash(u"Es ist ein Fehler aufgetreten")
            return FAILURE

        tokens = self.tokens(form)
        recipients = self.emails(data['emails'])
        smtp = uvclight.getSite().configuration.smtp_server
        sent = self.send(smtp, data['text'], tokens, *recipients)
        response = form.responseFactory()
        response.redirect(form.url(form.context), status=302)
        return response


class Letter:

    def __init__(self, text, emails=None):
        self.text = text
        self.emails = emails


class LetterEmailer(DownloadLetter):
    uvclight.name('downloadletter')
    uvclight.layer(IRCITheme)

    fields = DownloadLetter.fields + uvclight.Fields(IEmailer)
    fields['emails'].interface = IEmailer  # TEMPORARY FIX
    actions = DownloadLetter.actions + Actions(EmailAction('Send by mail'))

    def update(self):
        DE = DEFAULT % (
            self.context.startdate.strftime('%d.%m.%Y'),
            self.context.enddate.strftime('%d.%m.%Y'),
            )
        defaults = Letter(DE, emails=None)
        self.setContentData(ObjectDataManager(defaults))




