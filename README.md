# modularity-dep-viz
RPM dependency visualisation in Modularity

This script visualizes build and runtime dependnecies of RPM packages. It's a pretty early version developed iteratively (read: hacked, ugly, steaming pile of anti-pattern garbage).

Based on [Harald's script](https://harald.hoyer.xyz/2014/01/14/self-hosting-fedora-base/).

## Usage

1. Generate the deps `python dep-viz.py [--srpm] [--build] [-l INT] PKG [PKG ...] > out.dot`
2. Make it nice `START=7; cat out.dot | sfdp -Gstart=$START -Goverlap=prism | gvmap -e -d $START | neato -Gstart=$START -n -Ecolor=#44444455 -Tsvg > out.svg`
