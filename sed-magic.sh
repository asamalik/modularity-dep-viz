#!/bin/sh

grep "^[+*]" brt-pkgs.txt | sed 's/^.\t\(.*\)-[^-]*-[^-]*$/\1/'
