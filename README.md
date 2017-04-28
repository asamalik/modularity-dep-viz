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
usage: dep-viz.py [-h] [--build] [--srpm]
                  [--ignored-relations-file IGNORED_RELATIONS_FILE]
                  [-l MAX_LEVEL]
                  PACKAGE [PACKAGE ...]

Dependency visualizer.

positional arguments:
  PACKAGE               packages to be analyzed

optional arguments:
  -h, --help            show this help message and exit
  --build               resolve build instead of runtime dependencies
  --srpm                visualize source instead of binary packages - only for
                        runtime deps
  --ignored-relations-file IGNORED_RELATIONS_FILE
                        a YAML file describing which dependencies should be
                        ignored
  -l MAX_LEVEL, --max-level MAX_LEVEL
                        maximum level of recursive dependencies
```

### Ignoring dependencies

You will probably use this tool to optimize dependencies. If you plan to remove a dependency, you can visualize that change already using the `--ignored-relations-file FILENAME` option. The file has the following syntax:

```
---
ignored_relations:
  package_one:
  - removed_dependency_1
  - removed_dependency_3
  another_package:
  - another_removed_dep
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

#### 5. Remove unwanted dependency

The previous example shows that `nginx` build-requires `gd`. If you want to see what happens when you remove that dependency, create a file `ignored-relations.yaml` with the following content:

```
---
ignored_relations:
  nginx:
  - gd
```

... and use the `--ignored-relations-file FILENAME` option:

```
./dep-viz.py -l 3 --build --ignored-relations-file ./ignored_relations.yaml nginx | ./dot_to_svg.sh > example5.svg
```

[see example5.svg](https://github.com/asamalik/modularity-dep-viz/blob/master/example_outputs/example5.svg)

Yay! You would need only 36 packages instead of 61.
