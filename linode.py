### Linode API functionality for manage.py

from menu import menu
import settings
import api
apikey = settings.linode_api_key
linode = api.Api(apikey)

dns_ttl = settings.linode_dns_ttl
dns_a = settings.linode_dns_a

dns_base = (
	( 'A', '', str(dns_a), 0 ),
	( 'A', 'www', str(dns_a), 0 ),
)

dns_google_mail = (
	( 'CNAME', 'mail', 'ghs.google.com', 0 ),
	( 'CNAME', 'pop', 'pop.googlemail.com', 0 ),
	( 'CNAME', 'imap', 'imap.googlemail.com', 0 ),
	( 'CNAME', 'smtp', 'smtp.googlemail.com', 0 ),
	( 'TXT', '', 'v=spf1 a include:aspmx.googlemail.com -all', 0 ),
	( 'MX', '', 'aspmx.l.google.com', 1 ),
	( 'MX', '', 'alt1.aspmx.l.google.com', 5 ),
	( 'MX', '', 'alt2.aspmx.l.google.com', 5 ),
	( 'MX', '', 'aspmx2.googlemail.com', 10 ),
	( 'MX', '', 'aspmx3.googlemail.com', 10 ),
)

dns_google_apps = (
	( 'CNAME', 'calendar', 'ghs.google.com', 0 ),
	( 'CNAME', 'docs', 'ghs.google.com', 0 ),
	( 'CNAME', 'start', 'ghs.google.com', 0 )
)

dns_google_chat = (
	( 'SRV', '_xmpp-server._tcp',
            '5 0 5269 xmpp-server.l.google.com', 0 ),
	( 'SRV', '_xmpp-server._tcp',
            '20 0 5269 xmpp-server1.l.google.com', 0 ),
	( 'SRV', '_xmpp-server._tcp',
            '20 0 5269 xmpp-server2.l.google.com', 0 ),
	( 'SRV', '_xmpp-server._tcp',
            '20 0 5269 xmpp-server3.l.google.com', 0 ),
	( 'SRV', '_xmpp-server._tcp',
            '20 0 5269 xmpp-server4.l.google.com', 0 ),
	( 'SRV', '_jabber._tcp', '5 0 5269 xmpp-server.l.google.com', 0 ),
	( 'SRV', '_jabber._tcp', '20 0 5269 xmpp-server1.l.google.com', 0 ),
	( 'SRV', '_jabber._tcp', '20 0 5269 xmpp-server2.l.google.com', 0 ),
	( 'SRV', '_jabber._tcp', '20 0 5269 xmpp-server3.l.google.com', 0 ),
	( 'SRV', '_jabber._tcp', '20 0 5269 xmpp-server4.l.google.com', 0 ),
	( 'SRV', '_xmpp-client._tcp', '5 0 5222 talk.l.google.com', 0 ),
	( 'SRV', '_xmpp-client._tcp', '20 0 5222 talk1.l.google.com', 0 ),
	( 'SRV', '_xmpp-client._tcp', '20 0 5222 talk2.l.google.com', 0 ),
)

def get_domain_id(domain):
    domain_list = linode.domain_list()
    domain_id = 0
    for d in domain_list:
        if d.has_key('DOMAINID') and d.has_key('DOMAIN'):
            if d['DOMAIN'].lower() == domain.lower():
                domain_id = d['DOMAINID']
    if domain_id == 0:
        print 'Could not find domain in domain list, stopping.'
        return 0
    else:
        return domain_id

def list_dns_records(domain):
    domain_id = get_domain_id(domain)
    if domain_id == 0:
        return

    record_list = linode.domain_resource_list(DomainID=domain_id)
    for rr in record_list:
        print str(rr['RESOURCEID']) + ":",
        print rr['TYPE'] + ", " + rr['NAME'] + ", " + rr['TARGET'],
        print "(" + str(rr['PRIORITY']) + ") [" + str(rr['TTL_SEC']) + "]"

def add_dns_records(domain, records):
    domain_id = get_domain_id(domain)
    if domain_id == 0:
        return
    
    for record in records:
        print "Creating a record with:",
        print "DomainID: " + str(domain_id),
        print "Type: " + record[0],
        print "Name: " + record[1],
        print "Target: " + record[2],
        print "Priority: " + str(record[3]),
        print "TTL_sec: " + str(dns_ttl)
        try:
            result = linode.domain_resource_create(DomainID=domain_id,
                    Type=record[0], Name=record[1], Target=record[2],
                    Priority=record[3], TTL_sec=dns_ttl)
        except api.ApiError as err:
            print 'Error adding record:', 
            print err
    print 'Records added.'

