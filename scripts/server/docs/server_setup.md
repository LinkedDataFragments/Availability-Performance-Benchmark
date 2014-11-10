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

### Network
* Put the machine in the same subnet as the clients. In AWS, this can be accomplished by using a Virtual Private Cloud (VPC).
* Open at least ports 22 (SSH), 4444 (telnet used by monitor) open for incoming traffic within the subnet.
* Open at least port 8890 (standard Virtuoso sparql endpoint), ... (Fuseki sparql endpoint), ... open for outgoing traffic within the subnet.

### Software
* Ubuntu 13.10 (Server edition)
* ssh (client and server)
* s3cmd (if in AWS infrastructure): communication with S3 store
* Java >= 1.7.0 update 51
* nodejs >= 0.10.15
* Virtuoso >= 7.1 (we compiled it from source)
* Tomcat 7
* Fuseki

2) Preparing the server (after every (re)boot on AWS)
-----------------------------------------------------
This section assumes you use our server image on AWS.

Scripts for preparing the server are found in the <code>scripts</code> directory. So <code>cd</code> to <code>scripts/</code>. Each script contains some comments that explain what is going on.

### Mounting the drives
	./1_prepareAndMountDrives.sh

This mounts the two instance ssd drives to <code>/mnt/drive1</code> and <code>/mnt/drive2</code>, and formats them. You can check with <code>df -h</code>, and this should give something like:

	Filesystem      Size  Used Avail Use% Mounted on
	/dev/xvda1      7.8G  2.8G  4.7G  37% /
	none            4.0K     0  4.0K   0% /sys/fs/cgroup
	udev            3.7G  8.0K  3.7G   1% /dev
	tmpfs           752M  196K  752M   1% /run
	none            5.0M     0  5.0M   0% /run/lock
	none            3.7G     0  3.7G   0% /run/shm
	none            100M     0  100M   0% /run/user
	/dev/xvdb        40G   50M   39G   1% /mnt/drive1
	/dev/xvdc        40G   50M   39G   1% /mnt/drive2

Note the last two lines are the freshly mounted drives.

### Preparing Virtuoso database files

If you plan to run Virtuoso with our pre-loaded database, run:

	./2_prepareVirtuosoFiles.sh

This script gets the compressed database files (<code>virtuoso_drive1.tar.xz</code> and <code>virtuoso_drive2.tar.xz</code>) from S3 storage and unpacks them in <code>/mnt/drive1/virtuoso</code> and <code>/mnt/drive2/virtuoso</code> respectively. This can take a few minutes since each file is about 15 GB. Also, do this before starting the Virtuoso server (of course).

### Preparing Fuseki TDB database files

If you plan to run Fuseki with our pre-loaded TDB database, run:

	./3_prepareFusekiFiles_<dataset>.sh

This script gets the compressed database files (<code>fuseki-bsbm.tar.xz</code> or <code>fuseki-sp2b.tar.xz</code>) from S3 storage and unpacks them in <code>/mnt/drive2/dataset/bsbm/100M/fuseki-bsbm</code> or <code>/mnt/drive1/dataset/sp2b/100M/fuseki-sp2b</code> respectively. Do this before starting Fuseki (of course).

### Preparing HDT files

If you plan to run Fuseki or an LDF server with our HDT files, run:

	./4_prepareHDTFiles_<dataset>.sh

3) Virtuoso setup, config & run
-------------------------------

We compiled OpenLink Virtuoso Open-Source edition from source, from the development branch. The release version 7.1.0 didn't compile at the time of testing. We followed [these instructions](http://virtuoso.openlinksw.com/dataspace/doc/dav/wiki/Main/VOSUbuntuNotes#Building%20Virtuoso%20from%20Source).

We did the same for Virtuoso 6.

### Build tweaks

We chose to build Virtuoso in the home directory of the regular user (in this case 'ubuntu'). This allows virtuoso to run as a regular user. LDAP support and imsg support were disabled and no VAD's were installed. We enabled POSIX threads. This resulted in the following commands:

	./configure --prefix=/home/ubuntu/progs/virtuoso-opensource-bin --disable-all-vads --with-pthreads --disable-openldap --disable-imsg
	make -j5
	make install

