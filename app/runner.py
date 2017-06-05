# -*- coding: utf-8 -*-

import os
import sys


def main(argv=None):
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings")
    os.environ['DJANGO_IS_MANAGEMENT_COMMAND'] = '1'

    from django.core.management import execute_from_command_line

    if argv is None:
        argv = sys.argv
    execute_from_command_line(argv)


if __name__ == "__main__":
    main()