def add_dns_custom(domain):
    domain_id = get_domain_id(domain)
    if domain_id == 0:
        return

    Type = raw_input("Type: ")
    Name = raw_input("Name: ")
    Target = raw_input("Target: ")
    Priority = raw_input("Priority: ")
    try:
        Priority = int(Priority)
    except ValueError:
        Priority = 0
    
    try:
        linode.domain_resource_create(DomainID=domain_id, Type=Type,
                Name=Name, Target=Target, Priority=Priority, TTL_sec=dns_ttl)
    except api.ApiError as err:
        print 'Error adding record:',
        print err
    else:
        print 'Record added.'

def delete_dns_records(domain):
    conf = 'Are you sure you wish to delete all DNS records for this domain?'
    conf = raw_input(conf + ' y/N: ')
    if conf != 'y':
        return

    domain_id = get_domain_id(domain)
    if domain_id == 0:
        return

    record_list = linode.domain_resource_list(DomainID=domain_id)
    for rr in record_list:
        record_id = rr['RESOURCEID']
        try:
            print 'Deleting ' + str(record_id) + ' (' + rr['TYPE'],
            print ', ' + rr['NAME'] + ', ' + rr['TARGET'] + ')'
            linode.domain_resource_delete(DomainID=domain_id,
                   ResourceID=record_id)
        except api.ApiError as err:
            print 'Error deleting record:',
            print err
    print 'Records deleted.'

def list_dns_domains(current_domain):
    domain_list = linode.domain_list()
    for domain in domain_list:
        if domain.has_key('DOMAINID') and domain.has_key('DOMAIN'):
            print str(domain['DOMAINID']) + ': ' + domain['DOMAIN'],
            if domain['DOMAIN'].lower() == current_domain.lower():
                print " (*)",
            print

def add_dns_domain(domain):
    result = linode.domain_create(Domain=domain, Type='master',
            SOA_Email='random@randomskk.net', TTL_Sec=dns_ttl)
    if result.has_key('DomainID'):
        print 'DNS domain created with ID ' + str(result['DomainID'])
    else:
        print 'Error creating DNS domain.'

def delete_dns_domain(domain):
    conf = raw_input('Are you sure you want to delete this DNS domain? y/N: ')
    if conf != 'y':
        return

    domain_id = get_domain_id(domain)
    if domain_id == 0:
        return

    try:
        result = linode.domain_delete(DomainID=domain_id)
    except api.ApiError as err:
        print 'Error deleting domain:',
        print err
    else:
        print 'Domain ' + str(domain_id) + ' deleted.'
        return


def add_dns_records_menu(domain):
    options = {'1': 'Add base DNS entries (a,ns)',
               '2': 'Add Google Mail DNS entries (cname, txt, mx)',
               '3': 'Add Google Apps DNS entries (cname)',
               '4': 'Add Google Chat DNS entries (SRV)',
               '5': 'Add custom DNS entry',
               'b': 'Back'}

    while 1:
        choice = menu('Linode API > Add DNS Records', domain, options)
        if choice == '1':
            add_dns_records(domain, dns_base)
        elif choice == '2':
            add_dns_records(domain, dns_google_mail)
        elif choice == '3':
            add_dns_records(domain, dns_google_apps)
        elif choice == '4':
            add_dns_records(domain, dns_google_chat)
        elif choice == '5':
            add_dns_custom(domain)
        elif choice == 'b':
            return


def linode_menu(domain):
    options = {'1': 'List DNS domains', '2': 'List DNS records',
               '3': 'Add DNS domain', '4': 'Add DNS records',
               '5': 'Delete DNS records', '6': 'Delete DNS domain',
               'b': 'Back'}

    while 1:
        choice = menu('Linode API', domain, options)
        if choice == '1':
            list_dns_domains(domain)
        elif choice == '2':
            list_dns_records(domain)
        elif choice == '3':
            add_dns_domain(domain)
        elif choice == '4':
            add_dns_records_menu(domain)
        elif choice == '5':
            delete_dns_records(domain)
        elif choice == '6':
            delete_dns_domain(domain)
        elif choice == 'b':
            return