This results the Virtuoso package (binaries, libraries, config) being install into the <code>/home/ubuntu/progs/virtuoso-opensource-bin</code> directory.

### Virtuoso server tweaks

The Virtuoso server configuration is kept in a file <code>virtuoso.ini</code>. In our setup, this file can be found in <code>~/progs/virtuoso-opensource-bin/var/lib/virtuoso/db/virtuoso.ini</code>. We list the changes we made to this file, but don't copy it just like that; read the documentation!

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
	MaxQueryMem                     = 2G
	
	;; System with 7 GB free
	NumberOfBuffers                 = 595000
	MaxDirtyBuffers                 = 455000
	
	[Striping]
	Segment1                        = 30g, /mnt/drive1/virtuoso/db-seg1.db, /mnt/drive2/virtuoso/db-seg1.db

Note that, since striping is used, the DatabaseFile parameter doesn't matter.

### Running the server
If you use our AWS server image, just <code>cd</code> to the <code>~/progs/virtuoso-opensource-bin/bin/</code> and run

	./startVirtuoso.sh

This starts Virtuoso as foreground process. In fact, it does this:

	/home/ubuntu/progs/virtuoso-opensource-bin/bin/virtuoso-t -f -c /home/ubuntu/progs/virtuoso-opensource-bin/var/lib/virtuoso/db/virtuoso.ini

And creates a SPARQL endpoint at:

	http://<host>:8890/sparql


4) Fuseki with TDB backend setup, config & run
----------------------------------------------

This describes the (standard) Fuseki-Jena-TDB setup, which can be downloaded at the Apache Jena Releases [download page](http://jena.apache.org/download/index.cgi) as jena-fuseki-&lt;version&gt;-distribution.tar.gz.
We used Fuseki 1.0.1. Everything works pretty well out of the box. We just created scripts to start the server with the right parameters.

### Running the server
To run the server, <code>cd</code> to <code>~/progs/jena-fuseki-1.0.1</code>, and run

	./fuseki-server-<dataset>.sh

This starts Fuseki as a foreground process. In fact, it does this:

	./fuseki-server --loc=/mnt/drive2/dataset/bsbm/100M/fuseki-bsbm /bsbm

And starts a SPARQL endpoint at

	http://<host>:3030/<dataset>/sparql


4) Fuseki with HDT backend setup, config & run
----------------------------------------------

Fuseki Also works with [HDT](http://www.rdfhdt.org) as backend. We followed [these instructions](http://www.rdfhdt.org/manual-of-hdt-integration-with-jena/).
It comes down to setting the right jars on the classpath, and referring to HDT files in the configuration.

### Configuration

Here are the modified lines in config.ttl:

	[] rdf:type fuseki:Server ;
		ja:context [ ja:cxtName "arq:queryTimeout" ;  ja:cxtValue "60000,180000" ] ;
		ja:loadClass "org.rdfhdt.hdtjena.HDTGraphAssembler" ;
		fuseki:services (
			<#service1>
		) .

	<#service1> rdf:type fuseki:Service ;
		# SPARQL query services e.g. http://host:port/ds/sparql?query=...
		fuseki:serviceQuery             "sparql" ;
		fuseki:name                     "ds" ;
		fuseki:serviceQuery             "query" ;
		fuseki:serviceReadGraphStore    "get" ;
		fuseki:dataset                   <#dataset> .

	<#dataset> rdf:type ja:RDFDataset ;
		rdfs:label "ds" ;
		ja:defaultGraph <#graph1> .

	<#graph1> rdfs:label "RDF Graph1 from HDT file" ;
		rdf:type hdt:HDTGraph ;
		hdt:fileName "/mnt/drive1/hdt/dataset.hdt" .

### Running the server
To run the server, <code>cd</code> to <code>~/progs/jena-fuseki-1.0.1</code>, and run

	./fuseki-server-hdt.sh

This starts Fuseki as a foreground process. In fact, it does this:

	./fuseki-server --config=config.ttl

And creates a SPARQL endpoint at

	http://<host>:3030/ds/sparql

Switching data sets is done by putting the corresponding HDT file in the directory <code>/mnt/drive1/hdt/</code>.
