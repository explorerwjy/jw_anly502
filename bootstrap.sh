#!/bin/bash
#
# bootstrap script for S3 clusters
# Log output to /var/log/bootstrap-actions/
# This script runs as the hadoop user
# It is designed to only run once, but it has protections in case it gets run multiple times

cd /home/hadoop

# Install yum packages we want
sudo yum install -y git emacs

# Configure git
git config --global push.default simple


# Upgrade pip and install mrjob
sudo pip install mrjob                       # install mrjob
sudo easy_install ipython==1.2.1             # grab ipython
sudo pip install --upgrade pip               # moves /usr/bin/pip to /usr/local/bin
sudo ln /usr/local/bin/pip /usr/bin/pip      # hardlink to the old location

# 
if [ ! -e .bashrc-DIST ]; then
   echo Setting up the dot files on AWS user
   echo 
   echo "" >> .bashrc				# Amazon forgot a \n
   echo "" >> .bash_profile                  # Amazon forgot a \n
   mv .bashrc .bashrc-DIST                   # make a copy of the original .bashrc

   # Restore the .bashrc file
   # and append our .bashrc. This is easier than trying to quote things here
   cp -f .bashrc-DIST .bashrc                      # restore distribution
   aws s3 cp s3://gu-anly502/bootstrap-.bashrc - >> .bashrc

   # Add known_hosts for bitbucket and github
   cat >> .ssh/known_hosts << EOF
|1|PdsKoUH6ywpNMq0qWKoAHLGu1xI=|f5NUrP0eZUjiaevZj/jVfFSt03E= ssh-rsa AAAAB3NzaC1yc2EAAAABIwAAAQEAubiN81eDcafrgMeLzaFPsw2kNvEcqTKl/VqLat/MaB33pZy0y3rJZtnqwR2qOOvbwKZYKiEO1O6VqNEBxKvJJelCq0dTXWT5pbO2gDXC6h6QDXCaHo6pOHGPUy+YBaGQRGuSusMEASYiWunYN0vCAI8QaXnWMXNMdFP3jHAJH0eDsoiGnLPBlBp4TNm6rYI74nMzgz3B9IikW4WVK+dc8KZJZWYjAuORU3jc1c/NPskD2ASinf8v3xnfXeukU0sJ5N6m5E8VLjObPEO+mN2t/FZTMZLiFqPWc/ALSqnMnnhwrNi2rbfg/rd/IpL8Le3pSBne8+seeFVBoGqzHM9yXw==
|1|pguo+O/efPRLSe7Py0eQP6ErwK0=|rkOC8nP4kRjQ9eznuu5mmNTepvY= ssh-rsa AAAAB3NzaC1yc2EAAAABIwAAAQEAubiN81eDcafrgMeLzaFPsw2kNvEcqTKl/VqLat/MaB33pZy0y3rJZtnqwR2qOOvbwKZYKiEO1O6VqNEBxKvJJelCq0dTXWT5pbO2gDXC6h6QDXCaHo6pOHGPUy+YBaGQRGuSusMEASYiWunYN0vCAI8QaXnWMXNMdFP3jHAJH0eDsoiGnLPBlBp4TNm6rYI74nMzgz3B9IikW4WVK+dc8KZJZWYjAuORU3jc1c/NPskD2ASinf8v3xnfXeukU0sJ5N6m5E8VLjObPEO+mN2t/FZTMZLiFqPWc/ALSqnMnnhwrNi2rbfg/rd/IpL8Le3pSBne8+seeFVBoGqzHM9yXw==
EOF
fi


# Additions to .mrjob.conf
if [ ! -r .mrjob.conf ]; then
    cat >> /home/hadoop/.mrjob.conf <<EOF
runners:
  emr:
    strict_protocols: true
  hadoop:
    hadoop_bin: /usr/bin/hadoop
    strict_protocols: true
  inline:
    strict_protocols: true
  local:
    strict_protocols: true
EOF
fi

## Install the pig tutorial
if [ ! -d pigtutorial ]; then
  wget --quiet 'https://cwiki.apache.org/confluence/download/attachments/27822259/pigtutorial.tar.gz'
  tar xfvz pigtutorial.tar.gz
  mv pigtmp pigtutorial
  rm pigtutorial.tar.gz
fi



