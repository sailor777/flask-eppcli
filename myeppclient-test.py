from eppy.client import EppClient
from eppy.doc import (  EppInfoDomainCommand,EppInfoContactCommand,
                        EppCreateDomainCommand,EppCreateContactCommand)

class MyEpp(EppClient):

    def domain_info(self, domainname, log_send_recv=False):
        cmd = EppInfoDomainCommand()
        cmd.name = domainname
        print(cmd)
        return self.send(cmd, log_send_recv=log_send_recv)

    def contact_info(self, contactname, log_send_recv=False):
        cmd = EppInfoContactCommand()
        cmd.id = contactname
        print(cmd)
        return self.send(cmd, log_send_recv=log_send_recv)

    def domain_create(self, domainname, contactname, *ns, log_send_recv=False):
        cmd = EppCreateDomainCommand()
        cmd.name = domainname
        cmd.ns = {'hostObj': [*ns]}
        cmd.registrant = contactname
        print(cmd)
        return self.send(cmd, log_send_recv=log_send_recv)

    def contact_create(self, contactname=None, log_send_recv=False):
        cmd = EppInfoContactCommand()
        cmd.id = contactname
        print(cmd)
        return self.send(cmd, log_send_recv=log_send_recv)

if __name__ == '__main__':
    my_epp = MyEpp(ssl_keyfile='client.key', ssl_certfile='client.pem',
                   ssl_validate_hostname=False, ssl_validate_cert=False)
    my_epp.connect('epp-test-server.domainname')
    my_epp.read()
    resp = my_epp.login('LOGIN','PASS')
    my_epp.hello()
    #resp = my_epp.domain_info('testdomain.epp.ua')
    #resp1 = my_epp.contact_info('yfdle9412')
    resp = my_epp.domain_create('testdomain-1.epp.ua', 'contactname',
                                'ns1.epp.ua', 'ns2.epp.ua')
    print(resp)
    #print(resp1)
    #print(dir(resp))
    my_epp.logout()
