# -*- coding: utf-8 -*-
"""
    Yahoo fantasy basketball data analysis display

    copyright: (c) 2022 by Shaozuo Huang
"""

from flask_login import UserMixin

class User( UserMixin):
    '''
    Represents a user playing yahoo fantasy basketball.
    '''
    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    # override method
    def get_id(self):
        return self.guid

    def __init__(self, guid):
        self.guid = guid





