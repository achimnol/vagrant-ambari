vagrant-ambari
==============

This project is a set of scripts to deploy Apache Ambari on VirtualBox and Amazon AWS.  These scripts are designed for development and testing only.  For production, you need to change many parts for security, such as use of root accounts to run all daemons!

Some references
---------------

 * [Vagrant](https://github.com/mitchellh/vagrant)
 * [Vagrant-AWS](https://github.com/mitchellh/vagrant-aws)
 * [Apache Ambrai](https://ambari.apache.org/)

VirtualBox Guide
----------------

 - Prepare CentOS 64bit box using `vagrant box add centos6.5-x86_64 https://github.com/2creatives/vagrant-centos/releases/download/v6.5.1/centos65-x86_64-20131205.box`
   You can find other boxes in http://www.vagrantbox.es/ but we currently support CentOS 6 only.
 - Customize `Vagrant` configuration:
   - Change the number of nodes defined as `NUM_NODES`. Be aware that each VM uses 4GB of RAM!
 - Run `vagrant up` and wait for all procedures to complete.
 - Now you can connect to the master node via `http://127.0.0.1:8080` to continue with Ambari setup.  
   It is recommended to modify your `/etc/hosts` (`C:\Windows\System32\drivers\etc\hosts` for Windows) to map `master` with `127.0.0.1` and connect to the Ambari setup by `http://master:8080`.
 - Ambari setup:
   - The default account is admin / admin.
   - Check only the CentOS 6 repository.
   - Type `master`, `node1`, ..., `nodeN` (where N is `NUM_NODES`) in the node list.
   - Choose manual installation of Ambari agents instead of uploading the private key. They are automatically installed during the provisioning process.
   - Use "vagrant" for the user account name.
 - La Voila! Now you have a running Hadoop/Hive/Pig cluster on your desktop (or whatever that VirtualBox is running on).

Amazon AWS Guide
----------------

 - Install cygwin with **OpenSSH** and **rsync** packages.  Ensure that they are available from the command prompt by adding cygwin's bin directory to the `PATH` environment variable.
 - Install vagrant-aws plugin by `vagrant plugin install vagrant-aws`.
 - For KAIST users:
   - Increase the sleep delay from 2 to 11 between SSH connection tests in `run_instance.rb` and `start_instance.rb` at the directory `~/.vagrant.d/gems/gems/vagrant-aws-0.4.1/lib/vagrant-aws/action`.
     Find the corresponding line by searching `sleep`. (There is only one line per file.)
     Otherwise, the university firewall will block your external Internet connection for a few minutes after launching EC2 instances.
 - Prepare a dummy box by `vagrant box add dummy https://github.com/mitchellh/vagrant-aws/raw/master/dummy.box`.
 - Register your AWS access key and secret key to the environment variables named `AWS_ACCESS_KEY` and `AWS_SECRET_KEY`.
   For Linux/Mac users, use `export` command. For Windows users, use `set` command.
 - AWS configurations:
   - Store your private key (`.pem` file) generated from the AWS console in `~/.vagrant.d/`.
   - Configure a security group that allows external SSH (port 22) and HTTP (port 8080) inbound connections.
 - Customize `Vagrant` configuration:
   - Check the region where you provision the instances. The default is `ap-northeast-1` because it has the lowest latency from South Korea. :)
   - Change the security group name. The default is `default`.
   - Change the key filenames and keypair name.
   - Change the number of nodes defined as `NUM_NODES`.
   - If you want, you may change the instance type and AMI. The default instance type is `m1.large`.
     The default AMI image is CentOS 6.4 official release from the AWS marketplace.
 - Run `vagrant up --provider=aws` and wait for all procedures to complete.
 - Now you can connect to the master node via `http://{master's public ip}:8080/` to continue with Ambari setup.
 - Ambari setup:
   - The default account is admin / admin.
   - Check only the CentOS 6 repository.
   - Type FQDN of *internal* host names in the node list, for example: `ip-172-31-xx-xx.ap-northeast-1.compute.internal`.
   - Choose automatic installation via SSH and upload the private key.
   - Use "root" for the user account name.
 - La Voila! Now you have a running Hadoop/Hive/Pig cluster on AWS.

How to use SSH to the master machine
------------------------------------

 - You need to specify the SSH private key depending on your SSH client.
   - For PuTTY, use PuTTYGen to convert OpenSSL private key into PuTTY private key (ppk) without passphrase protection. And then add this key to Pageant.
   - For command line SSH, use `ssh -i {keyfilename} {master's ip}` command.
 - In VirtualbBox, the master's default SSH port is mapped to 2222. node1 is mapped to 2200, node2 to 2201, ..., so on.
 - In Amazon, you can use the plain SSH port 22.

What happens under the hood of `vagrant up`
-------------------------------------------

The Vagrant script automatically configures Hortonworks yum repositories and install ambari-server/agent.  For AWS, installation of ambari-agent is skipped because auto-installation by ambari-server works well without manual touches to the agent configurations (which is written in `ambari_server_init.py`).  To install the ambari-server automatically, it uses a `expect` script named `ambari_server_init.expect`.  The script also tries to disable `iptables` (which is on by default in CentOS AMI and only allows 22 port inbound connections only).  Actual deployments of virtual machines and provisioning is handled by Vagrant.

For VirtualBox, the root `/vagrant` directory is directly synchronized with the current working directory (where `Vagrant` file exists).  For AWS, vagrant uses `rsync` to copy files in the current working directory to `/vagrant` directory of each instance.
