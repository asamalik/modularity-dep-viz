#!/usr/bin/python2

import sys
import subprocess
import argparse
import yaml

# this script can figure out build or runtime dependencies of a set of packages
# it also knows what's in base runtime and uses that when possible




parser = argparse.ArgumentParser(description='Dependency visualizer.')
parser.add_argument('--build', action="store_true", help='resolve build instead of runtime dependencies')
parser.add_argument('--srpm', action="store_true", help='visualize source instead of binary packages - only for runtime deps')
parser.add_argument('--ignored-relations-file', type=str, default="", help='a YAML file describing which dependencies should be ignored')
parser.add_argument('-l', '--max-level', type=int, default=1, help='maximum level of recursive dependencies')
parser.add_argument('packages', metavar='PACKAGE', type=str, nargs='+', help='packages to be analyzed')
args = parser.parse_args()

# Build or runtime deps? True is build, False runtime
option_build_requires = args.build

# Runtime deps output binary RPMs. Set to True to output source SRPMSs.
# The script will run much longer.
option_just_sources = args.srpm

# Number of levels of requires
option_maximum_of_levels = args.max_level

# you can specify package dependencies you want to ignore
ignored_relations = {}
if args.ignored_relations_file:
    try:
        rel_file = open(args.ignored_relations_file,'r')
        ignored_relations = yaml.load(rel_file)["ignored_relations"]
    except:
        print >> sys.stderr, "ERROR: Can't read the 'ignored-deps-file'."
    

# build deps are srpms anyway, so let's not waste time...
if option_build_requires:
    option_just_sources = False

fedora_repo = "http://ftp.fi.muni.cz/pub/linux/fedora/linux/development/26/Everything/x86_64/os/"
fedora_source_repo = "http://ftp.fi.muni.cz/pub/linux/fedora/linux/development/26/Everything/source/tree/"

binary_repo_str = '--repofrompath=f26,{}'.format(fedora_repo)
source_repo_str = '--repofrompath=f26-source,{}'.format(fedora_source_repo)

def getBuildRequires(pkgset):
    ret = set()
    cmd = ["repoquery", "--disablerepo=*", binary_repo_str, source_repo_str, "--enablerepo=f26", "--enablerepo=f26-source", "--requires", "--srpm", "--source"]
    cmd.extend(pkgset)
    #print cmd
    out = subprocess.check_output(cmd)
    for r in out.split("\n"):
        ret.add(r)
    return ret

def getRequires(pkgset):
    ret = set()
    cmd = ["repoquery", "--disablerepo=*", binary_repo_str, source_repo_str, "--enablerepo=f26", "--enablerepo=f26-source", "--requires", "--source"]
    cmd.extend(pkgset)
    #print cmd
    out = subprocess.check_output(cmd)
    for r in out.split("\n"):
        ret.add(r)
    return ret

def getRPMs(requires):
    ret = set()
    cmd = ["repoquery", "--disablerepo=*", binary_repo_str, source_repo_str, "--enablerepo=f26", "--enablerepo=f26-source", "--whatprovides"]
    cmd.extend(requires)
    out = subprocess.check_output(cmd)
    for prov in out.split("\n"):
        ret.add("-".join(prov.split("-")[:-2]))
    return ret

def getSRPMs(requires):
    ret = set()
    cmd = ["repoquery", "--disablerepo=*", binary_repo_str, source_repo_str, "--enablerepo=f26", "--enablerepo=f26-source", "--whatprovides", "--source"]
    cmd.extend(requires)
    out = subprocess.check_output(cmd)
    for prov in out.split("\n"):
        if prov[-8:] != ".src.rpm":
            continue
        t=prov.rfind("-")
        t=prov.rfind("-", 0, t)
        ret.add(prov[:t])
    return ret

def getSRPM(package):
    cmd = ["repoquery", "--disablerepo=*", binary_repo_str, source_repo_str, "--enablerepo=f26", "--enablerepo=f26-source", "--whatprovides", "--source", package]
    out = subprocess.check_output(cmd)

    prov =  out.split("\n")[0]
    name = "-".join(prov.split("-")[:-2])
    return name

