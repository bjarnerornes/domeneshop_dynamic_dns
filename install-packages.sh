#!/bin/bash

set -euo pipefail

export DEBIAN_FRONTEND=noninteractive

# Update package list
apt-get update

# Upgrade packages
apt-get upgrade -y

# Install required packages
apt-get install -y hello

# Clean up package cache
apt-get clean 
rm -rf /var/lib/apt/lists/*
