#! /usr/bin/env python

from subprocess import call
import sys

args = sys.argv

def docs():
    print "pull    Pull commits from origin/master on all repos"
    print "push    Push unsynced commits to origin/master on all repos"

if len(args) == 1:
    print "I need a command"
    exit(0)

# remove script
args.pop(0)

command = args.pop(0)
repos = [repo for repo in args]

if len(repos) == 0:
    print "I need some repos to " + command