#! /usr/bin/env python

from subprocess import call
import sys
import os

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

def git(cur_path, path, command):
    os.chdir(path)
    run = ["git", command]

    if command == "push" or command == "pull":
        run.extend(("origin", "master"))

    call(run)
    os.chdir(cur_path)

config_dir = os.path.expanduser("~") + "/.carson"
config_file = config_dir + "/repositories"
args = sys.argv

if len(args) >= 2:
    # remove script
    args.pop(0)

    command = args.pop(0)
    repos = [repo for repo in args]

    if command:
        current_path = os.path.dirname(os.path.realpath(__file__))

        if not os.path.isdir(config_dir):
            os.makedirs(config_dir)

        if not os.path.exists(config_file):
            open(config_file, "a").close()

        repositories_file = open(config_file, "r")
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
                    with open(config_file, "a") as register:
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
                    open(config_file, "w").close()

                    with open(config_file, "a") as register:
                        for r, p in registered.iteritems():
                            if r != repo_name:
                                register.write(r + " = " + p + "\n")
                            else:
                                print "SUCCESS: " + repo_name + " unregistered"
                else:
                    print "ERROR: " + repo_name + " isn't registered"
        elif command == "list":
            pad_length = max(len(x) for x in registered) + 5

            if len(registered) > 0:
                print "Repo".ljust(pad_length, " ") + "Path"

                for r, p in registered.iteritems():
                    print r.ljust(pad_length, " ") + p
            else:
                print "No repos registered"
        elif command == "push" or command == "pull":
            if len(repos) > 0:
                for r in repos:
                    if r in registered.keys():
                        git(current_path, registered[r], command)
                    else:
                        print r + " is not a registered repo"
            else:
                for r, p in registered.iteritems():
                    git(current_path, registered[r], command)
        elif command == "status":
            if len(repos) > 0:
                for r in repos:
                    if r in registered.keys():
                        git(current_path, registered[r], command)
                    else:
                        print r + " is not a registered repo"
            else:
                for r, p in registered.iteritems():
                    git(current_path, registered[r], command)
        else:
            docs()
    else:
        docs()
else:
    docs()