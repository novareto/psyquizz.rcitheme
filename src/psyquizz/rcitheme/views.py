import uvclight
import itertools
from zope import interface
from zope import schema
from . import get_template
from .interfaces import IVBGTheme
from dolmen.forms.base.actions import Action, Actions
from nva.psyquizz.interfaces import ICompanyRequest
from nva.psyquizz.browser.invitations import DownloadLetter, DEFAULT
from nva.psyquizz.browser.lib.emailer import SecureMailer, prepare, ENCODING
from dolmen.forms.base import FAILURE
from dolmen.forms.base.widgets import FieldWidget
from cromlech.file import FileField
from dolmen.widget.file import FileSchemaField
from zope.interface import Interface
from zope.schema import interfaces as schema_interfaces
from dolmen.forms.base.datamanagers import ObjectDataManager
import xlrd
from nva.psyquizz.apps.company import AnonIndex


class AnonIndex(AnonIndex):
    uvclight.layer(IVBGTheme)
    template = get_template('anon_index_new.pt')


class Datenschutz(uvclight.Page):
    uvclight.context(interface.Interface)
    uvclight.layer(ICompanyRequest)
    uvclight.auth.require('zope.Public')

    template = get_template('datenschutz.cpt')


class IEmailer(interface.Interface):
    emails = FileField(title=u"Recipients", required=False)


class EmailAction(Action):

    def tokens(self, form):
        url = form.application_url() + '/befragung'
        for a in itertools.chain(
                form.context.complete, form.context.uncomplete):
            yield url, str(a.access)

    def emails(self, xls):
        import pdb; pdb.set_trace()
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
                mail = prepare(from_, email, title, body, body)
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
    uvclight.layer(IVBGTheme)

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
