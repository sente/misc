#!/bin/sh

dir=$1

find $dir -type f -name "*.zip" -printf "%TY-%Tm-%Td\t%h/%f\n" | sort | while read line; do
   echo "unzip -d $line"; done
