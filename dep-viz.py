import sys
import subprocess

# this script can figure out build or runtime dependencies of a set of packages
# it also knows what's in base runtime and uses that when possible

# Settings:

# Build or runtime deps? True is build, False runtime
option_build_requires = True

# Number of levels of requires
option_maximum_of_levels = 2



def getBuildRequires(pkgset):
    ret = set()
    cmd = ["repoquery", "--disablerepo=*", "--enablerepo=fedora", "--enablerepo=fedora-source", "--requires", "--srpm", "--source"]
    cmd.extend(pkgset)
    #print cmd
    out = subprocess.check_output(cmd)
    for r in out.split("\n"):
        ret.add(r)
    return ret

def getRequires(pkgset):
    ret = set()
    cmd = ["repoquery", "--disablerepo=*", "--enablerepo=fedora", "--enablerepo=fedora-source", "--requires", "--source"]
    cmd.extend(pkgset)
    #print cmd
    out = subprocess.check_output(cmd)
    for r in out.split("\n"):
        ret.add(r)
    return ret

def getRPMs(requires):
    ret = set()
    cmd = ["repoquery", "--disablerepo=*", "--enablerepo=fedora", "--enablerepo=fedora-source", "--whatprovides"]
    cmd.extend(requires)
    out = subprocess.check_output(cmd)
    for prov in out.split("\n"):
        ret.add("-".join(prov.split("-")[:-2]))
    return ret

def getSRPMs(requires):
    ret = set()
    cmd = ["repoquery", "--disablerepo=*", "--enablerepo=fedora", "--enablerepo=fedora-source", "--whatprovides", "--source"]
    cmd.extend(requires)
    out = subprocess.check_output(cmd)
    for prov in out.split("\n"):
        if prov[-8:] != ".src.rpm":
            continue
        t=prov.rfind("-")
        t=prov.rfind("-", 0, t)
        ret.add(prov[:t])
    return ret

def getBaseRuntimePkgs():
    ret = set()
    f = open('base_runtime_packages.txt', 'r')
    out = f.read()
    for r in out.split("\n"):
        ret.add(r)
    return ret

brt_pkgs = getBaseRuntimePkgs()

oldpkgset = set()
newpkgset = set(getSRPMs(sys.argv[1:]))

ignoreset = set([
])

level = 0
print "strict digraph G {"
print "node [fontname=monospace];"

# Highlighted modules
modules = set()

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

        # Visualise every dependency differently.
        if level is 0:
            print '\t"%s" [color=red,fontcolor=green,fontsize=40];' % i
        elif level is 1:
            print '\t"%s" [fontsize=25];' % i
        elif level is 2:
            print '\t"%s" [fontcolor="#003380",fontsize=20];' % i
        elif level is 3:
            print '\t"%s" [fontcolor="#0055d4",fontsize=16];' % i
        elif level is 4:
            print '\t"%s" [fontcolor="#2a7fff",fontsize=14];' % i

        if len(req):
            for j in req:

                # j is a require of the package

                # Base Runtime module
                if j in brt_pkgs:
                    if "BASE-RUNTIME" not in modules:
                        modules.add("BASE-RUNTIME")
                        print '\t"BASE-RUNTIME" [fontcolor="#666666",fontsize=30];'
                    print '\t"%s" -> "%s";' % (i,"BASE-RUNTIME")
                    newpkgset.discard(j)

                # Perl module
                elif j == "perl" or (j[:5] == "perl-"):
                    if "PERL" not in modules:
                        modules.add("PERL")
                        print '\t"PERL" [fontcolor="#666666",fontsize=30];'
                    print '\t"%s" -> "%s";' % (i,"PERL")
                    newpkgset.discard(j)

                # Python module
                elif j == "python" or j == "python2" or j == "python3" or (j[:7] == "python-") or (j[:8] == "python2-") or (j[:8] == "python3-"):
                    if "PYTHON" not in modules:
                        modules.add("PYTHON")
                        print '\t"PYTHON" [fontcolor="#666666",fontsize=30];'
                    print '\t"%s" -> "%s";' % (i,"PYTHON")
                    newpkgset.discard(j)

                # ignored packages
                elif j in ignoreset:
                    print '\t"%s" [fontcolor=red];' % j
                    print '\t"%s" -> "%s";' % (i,j)
                    newpkgset.discard(j)

                else:
                    print '\t"%s" -> "%s";' % (i,j)

    level+=1
print "}"

for i in newpkgset:
    print >> sys.stderr, i

print >> sys.stderr, "%d Packages" % len(newpkgset)