def getBaseRuntimePkgs():
    ret = set()
    f = open('base_runtime_packages.txt', 'r')
    out = f.read()
    for r in out.split("\n"):
        ret.add(r)
    return ret

brt_pkgs = getBaseRuntimePkgs()

oldpkgset = set()
newpkgset = set(getSRPMs(args.packages))

ignoreset = set([
    "generic-release",
    "fedora-release",
    "fedora-repos",
])

level = 0
print "strict digraph G {"
print "node [fontname=monospace];"

# Highlighted modules
modules = set()

# highlighted packages - just to make sure they are not highlighted twice
# which was happening when 1st lvl dep was also a 3rd lvl dep, so the pkg got highlighted as 3rd lvl
highlighted_pkgs = set()


# highlight input distinctively
for pkg in newpkgset:
    print '\t"%s" [color=red,fontcolor=green,fontsize=40];' % pkg
    highlighted_pkgs.add(pkg)

while (len(newpkgset - oldpkgset) > 0) and (level < option_maximum_of_levels):
    diff = newpkgset - oldpkgset
    oldpkgset = set(newpkgset)
    newpkgset = newpkgset | diff

    for i in list(diff):
        if option_build_requires:
            req = getSRPMs(getBuildRequires([i]))
        else:
            req = getRPMs(getRequires([i]))
        newpkgset = newpkgset | req


        # i is package

        # show just source packages?
        if option_just_sources:
            i_print = getSRPM(i)
        else:
            i_print = i

        if len(req):
            for j in req:

                # j is a require of the package

                # show just source packages?
                if option_just_sources:
                    j_print = getSRPM(j)
                else:
                    j_print = j


                if i_print in ignored_relations and j_print in ignored_relations[i_print]:
                    newpkgset.discard(j)
                    print >> sys.stderr, 'Ignored "%s" -> "%s"' % (i_print, j_print)
                    continue
                

                # Base Runtime module
                if j in brt_pkgs:
                    j_print = "BASE-RUNTIME"
                    if "BASE-RUNTIME" not in modules:
                        modules.add("BASE-RUNTIME")
                        print '\t"BASE-RUNTIME" [fontcolor="#666666",fontsize=30];'
                    newpkgset.discard(j)

                # Perl module
                elif j == "perl" or (j[:5] == "perl-"):
                    j_print = "PERL"
                    if "PERL" not in modules:
                        modules.add("PERL")
                        print '\t"PERL" [fontcolor="#666666",fontsize=30];'
                    newpkgset.discard(j)

                # Python module
                #elif j == "python" or j == "python2" or j == "python3" or (j[:7] == "python-") or (j[:8] == "python2-") or (j[:8] == "python3-"):
                #    j_print = "PYTHON"
                #    if "PYTHON" not in modules:
                #        modules.add("PYTHON")
                #        print '\t"PYTHON" [fontcolor="#666666",fontsize=30];'
                #    newpkgset.discard(j)

                # ignored packages
                elif j in ignoreset:
                    print '\t"%s" [fontcolor=red];' % j_print
                    newpkgset.discard(j)


                # Visualise every dependency differently.
                if j_print not in highlighted_pkgs and j_print not in modules:
                    highlighted_pkgs.add(j_print)
                    if level is 0:
                        print '\t"%s" [fontsize=25];' % j_print
                    elif level is 1:
                        print '\t"%s" [fontcolor="#003380",fontsize=20];' % j_print
                    elif level is 2:
                        print '\t"%s" [fontcolor="#0055d4",fontsize=16];' % j_print
                    elif level is 3:
                        print '\t"%s" [fontcolor="#2a7fff",fontsize=14];' % j_print

                # visualize relation
                print '\t"%s" -> "%s";' % (i_print, j_print)

    level+=1
print "}"

for i in highlighted_pkgs:
    print >> sys.stderr, i

print >> sys.stderr, "%d Packages" % len(highlighted_pkgs)

