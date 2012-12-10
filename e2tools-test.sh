#!/bin/sh
# Simple test for est e2tools <URL:http://home.earthlink.net/~k_sheff/sw/e2tools/>
# Copyright (C) 2006 Hans Ulrich Niedermann
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA

set -ex

# Caution: An image of 100G size needs 1.6GB on disk just to be formatted!
for imgsize in 1M; do
    testimg="test-${imgsize}.img"
    trap "" EXIT
    # create sparse image file full of zeros
    rm -f "${testimg}"
    /bin/dd if=/dev/null of="${testimg}" bs=1 count=1 seek="$imgsize"
    # create file system on image file
    /sbin/mkfs.ext2 -F "${testimg}"
    # check a few things
    ./e2mkdir "${testimg}:/foo"
    ./e2ls -l "${testimg}:"

    ./e2mkdir "${testimg}:/bar"
    ./e2mkdir "${testimg}:/bla"
    ./e2ls -l "${testimg}:"

    for file in README configure; do

	./e2cp "${file}" "${testimg}:/foo"
	./e2ls -l "${testimg}:/foo"

	trap "rm -f ${file}.test-c" EXIT
	./e2cp "${testimg}:/foo/${file}" "${file}.test-c"

	./e2rm ${testimg}:/foo/${file}
	./e2ls -l "${testimg}:/foo"

	cmp ${file} ${file}.test-c
	rm -f ${file}.test-c
    done

    # remove the test image
    rm -f "${testimg}"
    trap "" EXIT
done

exit 0
