resource "digitalocean_droplet" "instance" {
  image    = "debian-12-x64"
  name     = "mck-k8s-do-${count.index}"
  region   = "nyc1"
  size     = "s-1vcpu-2gb"
  ssh_keys = [digitalocean_ssh_key.default.fingerprint]
  count    = 1
}

resource "linode_instance" "instance" {
  image           = "linode/debian12"
  label           = "mck-k8s-linode-${count.index}"
  region          = "us-ord"
  type            = "g6-standard-1"
  authorized_keys = [linode_sshkey.default.ssh_key]
  count           = 1
}

data "aws_ami" "ubuntu" {
  most_recent = true

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-focal-20.04-amd64-server-*"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }

  owners = ["099720109477"] # Canonical
}

resource "aws_instance" "instance" {
  ami                    = data.aws_ami.ubuntu.id
  instance_type          = "t1.micro"
  key_name               = "opentofu"
  vpc_security_group_ids = [aws_default_security_group.default.id]
  count = 1
  tags = {
    Name = "mck-k8s-aws-${count.index}"
  }
}

resource "aws_default_subnet" "default_az1" {
  availability_zone = "us-west-2a"
}

resource "aws_default_vpc" "mainvpc" {
}

resource "aws_default_security_group" "default" {
  vpc_id = aws_default_vpc.mainvpc.id

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
}
