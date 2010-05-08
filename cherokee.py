### Cherokee functionality for manage.py

import os
from menu import menu
import settings

simple_vhost_dir = settings.cherokee_simple_vhost_dir
vhost_dir = settings.cherokee_vhost_dir
mkdir = settings.cherokee_mkdir
rm = settings.cherokee_rm

def add_simple_vhost(domain):
    result = os.system(mkdir + ' ' + simple_vhost_dir + '/' + domain)
    if result != 0:
        print 'Error adding directory, mkdir returned non-zero'
    else:
        print 'Directory added successfully, place files in:'
        print simple_vhost_dir + '/' + domain

def delete_simple_vhost(domain):
    pass

def add_vhost(domain):
    pass

def delete_vhost(domain):
    pass

def enable_php(domain):
    pass

def disable_php(domain):
    pass

def disable_vhost(domain):
    pass

def enable_vhost(domain):
    pass

def cherokee_menu(domain):
    options = {'1': 'Add simple vhost', '2': 'Delete simple vhost',
               '3': 'Add vhost', '4': 'Delete vhost',
               '5': 'Enable PHP', '6': 'Disable PHP',
               '7': 'Disable vhost', '8': 'Enable vhost',
               'b': 'Back'}

    while 1:
        choice = menu('Cherokee', domain, options)

        if choice == '1':
            add_simple_vhost(domain)
        elif choice == '2':
            delete_simple_vhost(domain)
        elif choice == '3':
            add_vhost(domain)
        elif choice == '4':
            delete_vhost(domain)
        elif choice == '5':
            enable_php(domain)
        elif choice == '6':
            disable_php(domain)
        elif choice == '7':
            disable_vhost(domain)
        elif choice == '8':
            enable_vhost(domain)
        elif choice == 'b':
            return

