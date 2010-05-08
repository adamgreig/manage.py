### System level functionality for manage.py

import os
import sys
from subprocess import Popen, PIPE
from menu import menu
import settings
base_dir = settings.system_home_base_dir
useradd = settings.system_useradd
userdel = settings.system_userdel
rm = settings.system_rm

def add_user(domain):
    password = Popen(['/usr/bin/pwgen', '-cnB', '16', '1'], stdout=PIPE)
    password = password.communicate()[0][0:15]
    cmd = useradd + ' -Umb ' + base_dir + ' -p ' + password + ' ' + domain
    result = os.system(cmd)
    if result != 0:
        print 'Error adding user, non-zero return from useradd.'
    else:
        print 'User added successfully with password ' + password

def delete_user(domain):
    print 'Are you totally sure you want to delete this user?'
    conf = raw_input('Enter the domain again to confirm: ')
    if conf == domain:
        cmd = userdel + ' ' + domain
        result = os.system(cmd)
        if result != 0:
            print 'Error deleting user, non-zero return from userdel.'
        else:
            print 'User deleted successfully.'
    else:
        print 'Incorrect confirmation, cancelling.'

def delete_user_files(domain):
    print 'Are you totally sure you want to delete all of this domain\'s files?'
    print 'This cannot be undone and is generally a bad idea.'
    print 'Type "Yes, I\'m totally sure I want to delete all the files and',
    print 'know that this is generally a bad idea." to continue.'
    conf = raw_input('')
    if conf != "Yes, I'm totally sure I want to delete all the files and" + \
            " know that this is generally a bad idea.":
        print "Incorrect confirmation, stopping."
        return
    conf = raw_input('Confirm the domain whose files are being deleted: ')
    if conf != domain:
        print "Incorrect confirmation, stopping."
        return
    if domain.find('/') != -1 or domain.find('..') != -1:
        print "Illegal characters in domain name, stopping."
        return
    cmd = rm + " -rf " + base_dir + "/" + domain + "/"
    print 'About to run: '
    print cmd
    conf = raw_input("Last chance! Continue? y/N: ")
    if conf != 'y':
        print 'Stopping.'
        return
    os.system(cmd)
    print 'Files deleted.'

def system_menu(domain):
    options = {'1': 'Add user', '2': 'Delete user', '3': 'Delete user files',
               'b': 'Back'}
    while 1:
        choice = menu('System', domain, options)
        if choice == '1':
            add_user(domain)
        elif choice == '2':
            delete_user(domain)
        elif choice == '3':
            delete_user_files(domain)
        elif choice == 'b':
            return
