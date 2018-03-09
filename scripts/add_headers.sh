#!/bin/bash

# Excpeted:
# 'c.hdr' with C header
# 'py.hdr' with Python header

# C
hdr="$( cat c.hdr )"
echo "${hdr}"
for f in `find ./ -type f -name '*.[c|h]'`
do
	echo "Writing header to '${f}'"
	#sed -i "1i${hdr}" "${f}"
	echo "${hdr}" | cat - ${f} > /tmp/.hs && mv /tmp/.hs ${f}
done

# python
hdr="$( cat py.hdr )"
echo "${hdr}"
for f in `find ./ -type f -name '*.py'`
do
	echo "Writing header to '${f}'"
	echo "${hdr}" | cat - ${f} > /tmp/.hs && mv /tmp/.hs ${f}
done
