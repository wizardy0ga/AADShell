#!/usr/bin/sh

# Installer file is intended to ensure that only root / sudo users and processes
# can interact with the program and its source code. This is to ensure that the
# secrets within the store remain protected at the cost of convenience to the user.


# Set root user as owner of source code, data store and tools
chown root ../src
chown root ../store
chown root ../tools
chown root ../aadshell.py

# Set rwx perms for root, --- for everyone else
chmod 700 -R ../src
chmod 700 -R ../store
chmod 700 -R ../tools
chmod 700 ../aadshell.py

echo "Installation successful"