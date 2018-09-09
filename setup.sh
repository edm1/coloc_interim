#!/usr/bin/env bash
#

set -euo pipefail

mkdir -p software
cd software

# Install conda
wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh -O miniconda.sh
bash miniconda.sh -b -p $HOME/miniconda
echo export PATH="$HOME/miniconda/bin:\$PATH" >> ~/.profile
. ~/.profile

# Install python and pandas
conda install --yes pandas

# Install GNU parallel
wget http://ftp.gnu.org/gnu/parallel/parallel-20180722.tar.bz2
tar xvjf parallel-20180722.tar.bz2

# Install R
sudo apt-get update
sudo apt-get -y install r-base-core
sudo apt-get -y install libxml2-dev
sudo apt-get -y install libcurl4-openssl-dev
sudo apt-get -y install libssl-dev

# Install coloc - Need to open R and run these commands
# source("https://bioconductor.org/biocLite.R")
# biocLite("snpStats")
# install.packages('coloc')
# install.packages("tidyverse")

# Install LDstore

# Bin
cd ..
mkdir -p bin
cd bin
ln -s ../software/parallel-20180722/src/parallel
echo export PATH="$PWD:\$PATH" >> ~/.profile
. ~/.profile

echo COMPLETE
