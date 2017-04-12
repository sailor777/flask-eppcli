from eppy.client import EppClient
from eppy.doc import (  EppCheckDomainCommand,EppCheckContactCommand,
                        EppInfoDomainCommand,EppInfoContactCommand,
                        EppCreateDomainCommand,EppCreateContactCommand,
                        EppRenewDomainCommand)

class MyEpp(EppClient):

    def domain_check(self, domain, log_send_recv=True):
        cmd = EppCheckDomainCommand()
        cmd.name = domain
        print(cmd)
        return self.send(cmd, log_send_recv=log_send_recv)

    def contact_check(self, contact_id, log_send_recv=True):
        cmd = EppCheckContactCommand()
        cmd.id = contact_id
        print(cmd)
        return self.send(cmd, log_send_recv=log_send_recv)

    def domain_info(self, domain, log_send_recv=False):
        cmd = EppInfoDomainCommand()
        cmd.name = domain
        print(cmd)
        return self.send(cmd, log_send_recv=log_send_recv)

    def contact_info(self, contact_id, log_send_recv=False):
        cmd = EppInfoContactCommand()
        cmd.id = contact_id
        print(cmd)
        return self.send(cmd, log_send_recv=log_send_recv)

    def domain_create(self, domain, contact_id, *ns, log_send_recv=False):
        cmd = EppCreateDomainCommand()
        cmd.name = domain
        cmd.ns = {'hostObj': [*ns]}
        cmd.registrant = contact_id
        print(cmd)
        return self.send(cmd, log_send_recv=log_send_recv)

    def contact_create( self,person,org,street,email,phone,id=None,
                        city='Lviv',pc='79000',cc='UA',log_send_recv=False):
        cmd = EppCreateContactCommand()
        cmd.postalInfo = {  '@type': 'int', 'name': person,'org': org, 'addr': \
                            {'street': street,'city': city, 'pc': pc, 'cc': cc}}
        cmd.voice = phone
        cmd.email = email
        cmd.id = id
        cmd.authInfo = {'pw': 'kajvwevjwovj239t0gjv0i3h'}
        print(cmd)
        return self.send(cmd, log_send_recv=log_send_recv)

    def domain_renew(self, domain, curExpDate, period, log_send_recv=True):
        cmd = EppRenewDomainCommand()
        cmd.name = domain
        cmd.curExpDate = curExpDate
        cmd.period = {'@unit': 'y', '_text': period}
        print(cmd)
        return self.send(cmd, log_send_recv=log_send_recv)
