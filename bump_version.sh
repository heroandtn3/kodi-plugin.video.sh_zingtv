#!/usr/bin/sh

if [ -z "$1" ]; then
    echo $(grep "VERSION=" Makefile)
    echo usuage: $0 version_number
    exit
fi

version=$1

# Makefile
sed -i -r "s/VERSION=.*?/VERSION=$version/" Makefile

# addon.xml
sed -i -r "s/(<addon .*? version=)\".*?\"/\1\"$version\"/" addon.xml

exit 0
