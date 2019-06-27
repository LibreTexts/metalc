# running jhub on ubuntu

- this is assuming you have your ubuntu vm up and running

- 6GB was NOT enough space! so do 10GB
  - nevermind! 10GB was not enough either!

- at the end, it required 15GB

- filenames will be assumed to be from the root of the github repo,
  "https://github.com/ixjlyons/jupyterhub-deploy-teaching.git"

### steps

1. git clone https://github.com/ixjlyons/jupyterhub-deploy-teaching.git

1. make "group_vars/jupyterhub_hosts" file and add your own username using
   the example.

1. make "hosts" file from the example
   - add line "local ansible_ssh_host=127.0.0.1 ansible_ssh_port=22"

1. run `sudo apt-get install ansible`

1. run `git clone https://github.com/UDST/ansible-conda.git`

   - b/c ansible doesnt have the "ansible-conda" module automatically

1. install ssh
   - run "sudo apt-get install ssh"

1. allow ssh to run

   - run `ssh-keygen` (just leave the stuff it asks blank)

   - run `cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys`

   - needed because it usually blocks you from ssh

1. run `sudo aptitude full-upgrade`

   - needed b/c apt safe upgrade module failed

1. run `sudo apt-get install python3-distutils`
  
   - required for [python : conda install ipython and jupyter deps]

     - maybe add this in the playbook

1. install conda! In Celine's and my VMs, this was done by running the
   miniconda shell script in the `/tmp/` directory.

1. but conda still isnt working, so now ansible-conda modules need the
   `executable` parameter

   - find the executable for your conda by running `type conda`
      Note: you may have to run `source ~/.bashrc` for this to work if
      you just installed conda

   - go into "roles/nbgrader/tasks/main.yml" and under the "conda install
     grader" task, add `executable={your conda executable}` to the end of the
     "conda" module line so it will look like:
     ```
    name: conda install nbgrader
    conda: name={{item}} state=present executable=/opt/conda/bin/conda
    become: true ...
     ```

     - had to do this for "roles/python/tasks/jupyter.yml" also
   
1. For some reason, "jupyter contrib nbextensions" wont work so with ansible so run
   `sudo /path/to/your/conda/executable install -c conda-forge jupyter_contrib_nbextensions`

1. step "install cull_idle_servers dependencies" requires pip!
   - run `sudo apt install python-pip`

1. create self-signed ssl certificates to make nginx work

   from [this page](https://www.akadia.com/services/ssh_test_certificate.html)
   run:
   ```
   cd security
   openssl genrsa -out ssl.key 1024
   openssl req -new -key ssl.key -out ssl.csr
   openssl x509 -req -in ssl.csr -signkey ssl.key -out ssl.crt
   ```

1. run `ansible-playbook -l local -u <your_username> --ask-become-pass deploy.yml

   - runs the playbook, deploy.yml, using the host we previously created called
     kevin which just logs in to the localhost at port 22. using "kkrausse"
     (my username) and asking for password. 

### testing

1. run `jupyterhub` on the vm

	- if someone is using port 8000 (i.e. you get error EADDR_IN_USE)
	  find out which process by running `sudo lsof -i :8000` and
	  kill that process

1. setup port forwarding

   - go the VM setting -> Network

   - at this point adapter 1 should be attached to NAT. If not, change it

   - go to advanced setting and click on port forwarding and add a rule and
     set Host Port to 8000 and Guest Port to 8000 also. Leave others blank.

   - save the settings

1. in your browser, navigate to [localhost:8000](localhost:8000)
