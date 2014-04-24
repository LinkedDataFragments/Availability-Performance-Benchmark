Server setup for LDF evaluation
===============================

This setup describes how to set up the server for LDF evaluation. We use Amazon AWS infrastructure for this purpose, but it should work on any hardware setup that meets te requirements.

1) Prerequisites
----------------

### Minimum (virtual) hardware
* **important:** 2 HD's of *at least* 30 GB each. Our setup uses striping over 2 disks for Virtuoso. In AWS, this is instance storage (2 SSD drives).
* 4 CPU cores
* 8 GB RAM
* Decent network connection

### network
* Put the machine in the same subnet as the clients. In AWS, this can be accomplished by using a Virtual Private Cloud (VPC).
* Open at least ports 22 (SSH), 4444 (telnet used by monitor) open for incoming traffic within the subnet.
* Open at least port 8890 (standard Virtuoso sparql endpoint), ... (Fuseki sparql endpoint), ... open for outgoing traffic within the subnet.

### software
* Ubuntu 13.10 (Server edition)
* ssh (client and server)
* s3cmd (if in AWS infrastructure): communication with S3 store
* Java >= 1.7.0 update 51
* nodejs >= 0.10.15
* Virtuoso >= 7.1 (we compiled it from source)
* Tomcat
* Fuseki

2) Virtuoso setup, config & run
-------------------------------

We compiled OpenLink Virtuoso Open-Source edition from source, from the development branch. The release version 7.1.0 didn't compile at the time of testing. We followed [these instructions](http://virtuoso.openlinksw.com/dataspace/doc/dav/wiki/Main/VOSUbuntuNotes#Building%20Virtuoso%20from%20Source).

### Build tweaks

We chose to build Virtuoso in the home directory of the regular user (in this case 'ubuntu'). This allows virtuoso to run as a regular user. LDAP support and imsg support were disabled and no VAD's were installed. We enabled POSIX threads. This resulted in the following commands:

	./configure --prefix=/home/ubuntu/progs/virtuoso-opensource-bin --disable-all-vads --with-pthreads --disable-openldap --disable-imsg
	make -j5
	make install

This results the Virtuoso package (binaries, libraries, config) being install into the <pre>/home/ubuntu/progs/virtuoso-opensource-bin</pre> directory.

### Virtuoso server tweaks

The Virtuoso server configuration is kept in a file <pre>virtuoso.ini</pre>. In our setup, this file can be found in <pre>~/progs/virtuoso-opensource-bin/var/lib/virtuoso/db/virtuoso.ini</pre>. We list the changes we made to this file, but don't copy it just like that; read the documentation!

	;
	;  Database setup
	;
	[Database]
	DatabaseFile                    = /mnt/drive1/virtuoso/virtuoso.db
	ErrorLogFile                    = /mnt/drive1/virtuoso/virtuoso.log
	LockFile                        = /mnt/drive1/virtuoso/virtuoso.lck
	TransactionFile                 = /mnt/drive1/virtuoso/virtuoso.trx
	xa_persistent_file              = /mnt/drive2/virtuoso/virtuoso.pxa
	Striping                        = 1
	
	[TempDatabase]
	DatabaseFile                    = /mnt/drive2/virtuoso/virtuoso-temp.db
	TransactionFile                 = /mnt/drive2/virtuoso/virtuoso-temp.trx
	
	;
	;  Server parameters
	;
	[Parameters]
	DirsAllowed                     = ., /home/ubuntu/progs/virtuoso-opensource-bin/share/virtuoso/vad, /mnt/drive1/dataset/bsbm/100M, /mnt/drive1/dataset/sp2b/100M
	ThreadThreshold                 = 100
	MaxQueryMem                     = 4G
	
	;; System with 28 GB free
	NumberOfBuffers                 = 2380000
	MaxDirtyBuffers                 = 1820000
	
	[Striping]
	Segment1                        = 30g, /mnt/drive1/virtuoso/db-seg1.db, /mnt/drive2/virtuoso/db-seg1.db

Note that, since striping is used, the DatabaseFile parameter doesn't matter.

### Running the server

This command is an example on how to start the server. <pre>virtuoso-t -h</pre> gives all options.

	/home/ubuntu/progs/virtuoso-opensource-bin/bin/virtuoso-t -f -c /home/ubuntu/progs/virtuoso-opensource-bin/var/lib/virtuoso/db/virtuoso.ini

