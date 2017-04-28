#!/bin/sh

mkdir modularity
./dep-viz.py -l 10 mariadb mongodb python2 python3 docker nodejs proftpd nginx chronyd postgresql haproxy httpd varnish postfix memcached ruby | ./dot_to_svg.sh > modularity/all-runtime-binary.svg
./dep-viz.py -l 10 --srpm mariadb mongodb python2 python3 docker nodejs proftpd nginx chronyd postgresql haproxy httpd varnish postfix memcached ruby | ./dot_to_svg.sh > modularity/all-runtime-source.svg
./dep-viz.py -l 1 --build mariadb mongodb python2 python3 docker nodejs proftpd nginx chronyd postgresql haproxy httpd varnish postfix memcached ruby | ./dot_to_svg.sh > modularity/all-build-lvl-1.svg
./dep-viz.py -l 2 --build mariadb mongodb python2 python3 docker nodejs proftpd nginx chronyd postgresql haproxy httpd varnish postfix memcached ruby | ./dot_to_svg.sh > modularity/all-build-lvl-2.svg
./dep-viz.py -l 3 --build mariadb mongodb python2 python3 docker nodejs proftpd nginx chronyd postgresql haproxy httpd varnish postfix memcached ruby | ./dot_to_svg.sh > modularity/all-build-lvl-3.svg
./dep-viz.py -l 4 --build mariadb mongodb python2 python3 docker nodejs proftpd nginx chronyd postgresql haproxy httpd varnish postfix memcached ruby | ./dot_to_svg.sh > modularity/all-build-lvl-4.svg
./dep-viz.py -l 5 --build mariadb mongodb python2 python3 docker nodejs proftpd nginx chronyd postgresql haproxy httpd varnish postfix memcached ruby | ./dot_to_svg.sh > modularity/all-build-lvl-5.svg
./dep-viz.py -l 6 --build mariadb mongodb python2 python3 docker nodejs proftpd nginx chronyd postgresql haproxy httpd varnish postfix memcached ruby | ./dot_to_svg.sh > modularity/all-build-lvl-6.svg
./dep-viz.py -l 7 --build mariadb mongodb python2 python3 docker nodejs proftpd nginx chronyd postgresql haproxy httpd varnish postfix memcached ruby | ./dot_to_svg.sh > modularity/all-build-lvl-7.svg
./dep-viz.py -l 8 --build mariadb mongodb python2 python3 docker nodejs proftpd nginx chronyd postgresql haproxy httpd varnish postfix memcached ruby | ./dot_to_svg.sh > modularity/all-build-lvl-8.svg
