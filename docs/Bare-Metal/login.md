# Login
This JupyterHub serves LibreTexts instructors and their students, as well as UC Davis faculty, staff, and students.

## Request an account
If you are a LibreTexts or UC Davis student, please request an account by sending your 
Google OAuth enabled email to <email>. Your email address must have a Google Account 
that can be used with Google OAuth, like `@gmail.com` or `@ucdavis.edu`.

## Getting started with Jupyter
[Jupyter](https://jupyter.org/index.html) is an environment where you can
create interactive notebooks with code, visualizations, and more. 

Some resources to learn Jupyter:
* [jupyter.org/try](https://jupyter.org/try) has interactive demo notebooks in
many different languages
* [Demo video of Jupyter](https://www.youtube.com/watch?v=DLWBfR2hxoo&list=PLUrHeD2K9CmnCOjrnHzSIbZbZmDE-lQRt)
of how to navigate the Jupyter Notebook.
* Visit the 
[JupyterLab documentation](https://jupyterlab.readthedocs.io/en/latest/user/interface.html)
for more information on navigating the interface.

## Setting up custom conda environments
Please visit [here](https://github.com/LibreTexts/default-env#creating-your-own-custom-conda-environment)
for information on creating custom conda environments.

## Setting up custom environments for a class
If you are a teacher who wants to set up an environment with custom packages and kernels,
please create one of the following and email it to <email>:
1. One or more configuration files supported by [repo2docker](https://repo2docker.readthedocs.io) that list your desired packages. Supported configuration files are listed
  [here](https://repo2docker.readthedocs.io/en/latest/config_files.html).
1. A [Dockerfile](https://docs.docker.com/engine/reference/builder/). We recommend using or building
on top of a [Jupyter Docker Stack](https://jupyter-docker-stacks.readthedocs.io/en/latest/index.html)
that is already available to the community.

For an example of packages that could be included, please look at the 
[Jupyter Core Stacks](https://jupyter-docker-stacks.readthedocs.io/en/latest/using/selecting.html#core-stacks).

## I have an issue!
Please [open an issue](https://github.com/LibreTexts/tech-Issues/issues/new) on GitHub. You will need to 
create a GitHub account if you do not have one.

## Contact
If you have an technical issue, please first open one [here](https://github.com/LibreTexts/tech-Issues/issues) on GitHub.
For other issues, please contact <email>.
