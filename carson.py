#! /usr/bin/env python

from subprocess import call
import sys
import os

args = sys.argv

def docs():
    print "pull <repo>, <repo> ...    Pull commits from origin/master on all repos"
    print "push <repo>, <repo> ...    Push unsynced commits to origin/master on all repos"

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

registered = open(os.path.dirname(os.path.realpath(__file__)) + "/repositories", "r")

for r in repos:
    pass