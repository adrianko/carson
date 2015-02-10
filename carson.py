#! /usr/bin/env python

from subprocess import call
import sys
import os
from os.path import expanduser

"""
TODO Add repo modify
TODO Suppress output if up to date and display custom message
"""
def docs():
    print "Carson - git helper tool"
    print "list                        List all registered repos"
    print "status <repo>, <repo> ...   Show status of all repos"
    print "pull <repo>, <repo> ...     Pull commits from origin/master on all repos"
    print "push <repo>, <repo> ...     Push unsynced commits to origin/master on all repos"
    print "register <repo> <path>      Register a repo"
    print "unregister <repo>           Unregister a repo"

args = sys.argv

if len(args) >= 2:
    # remove script
    args.pop(0)

    command = args.pop(0)
    repos = [repo for repo in args]

    if command:
        current_path = os.path.dirname(os.path.realpath(__file__))
        repositories_path = expanduser("~") + "/.carson/repositories"

        if not os.path.isdir(expanduser("~") + "/.carson"):
            os.makedirs(expanduser("~") + "/.carson")

        if not os.path.exists(repositories_path):
            open(repositories_path, "a").close()

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
                repo_name = repos[0].strip()
                repo_path = repos[1].strip()

                if repo_name not in registered.keys():
                    with open(repositories_path, "a") as register:
                        register.write(repo_name + " = " + repo_path + "\n")
                    print "SUCCESS: " + repo_name + " registered at path " + repo_path
                else:
                    print "ERROR: " + repo_name + " already registered at path " + registered[repo_name]
        elif command == "unregister":
            if len(repos) == 0:
                print "Need a name"
            else:
                repo_name = repos[0].strip()

                if repo_name in registered.keys():
                    open(repositories_path, "w").close()

                    with open(repositories_path, "a") as register:
                        for r, p in registered.iteritems():
                            if r != repo_name:
                                register.write(r + " = " + p + "\n")
                            else:
                                print "SUCCESS: " + repo_name + " unregistered"
                else:
                    print "ERROR: " + repo_name + " isn't registered"
        elif command == "list":
            pad_length = max(len(x) for x in registered) + 5

            for r, p in registered.iteritems():
                print r.ljust(pad_length, " ") + p
        elif command == "push" or command == "pull":
            if len(repos) > 0:
                for r in repos:
                    if r in registered.keys():
                        os.chdir(registered[r])
                        call(["git", command, "origin", "master"])
                        os.chdir(current_path)
                    else:
                        print r + " is not a registered repo"
            else:
                for r, p in registered.iteritems():
                    os.chdir(registered[r])
                    call(["git", command, "origin", "master"])
                    os.chdir(current_path)
        elif command == "status":
            if len(repos) > 0:
                for r in repos:
                    if r in registered.keys():
                        os.chdir(registered[r])
                        call(["git", command])
                        os.chdir(current_path)
                    else:
                        print r + " is not a registered repo"
            else:
                for r, p in registered.iteritems():
                    os.chdir(registered[r])
                    call(["git", command])
                    os.chdir(current_path)
        else:
            docs()
    else:
        docs()
else:
    docs()