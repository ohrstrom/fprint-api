# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import post_save
from django.dispatch import receiver
from authtools.models import AbstractEmailUser


@python_2_unicode_compatible
class User(AbstractEmailUser):

    pass

    class Meta(AbstractEmailUser.Meta):
        app_label = 'auth_extra'
        db_table = 'auth_user'
        swappable = 'AUTH_USER_MODEL'
        verbose_name = _('User Account')
        verbose_name_plural = _('User Accounts')


    def __str__(self):
        # if self.username:
        #     return '{}'.format(self.username)
        return '{}'.format(self.email)
