import dns.tsigkeyring
import dns.update
import dns.query
import dns.zone
import dns.rdataclass
import dns.rdatatype

class NameServer:
    def __init__(self, server_address, server_keyname, server_key, domain):
        """
        To initialize the object:
            server_address: address of the bind server where we are allowed to
            remote update
            server_keyname: the name of the update key
            server_key: the actual update key
            domain: the root domain we are going to add/remove/query records
            from
        """
        keyring = dns.tsigkeyring.from_text({server_keyname : server_key})
        self.update = dns.update.Update(domain, keyring=keyring)
        self.server_address = server_address
        self.domain = domain

    def add_host(self, name, ip):
        """
        Given a name and a ip address it creates the A record
        """
        rdataa = dns.rdata.from_text(dns.rdataclass.IN,dns.rdatatype.A,str(ip))
        rdataseta = dns.rdataset.from_rdata(300,rdataa)
        self.update.add(name,rdataseta)
        return dns.query.tcp(self.update,self.server_address)

    def add_cname(self, alias_name, name):
        """
        Given an alias name and a name (A record) it creates the CNAME record
        """
        rdataa = dns.rdata.from_text(dns.rdataclass.IN,dns.rdatatype.CNAME,str(name))
        rdataseta = dns.rdataset.from_rdata(300,rdataa)
        self.update.add(alias_name,rdataseta)
        return dns.query.tcp(self.update,self.server_address)

    def del_host(self, name):
        """
        It deletes the record pointed by name
        """
        self.update.delete(name)
        return dns.query.tcp(self.update,self.server_address)

    def query_host(self, name):
        """
        Simple host query, boolean return
        """
        z = dns.zone.from_xfr(dns.query.xfr(self.server_address, self.domain))
        try:
            z.find_node(name)
            return True
        except KeyError:
            return False
