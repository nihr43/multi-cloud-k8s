import yaml
from fabric import Connection


class Instance:
    def __init__(self, name, provider, ipv4):
        self.name = name
        self.provider = provider
        self.ipv4 = ipv4
        self.peers = []

        if self.provider == "aws":
            self.username = "admin"
        else:
            self.username = "root"

    def get_peers(self):
        conn = Connection(host=self.ipv4, user=self.username)
        status = conn.sudo("/snap/bin/microk8s status -w --format yaml", hide=True)
        status_parsed = yaml.safe_load(status.stdout)
        for n in status_parsed["high-availability"]["nodes"]:
            self.peers.append(n)

    def join_token(self):
        conn = Connection(host=self.ipv4, user=self.username)
        jointoken = conn.sudo(
            "/snap/bin/microk8s add-node --format token-check", hide=True
        )
        return jointoken.stdout

    def join(self, initiator):
        conn = Connection(host=self.ipv4, user=self.username)
        cmd = "/snap/bin/microk8s join {}:25000/{}".format(
            initiator.ipv4, initiator.join_token()
        )
        conn.sudo(cmd)
