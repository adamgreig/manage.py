### Menu functionality for manage.py

def menu(text, domain, options):
    keys = options.keys()
    keys.sort()
    choice = None
    while choice not in keys:
        print ''
        print text
        print 'Domain: ' + domain
        for key in keys:
            print key + ') ' + options[key]
        print
        choice = raw_input('> ')
        if choice not in keys:
            print 'Invalid choice'
    return choice


