# modularity-dep-viz
RPM dependency visualisation in Modularity

This script visualizes build and runtime dependnecies of RPM packages. It's a pretty early version developed iteratively (read: hacked, ugly, steaming pile of anti-pattern garbage).

Based on [Harald's script](https://harald.hoyer.xyz/2014/01/14/self-hosting-fedora-base/).

## Usage

```
./dep-viz.py PACKAGE | ./dot_to_svg.sh > out.svg
```

### All parametres

```
usage: dep-viz.py [-h] [--build] [--srpm] [-l MAX_LEVEL] PACKAGE [PACKAGE ...]

Dependency visualizer.

positional arguments:
  PACKAGE               packages to be analyzed

optional arguments:
  -h, --help            show this help message and exit
  --build               resolve build instead of runtime dependencies
  --srpm                visualize source instead of binary packages - only for
                        runtime deps
  -l MAX_LEVEL, --max-level MAX_LEVEL
                        maximum level of recursive dependencies
```

### Examples

#### 1. Get all runtime dependnecies of httpd and nginx

```
./dep-viz.py -l 10 httpd nginx | ./dot_to_svg.sh > example1.svg
```

[see example1.svg](https://github.com/asamalik/modularity-dep-viz/blob/master/example_outputs/example1.svg)

#### 2. The same as previous step, but show only SRPM (source) packages

```
./dep-viz.py -l 10 --srpm httpd nginx | ./dot_to_svg.sh > example2.svg
```

[see example2.svg](https://github.com/asamalik/modularity-dep-viz/blob/master/example_outputs/example2.svg)


#### 3. Get build dependencies of nginx (limit recursion to 1 level)

```
./dep-viz.py -l 1 --build nginx | ./dot_to_svg.sh > example3.svg
```

[see example3.svg](https://github.com/asamalik/modularity-dep-viz/blob/master/example_outputs/example3.svg)

#### 4. Get build dependencies of nginx (limit recursion to 3 levels)

```
./dep-viz.py -l 3 --build nginx | ./dot_to_svg.sh > example4.svg
```

[see example4.svg](https://github.com/asamalik/modularity-dep-viz/blob/master/example_outputs/example4.svg)

