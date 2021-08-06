# -*- coding: utf-8 -*-

import logging
import uvclight
#from os import path
from fanstatic import Library, Resource  #, Group


library = Library('psyquizz.rcitheme', 'static')
rcicss = Resource(library, 'rci.css')


def get_template(name):
    return uvclight.get_template(name, __file__)
