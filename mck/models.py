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

    def prune_orphaned_peers(self, instances):
        """
        finds and prunes nodes which exist in k8s but do not exist in tf state.
        """
        conn = Connection(host=self.ipv4, user=self.username)

        # if any existing peers were found which do not match any
        # instance in tf state
        for p in self.peers:
            peer_address = p["address"].removesuffix(":19001")
            if not any(x.ipv4 == peer_address for x in instances):
                print("force removing missing node {}".format(peer_address))
                conn.sudo(
                    "/snap/bin/microk8s remove-node {} --force".format(peer_address)
                )

    def join(self, leader):
        conn = Connection(host=self.ipv4, user=self.username)
        cmd = "/snap/bin/microk8s join {}:25000/{}".format(
            leader.ipv4, leader.join_token()
        )
        conn.sudo(cmd)
