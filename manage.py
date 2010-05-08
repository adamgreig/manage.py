### Manage various server features
### Adam Greig, May 2010

import sys
import linode
from menu import menu

def main_menu(domain):
    options = {'1': 'Linode API', 'q': 'Quit'}
    choice = menu('Main Menu:', domain, options)
    if choice == '1':
        linode.linode_menu(domain)
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
