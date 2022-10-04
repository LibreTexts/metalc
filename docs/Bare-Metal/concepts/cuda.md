# CUDA

This document contains notes on CUDA in the context of the bare-metal cluster.

## About

CUDA allows for computing to be done on GPUs. This is most relevant for machine learning applications.

## Installing

On a node with GPU(s), run the following commands to install CUDA:

```
sudo apt-key adv --fetch-keys https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/7fa2af80.pub
sudo add-apt-repository "deb https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/ /"
sudo apt update
sudo apt install cuda
```

Modification may be required for more recent versions.

Additionally, we want to prevent the cuda packages from updating on their own.
To do so, run the following commands:

```
sudo apt-mark hold cuda-drivers-510
sudo apt-mark hold nvidia-driver-510
```

Again, the commands may need to be updated for corresponding package versions.
