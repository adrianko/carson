#! /usr/bin/env python

from subprocess import call
import sys
import os
from os.path import expanduser

"""
TODO Ensure file exists
TODO Create file if not exists
TODO List registered repos
TODO Add repo unregister
TODO Add repo modify
"""
def docs():
    print "pull <repo>, <repo> ...    Pull commits from origin/master on all repos"
    print "push <repo>, <repo> ...    Push unsynced commits to origin/master on all repos"
    print "register <repo> <path>     Register a repo with carson"


args = sys.argv

if len(args) == 1:
    print "I need a command"
    docs()
    exit(0)

# remove script
args.pop(0)

command = args.pop(0)
repos = [repo for repo in args]

if len(repos) == 0:
    print "I need some repos to " + command
    docs()
    exit(0)

current_path = os.path.dirname(os.path.realpath(__file__))
repositories_path = expanduser("~") + "/.carson/repositories"
repositories_file = open(repositories_path, "r")
registered = {}

for r in repositories_file:
    split = r.split("=")
    registered[split[0].strip()] = split[1].strip()

if command == "register":
    if len(repos) == 0:
        print "Need a name and a path"
    elif len(repos) == 1:
        print "Need a path"
    else:
        with open(repositories_path, "a") as register:
            register.write(repos[0].strip() + " = " + repos[1].strip() + "\n")
        print repos[0].strip() + " successfully registered at path " + repos[1].strip()
else:
    for r in repos:
        if r in registered.keys():
            os.chdir(registered[r])
            call(["git", command, "origin", "master"])
            os.chdir(current_path)
        else:
            print r + " is not a registered repo"