# Onboarding

This file helps onboard new hires into the Jupyter team.

## Basic Information
Our bare-metal cluster consists of one master node named chick0 and 11 children named 
chick1 through chick19 sequentially. It also contains a management node called rooster, which 
acts as a proxy between the Internet and the cluster. The cluster is under a private network, 
so the only way to access the cluster is by SSHing into rooster.

## Getting Started
### Connecting to Rooster
If you have Windows, it would probably be easier to 
install [PuTTY](https://www.chiark.greenend.org.uk/~sgtatham/putty/latest.html).
PuTTY makes it easier for you to SSH into rooster. Otherwise, you can
use the command line.

You need to give your public key to someone who currently has access
to rooster so that you can SSH into the server. 
[Generate your SSH key](https://confluence.atlassian.com/bitbucketserver/creating-ssh-keys-776639788.html)
if you haven't already. If you are using PuTTY, generate your SSH key
using [PuTTYGen](https://www.ssh.com/ssh/putty/windows/puttygen). 

Afterwards, email your public key (should be the file `id_rsa.pub`
or something similar) to someone who has access to rooster. **Do not
email your private key.**

### Joining Our Communication Channels
We use Slack and Zulip to communicate. Make sure that you get invited to
both of these channels.


