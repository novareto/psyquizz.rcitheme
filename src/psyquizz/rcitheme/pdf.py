# -*- coding: utf-8 -*-
# Copyright (c) 2007-2021 NovaReto GmbH
# cklinger@novareto.de

import uvclight
import datetime

from .interfaces import IRCITheme
from reportlab.lib.units import cm
from reportlab.platypus import Paragraph
from nva.psyquizz.browser.pdf import GeneratePDF, FRONTPAGE, styles, PageBreak
from nva.psyquizz.browser.pdf.quizz5 import Quizz5PDF


class Quizz5PDF(Quizz5PDF):
    uvclight.layer(IRCITheme)

    def frontpage(self, parts):
        crit_style = self.crit_style()
        parts.append(Paragraph(u'Auswertungsbericht', styles['Heading1']))
        parts.append(Paragraph(u'„psyBel Befragung“ – Gefährdungsbeurteilung psychischer Belastung', styles['Heading2']))
        fp = FRONTPAGE % (
            self.context.course.company.name,
            self.context.course.title,
            self.context.startdate.strftime('%d.%m.%Y'),
            self.context.enddate.strftime('%d.%m.%Y'),
            crit_style,
            self.request.form.get('total', ''),
            datetime.datetime.now().strftime('%d.%m.%Y'))
        parts.append(Paragraph(fp.strip(), styles['Normal']))
        parts.append(PageBreak())
        return


    def headerfooter(self, canvas, doc):
        canvas.setFont("Helvetica", 9)
        canvas.drawString(1 * cm, 2 * cm, u"psyBel Befragung")
        canvas.drawString(1 * cm, 1.6 * cm, u"Gefährdungsbeurteilung psychischer Belastung")
        canvas.drawString(1 * cm, 1.2 * cm, u"Ein Programm der BG RCI")
        canvas.drawString(15 * cm, 2 * cm, u"Grundlage der Befragung:")
        canvas.drawString(15 * cm, 1.6 * cm, u"FBGU-Fragebogen")
        canvas.setFont("Helvetica", 12)

