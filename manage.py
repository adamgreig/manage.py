#!/usr/bin/python
### Manage various server features
### Adam Greig, May 2010

import sys
import linode, system, cherokee
from menu import menu

def main_menu(domain):
    options = {'1': 'Linode API', '2': 'System', 
               '3': 'Cherokee', 'q': 'Quit'}
    choice = menu('Main Menu:', domain, options)
    if choice == '1':
        linode.linode_menu(domain)
    elif choice == '2':
        system.system_menu(domain)
    elif choice == '3':
        cherokee.cherokee_menu(domain)
    elif choice == 'q':
        sys.exit(0)

def main():
    print 'manage.py v0.2'
    print 'Adam Greig 05/2010'
    print ''
    domain = raw_input('Domain name: ')
    while 1:
        main_menu(domain)

if __name__ == '__main__':
    main()
