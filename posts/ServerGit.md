Server

Specialized computer or software system designed to manage, store, and process data for other computers or devices, often referred to as clients.

A server is any device or program that provides services to other devices (clients) over a network, ranging from hosting websites and files to running applications and databases. It plays a crucial role in modern computing, supporting communication and resource-sharing across the internet and local networks.

![Servergit image 1](posts/assets/ServerGit/image-1.jpeg)

1. Types of Servers

Web Server: Hosts websites and serves web pages to users' browsers (e.g., Apache, Nginx).

File Server: Stores files and manages access to them on a network (e.g., Windows File Server/ Samba Server).

Database Server: Hosts a database and allows clients to query and manage data (e.g., MySQL, SQL Server).

Mail Server: Manages sending, receiving, and storing emails.

Application Server: Runs specific applications or services for clients (e.g., handling business logic in a web app).

Game Server: Hosts online multiplayer games, allowing players to connect and play together.

DNS Server: Resolves domain names to IP addresses so that browsers can connect to websites (e.g., Google's Public DNS, Root DNS ).

2. Functions of a Server

Provide services: A server might serve files, process web requests, or manage data.

Share resources: Servers allow multiple users or devices to share access to things like files, printers, or databases.

Manage connections: Servers handle the connections and requests made by client machines.

Security and Access Control: Servers often implement authentication, authorization, and encryption to secure the resources they provide.

3. Hardware vs. Software

Hardware: The physical machine running the server software, typically more powerful and optimized for constant uptime and reliability.

Software: The server-side application or operating system running on the server machine (e.g., Linux, Windows Server).

4. How Servers Work

When a client (a user’s computer, smartphone, or application) makes a request (e.g., to view a website), the server processes the request and sends back the appropriate response (e.g., the HTML content of a webpage).

Servers are designed to handle multiple requests at once, often from thousands of clients simultaneously.

5. Server Locations

On-premises servers: Physical servers located in an organization's data center or office.

Cloud servers: Virtualized servers hosted by cloud service providers like AWS, Google Cloud, or Microsoft Azure.

Allowing for greater scalability and flexibility.

6. Server Management

Servers typically require management for uptime, security, performance, backups, and other operational concerns.

As We Learn Basic Detail of Server,

Now it's Time to Hand's On Server Configure. We Learn Server Configuration on Linux Server.

We Should know Linux have various distribution, Ubuntu, Unix, Redhat, Centos and many more.

Here We are going to use Redhat Server Edition.

First Download Redhat ISO or Centos ISO from Official Website,

Now We have Server ISO, Virtualbox

Let's Configure and Start Understand Feature also.

![Servergit image 2](posts/assets/ServerGit/image-2.png)

Now Start Very First Step of Configuration...

Follow me Step by Step......

Yum Server Configuration

YUM (Yellowdog Updater, Modified) server, which is used in Red Hat-based Linux distributions (such as CentOS, Fedora, and RHEL) to manage package installations and updates.

Set up or configure a YUM server:

![Servergit image 3](posts/assets/ServerGit/image-3.png)

Login and enter password

Now this we can connect external ISO file so we can copy Package and Configure server.

![Servergit image 4](posts/assets/ServerGit/image-4.png)

use command::

df -Th (show Disk File and path of mount iso file)

![Servergit image 5](posts/assets/ServerGit/image-5.png)

yum clean all   (cmd to clean all disk space)

#cd /etc/yum.repo.d/

(clean all file pre-exit)

$rm -rf *

$vi /ftp.repo (create file)

we can config as per need.

Now copy package folder from iso drive to var folder

![Servergit image 6](posts/assets/ServerGit/image-6.png)

$df -Th  show disk file and path

$cp /* /var/ftp/pub/repo/

$cd /Packages

$rpm -ivh vsftpd*

$yum clean all

$yum repolist all

Now You Successfully Configure Yum server,

More info [link](https://www.blogger.com/)

yum search, yum info, yum history, yum grouplist.

FTP Server Configure:

![Servergit image 7](posts/assets/ServerGit/image-7.png)

$yum -ivh vsftpd*

$systemctl start vsftpd

$systemctl enable vsftpd

$systemctl status vsftpd

Note: To make more secure we can use Selinux, but some organization disable it.

FTP main configuration file is

/etc/vsftpd/vsftpd.conf ---- here you find original file.

NOTE: don't forget make backup of original file while you going to make changes, it's help to troubleshoot, if misconfiguration done.

cp /etc/vsftpd.conf  /etc/vsftpd.conf.orig

![Servergit image 8](posts/assets/ServerGit/image-8.png)

cp cmd use for copy data from one to other location.

mv cmd also use for move data from one to other location or rename any file also.

Now do some main configuration,

only installation of package/demeon not allow you to use service like as we do in Windows.

Now configure and allow service from firewall i.e  on server level

firewall-cmd : use this to allow services.

![Servergit image 9](posts/assets/ServerGit/image-9.png)

firewall-cmd --list-all    [it show all service which allow from firewall]

port 21 /tcp for ftp server.

add --permanent --public by firewalld

Read man firewalld

This is only we allow ftp server from firewall, now  we have also check or configure Network also by nmcli cmd

so, we can communicate within safe and wanted Network.

Let's Learn about Nmcli

First go and read man page that's help us alot, to understand demeon / package.

man nmcli

Nmcli help us to configure System / Server / Laptop to connect with required network

![Servergit image 10](posts/assets/ServerGit/image-10.png)

$nmcli c mod enp0s3 ipv4.addresses "192.168.1.108/24"

$nmcli c mod enp0s3 ipv4.dns "8.8.8.8"

$nmcli c mod enp0s3 ipv4.method manual

$nmcli c down enp0s3

$nmcli c up enp0s3

Now your network also configure.

![Servergit image 11](posts/assets/ServerGit/image-11.png)

By ifconfig we can check ip status

______________________________________________________________________________________________

Mail server: Now have a look on mail server that is important day to day life.

Then we also try to understand Mail  server attack, C-Panel and other tools.

Note: For mail server Packages we need are

Postfix, Dovecot, imap, bind, smtp

Postfix: a hugely-popular Mail Transfer Agent (MTA) designed to determine routes and send emails. This cross-platform server is open-source.

Dovecot: primary purpose is to act as a mail storage server. The mail is delivered to the server using some mail delivery agent and is stored for later access with an email client.  Dovecot can also act as mail [proxy server](https://www.blogger.com/), forwarding connection to another mail server, or act as a lightweight MUA in order to retrieve and manipulate mail on remote server for e.g. mail migration.
