# Basic For OSI Model

OSI Model are divide into two part mainly:

1) Network

2) Server

Let have some flash light on Network

In simple way we all know Network, major component RJ45 cable connector, LAN cable Cat5, Cat5e, Cat6....many more option also.

![Newtwork_Doc_Git image 1](posts/assets/Newtwork_doc_git/image-1.jpeg)

Next focus on Topology we use, while configuration Point topology.Star topology.Bus topology.Ring topology.Mesh topology.Hybrid topology.Daisy chain topologyNext focus on Topology we use, while configuration Point topology.Star topology.Bus topology.Ring topology.Mesh topology.Hybrid topology.Daisy chain topology

![Newtwork_Doc_Git image 2](posts/assets/Newtwork_doc_git/image-2.jpeg)

Next Level

Data Layer

Where we learn about:

The Address Resolution Protocol (ARP) operates on both Layer 2 and Layer 3,

Layer 2: The data link layer, where MAC addresses are located.

Layer 3: The network layer, where IP addresses are located

Here's how ARP works:

1) When a device wants to send data to another device on the same network, it knows the IP address of the destination but not the MAC address.

2) The device broadcasts an ARP request to all devices on the local subnet asking for the MAC address associated with the IP address.

3) The device that matches the IP address responds with its MAC address.

4) The device updates its ARP table with the new MAC address so it knows how to reach the other device.

ARP caches resolved addresses for a short period of time to reduce the number of address resolution requests. The cache is periodically flushed to remove unused entries and free up space.

![Newtwork_Doc_Git image 3](posts/assets/Newtwork_doc_git/image-3.gif)

ICMP packet for ping cmd

Now put some light on Network Configuration.

There are many Device and option for Network Configuration with different rule, policies, packet filtering.

For Configuration, Most of organization use Different type of Router which also act as firewall (Router + Firewall) device are:

Sophos, Fortinet, Juniper and many more provide software and Hardware, BUT some organization use in-house configuration, this is done with help of VYOS ISO file available to configure step by step.

Which we learn soon....

![Newtwork_Doc_Git image 4](posts/assets/Newtwork_doc_git/image-4.png)

Let's Download VYOS ISO File

Vyos is an open-source network operating system that is based on Linux and used primarily for routing, firewalling, and VPN functionality.

You can download it from the official VyOS website.   [https://vyos.io/](https://www.blogger.com/).

Navigate to the "Downloads" section, typically under the "Get VyOS" or "Download VyOS" menu.

Keep in mind download lts version always.

Installation

Once you have the ISO file, you can:

Create a bootable USB drive: Using tools like Rufus (on Windows) or dd (on Linux/Mac).

Install on Virtual Machines: Like VMware or VirtualBox. (For Local practice)

Deploy on Physical Hardware: If you have a dedicated server or device.

We are install / Configure VYOS on VirtualBox:

Installation step are available on official website.

Default user and password are vyos, but we can reset password while installation.

![Newtwork_Doc_Git image 5](posts/assets/Newtwork_doc_git/image-5.png)

                   

![Newtwork_Doc_Git image 6](posts/assets/Newtwork_doc_git/image-6.png)

As we can see eth0 eth3 there are 4 NIC port which are not configure yet but we going to configure.

We configure all port as per real IT world Realm.

Note: Before move to configuration part let have some basic review required protocol

DHCP: Dynamic Host Configuration Protocol

The most common types of information a DHCP server can provide:

1. IP address
2. Subnet mask
3. Domain name
4. Default gateway (routers)
5. DNS server address

DHCP is connectionless, which means it uses UDP at the Transport layer, also known as the Host-to-Host layer.

They are four-step process establish Server - Client handshake.

DNS: Domain Name Service (DNS) resolves hostnames—specifically, Internet names.

DNS address and send a UDP request to your DNS server to resolve the name.

If your first DNS server doesn’t know the answer to the query, then the DNS server forwards a TCP request to its root DNS server.

ARP: Address Resolution Protocol (ARP) finds the hardware address of a host from a known IP address.

ARP broadcast—notice that the destination hardware address.

Subnet: Creating subnetworks is essentially the act of taking bits from the host portion of the address and reserving them to define the subnet address instead.

In this first section, we’ll be discussing classful routing, which refers to the fact that all hosts
The network are using the exact same subnet mask. Later, when we move on to cover variable length subnet masks (VLSMs).

-----------------------------------------------------------------------------------------------------------------------------------------------------------

1) Below image give us very basic and normal scenario.

