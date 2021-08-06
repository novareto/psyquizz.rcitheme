# -*- coding: utf-8 -*-

import uvclight
from dolmen.template import ITemplate
from dolmen.message import receive
from uvc.design.canvas import menus, managers
from uvc.design.canvas.viewlets import MenuViewlet
from uvc.content.interfaces import IContent
from grokcore.component import adapter, implementer
from nva.psyquizz.browser.viewlets import PersonalMenuViewlet
from .interfaces import IRCITheme
from . import get_template
from siguvtheme.uvclight.viewlets import BGHeader
from zope import interface


class RCIFooter(uvclight.ViewletManager):
    uvclight.context(interface.Interface)
    uvclight.name('rcifooter')
    template = get_template('rcifooter.cpt')

    def update(self):
        pass



class BGHeader(BGHeader):
    uvclight.layer(IRCITheme)
    template = get_template('header.cpt')


class Disable(PersonalMenuViewlet):
    uvclight.name('personalmenuviewlet')
    uvclight.layer(IRCITheme)

    def available(self):
        return False

    def update(self):
        pass
    
    def render(self):
        return u''


class Tabs(uvclight.ViewletManager):
    uvclight.name('tabs')
    uvclight.layer(IRCITheme)
    uvclight.context(uvclight.Interface)
    uvclight.implements(managers.ITabs)


class Navigation(uvclight.ViewletManager):
    uvclight.name('navigation')
    uvclight.layer(IRCITheme)
    uvclight.context(uvclight.Interface)

    def application_url(self):
        return self.view.application_url()


class PageTop(uvclight.ViewletManager):
    uvclight.name('pagetop')
    uvclight.layer(IRCITheme)
    uvclight.context(uvclight.Interface)
    uvclight.implements(managers.IPageTop)


class Headers(uvclight.ViewletManager):
    uvclight.name('headers')
    uvclight.layer(IRCITheme)
    uvclight.context(uvclight.Interface)
    uvclight.implements(managers.IHeaders)


class AboveContent(uvclight.ViewletManager):
    uvclight.name('above-body')
    uvclight.layer(IRCITheme)
    uvclight.context(uvclight.Interface)
    uvclight.implements(managers.IAboveContent)


class BelowContent(uvclight.ViewletManager):
    uvclight.name('below-body')
    uvclight.layer(IRCITheme)
    uvclight.context(uvclight.Interface)
    uvclight.implements(managers.IBelowContent)


class Footer(uvclight.ViewletManager):
    uvclight.name('footer')
    uvclight.layer(IRCITheme)
    uvclight.context(uvclight.Interface)
    uvclight.implements(managers.IFooter)


class ObjectActionMenuViewlet(MenuViewlet):
    uvclight.viewletmanager(managers.IAboveContent)
    uvclight.context(IContent)
    uvclight.layer(IRCITheme)
    uvclight.order(10)
    menu = menus.ContextualActionsMenu


class AddMenuViewlet(MenuViewlet):
    uvclight.viewletmanager(managers.IAboveContent)
    uvclight.layer(IRCITheme)
    uvclight.order(20)
    menu = menus.AddMenu


class FooterViewlet(MenuViewlet):
    uvclight.viewletmanager(managers.IFooter)
    uvclight.layer(IRCITheme)
    uvclight.order(20)

    menu = menus.PersonalMenu
    template = get_template('footer.cpt')

    def getFooter(self):
        menu = menus.FooterMenu(self.context, self.request, self.view)
        menu.update()
        return menu.entries


class DocumentActionsViewlet(MenuViewlet):
    uvclight.viewletmanager(managers.IAboveContent)
    uvclight.layer(IRCITheme)
    uvclight.order(20)

    template = get_template('documentactionstemplate.cpt')
    name = u'Aktion'
    id = u'documentactionsviewlet'

    def update(self):
        self.menu = menus.DocumentActionsMenu(
            self.context, self.request, self.view)
        self.menu.update()


class NavigationMenuViewlet(MenuViewlet):
    uvclight.viewletmanager(Navigation)
    uvclight.layer(IRCITheme)
    uvclight.order(30)

    menu = menus.NavigationMenu
    template = get_template('navigationtemplate.cpt')

    id = u'globalmenuviewlet'

    def getNavigation(self):
        menu = menus.NavigationMenu(self.context, self.request, self.view)
        menu.update()
        return menu.entries

    def getUser(self):
        menu = menus.UserMenu(self.context, self.request, self.view)
        menu.update()
        return menu.entries

    def getRenderableItems(self):
       return list()

    def getQuicklinks(self):
        menu = menus.Quicklinks(self.context, self.request, self.view)
        menu.update()
        return menu.entries

    def getPersonal(self):
        menu = menus.PersonalMenu(self.context, self.request, self.view)
        menu.update()
        return menu.entries

    
class FlashMessages(uvclight.Viewlet):
    uvclight.order(2)
    uvclight.layer(IRCITheme)
    uvclight.viewletmanager(managers.IAboveContent)
    template = uvclight.get_template('flash.cpt', __file__)

    def update(self):
        self.messages = [msg.message for msg in receive()]
