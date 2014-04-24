Server setup for LDF evaluation
===============================

This setup describes how to set up the server for LDF evaluation. We use Amazon AWS infrastructure for this purpose, but it should work on any hardware setup that meets te requirements.

1) Prerequisites
----------------

###Minimum (virtual) hardware
* **important:** 2 HD's of *at least* 30 GB each. Our setup uses striping over 2 disks for Virtuoso. In AWS, this is instance storage (2 SSD drives).
* 4 CPU cores
* 8 GB RAM
* Decent network connection

###network
* Have the machine in the same subnet as the clients. In AWS, this can be accomplished by using a Virtual Private Cloud (VPC).
* Open at least ports 22 (SSH), 4444 (telnet used by monitor) open for incoming traffic within the subnet.
* Open at least port 8890 (standard Virtuoso sparql endpoint), ... (Fuseki sparql endpoint), ... open for outgoing traffic within the subnet.

###software
* Ubuntu 13.10 (server)
* s3cmd (if in AWS infrastructure): communication with S3 store
* Java >= 1.7.0 update 51
* nodejs >= 0.10.15
* Virtuoso >= 7.1 (we compiled it from source)
* Tomcat
* Fuseki