Two ISP and have firewall configure with load balance for any office.

![Newtwork_Doc_Git image 7](posts/assets/Newtwork_doc_git/image-7.png)

![Newtwork_Doc_Git image 8](posts/assets/Newtwork_doc_git/image-8.png)

As we see above ISP is providing 1.1.1.1/30 IP Address.

Now let start  configure local basic Network.

First we install vyos iso file in virtualbox.

Default login : vyos password : vyos

but while installing we can change password as we want.

![Newtwork_Doc_Git image 9](posts/assets/Newtwork_doc_git/image-9.png)

As we see port are not configure:

Note: Commit (Enter)

Save (Enter)

use for save changes.

![Newtwork_Doc_Git image 10](posts/assets/Newtwork_doc_git/image-10.png)

Interface Configuration:

$ set interfaces ethernet eth0 address dhcp
 $set interfaces ethernet eth0 description 'OUTSIDE'
 $set interfaces ethernet eth1 address '192.168.1.1/24'
 $set interfaces ethernet eth1 description 'INSIDE'

DHCP Configure:

$set service dhcp-server shared-network-name LAN subnet "192.168.1.0/24" default-router "192.168.1.1"

$set service dhcp-server shared-network-name LAN subnet "192.168.1.0/24" name-server "192.168.1.1"

$set service dhcp-server shared-network-name LAN subnet "192.168.1.0/24" domain-name "ABC.Department"

$set service dhcp-server shared-network-name LAN subnet "192.168.1.0/24" lease '86400'

$set service dhcp-server shared-network-name LAN subnet "192.168.1.0/24" range start "192.168.1.10"  stop "192.168.1.20"

![Newtwork_Doc_Git image 11](posts/assets/Newtwork_doc_git/image-11.png)

Let's Configure DNS [Domain Name Service]

$set service dns forwarding cache-size '0'

$set service dns forwarding listen-address "192.168.1.1"

$set service dns forwarding allow-from "192.168.1.0/24"

NAT Configure:[ network address translation]

$set nat source rule 100 outbound-interface 'eth0'

$set nat source rule 100 source address '192.168.1.0/24'

$set nat source rule 100 translation address masquerade

Now We configured DHCP/DNS/NAT, but without firewall we can't filter packet from OutSide & InSide.

To understand we allow ssh to communicate.

$set service ssh port '22'

Firewall Policy Or packet allow:

$set firewall name OUTSIDE-IN default-action 'drop'

$set firewall name OUTSIDE-IN rule 10 action 'accept'

$set firewall name OUTSIDE-IN rule 10 state established 'enable'

$set firewall name OUTSIDE-IN rule 10 state related 'enable'

$set firewall name OUTSIDE-LOCAL default-action 'drop'

$set firewall name OutSide-Local rule 10 action 'accept'

$set firewall name OutSide-Local rule 10 state established 'enable'

$set firewall name OutSide-Local rule 10 state related 'enable'

$set firewall name OutSide-Local rule 20 action 'accept'

$set firewall name OutSide-Local rule 20 icmp type-name 'echo-request'

$set firewall name OutSide-Local rule 20 protocol 'icmp'

$set firewall name OutSide-Local rule 20 state new 'enable'

$set firewall name OutSide-Local rule 30 action 'drop'

$set firewall name OutSide-Local rule 30 destination port '22'
$set firewall name OutSide-Local rule 30 protocol 'tcp'
$set firewall name OutSide-Local rule 30 recent count '4'
$set firewall name OutSide-Local rule 30 recent time 'minute'
$set firewall name OutSide-Local rule 30 state new 'enable'

$set firewall name OutSide-Local rule 31 action 'accept'
$set firewall name OutSide-Local rule 31 destination port '22'
$set firewall name OutSide-Local rule 31 protocol 'tcp'
$set firewall name OutSide-Local rule 31 state new 'enable'

### Let's Understand about TLS ( Transport Layer Security ) ###

A primary use case of TLS is encrypting the communication between web applications and servers, such as web browsers loading a website. TLS can also be used to encrypt other communications such as email, messaging, and [voice over I](https://www.blogger.com/)P.
