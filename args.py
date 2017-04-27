import argparse

parser = argparse.ArgumentParser(description='Dependency visualizer.')
parser.add_argument('--build', action="store_true", help='resolve build instead of runtime dependencies')
parser.add_argument('-l', '--max-level', type=int, default=1, help='maximum level of recursive dependencies')
parser.add_argument('packages', metavar='PACKAGE', type=str, nargs='+', help='packages to be analyzed')
args = parser.parse_args()

print args
