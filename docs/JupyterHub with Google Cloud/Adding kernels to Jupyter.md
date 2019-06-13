# Introduction

This document aims to teach how to install additional kernels in JupyterHub. A kernel, in this
context, is a program that runs and introspects the user’s code. JupyterHub uses kernels to run
and support different programming languages. This guide was tested on a deployment of ‘The
littlest JupyterHub’ running on Ubuntu 18 inside of a VirtualBox.
#### Note: ​I had to manually grant write permission to users to install using conda.

## R Kernel
1. Login to JupyterHub as an admin user, and run a terminal.
2. Run the command: 
>sudo -E conda install r
3. After the installation is done, run r with the command: R
4. Install needed R packages with:
>install.packages(c(​'repr'​, ​'IRdisplay'​, ​'IRkernel'​), type = ​'source'​)
5. Make the R kernel available to all JupyterHub users:
>IRkernel::installspec(user = ​FALSE​)
6. Installation is done, R notebooks should now be supported.

## Python2 Kernel

1. Login to JupyterHub as an admin user, and run a terminal.
2. Create a conda environment for Python2, run the command:
>​conda create ​-​n ipykernel_py2 python​=​ 2 ​ ipykernel
3. Activate the new environment:
>source activate ipykernel_py
4. Add the kernel to JupyterHub:
>python ​-​m ipykernel install ​--​user

## Octave Kernel
1. Login to JupyterHub as an admin user, and run a terminal.
2. Install Octave with conda:
>sudo conda install octave 

- If the above doesn't work, run: 
>conda install octave
  
3. Install the Octave Kernel with conda:
> conda config --add channels conda-forge <br>
 conda install octave_kernel
 
4. Installation should be done, Octave notebooks should now be supported.
