# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible

from django.utils.translation import ugettext_lazy as _
from authtools.models import AbstractEmailUser


@python_2_unicode_compatible
class User(AbstractEmailUser):

    class Meta(AbstractEmailUser.Meta):
        app_label = 'auth_extra'
        db_table = 'auth_user'
        swappable = 'AUTH_USER_MODEL'
        verbose_name = _('User Account')
        verbose_name_plural = _('User Accounts')


    def __str__(self):
        return '{}'.format(self.email)
