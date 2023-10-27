class Instance:
    def __init__(self, name, provider, ipv4):
        self.name = name
        self.provider = provider
        self.ipv4 = ipv4

        if self.provider == "aws":
            self.username = "admin"
        else:
            self.username = "root"
