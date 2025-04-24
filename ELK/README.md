# ELK 
## Install

Based on https://technisys.atlassian.net/wiki/spaces/TTL/pages/2394528118/ELK+Deployment
    
REPO :  https://bitbucket.org/technisys/digital-monitoring/src/master/

Installing and configuring 

1 - Connect through ssh to the VM and execute the following commands. Those basically will update and install required packages.

sudo yum -y update
sudo yum -y install epel-release
sudo yum -y install ansible
sudo yum -y install git
ansible-galaxy install geerlingguy.java

2 - Once you updated and installed all the packages, now you need to get this repository that has all the Ansible tasks that will be executed soon.


### ANSIBLE Steps


Create inventory config based on template to run ansible on VM, like :

```
cat ELK/inventory.yml 

        [elastic]
        localhost ansible_connection=local 

        [logstash]
        localhost ansible_connection=local

        [kibana]
        localhost ansible_connection=local

        [curator]
        localhost ansible_connection=local
```

Run Ansible local on destination server

```
ansible-playbook --connection=local --inventory inventory.yml  mainElastic.yml

Note: The default users created automatically with the installation process are printed in the standard output (screen). SAVE THE PASSWORDS!!!!

Now you can configure the username and password for Logstash y Kibana, also the IP address of ElasticSearch service. By default, the username and password configuration should be modified in the following template files. To avoid issues, always use “elastic” user and password (generated in the previous step)

ansible/ELK/roles/logstash/templates/logstash.yml
ansible/ELK/roles/kibana/templates/kibana.yml

ansible-playbook --connection=local --inventory inventory.yml  mainLogstash.yml
ansible-playbook --connection=local --inventory inventory.yml  mainKibana.yml
ansible-playbook --connection=local --inventory inventory.yml  mainCurator.yml

```

Install APM SERVER

```
curl -L -O https://artifacts.elastic.co/downloads/apm-server/apm-server-7.17.0-x86_64.rpm
rpm -vi apm-server-7.17.0-x86_64.rpm
```

Editar Elastic Security

Edit this file

```
vim /etc/elasticsearch/elasticsearch.yml
```

Edit/add fields

```
xpack.security.enabled: false
xpack.security.transport.ssl.enabled: false
```

Then restart
```
service elasticsearch restart
```

### Regenerate Elastic password (only if needed ! or if you loose passwords)

```
cd /usr/share/elasticsearch/
bin/elasticsearch-setup-passwords interactive -u "http://localhost:9200"
```

