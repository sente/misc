find . -type f -printf "%TY-%Tm-%Td\t%h/%f\n" | while read line; do unzip -d $line; done
