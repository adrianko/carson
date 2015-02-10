#! /usr/bin/env python

from subprocess import call
import sys
import os

"""
TODO Suppress output if up to date and display custom message
"""
def docs():
    print cPrint("bold", "Carson - git helper tool")
    print "list                        List all registered repos"
    print "status <repo>, <repo> ...   Show status of all repos"
    print "pull <repo>, <repo> ...     Pull commits from origin/master on all repos"
    print "push <repo>, <repo> ...     Push unsynced commits to origin/master on all repos"
    print "register <repo> <path>      Register a repo"
    print "unregister <repo>           Unregister a repo"
    print "modify <repo> <path>        Modify either the repo name or path"

def git(cur_path, path, command):
    os.chdir(path)
    run = ["git", command]

    if command == "push" or command == "pull": run.extend(("origin", "master"))

    call(run)
    os.chdir(cur_path)

def cPrint(colour, string): return "\033[" + {"green": "92", "red": "91", "bold": "1"}[colour] + "m" + string + "\033[0m"

def printError(string): print cPrint("red", "ERROR: ") + string

def printSuccess(string): print cPrint("green", "SUCCESS: ") + string

config_dir = os.path.expanduser("~") + "/.carson"
config_file = config_dir + "/repositories"
args = sys.argv

if len(args) >= 2:
    # remove script
    args.pop(0)

    command = args.pop(0)
    repos = [repo.strip() for repo in args]

    if command:
        current_path = os.path.dirname(os.path.realpath(__file__))

        if not os.path.isdir(config_dir): os.makedirs(config_dir)
        if not os.path.exists(config_file): open(config_file, "a").close()

        repositories_file = open(config_file, "r")
        registered = {}

        for r in repositories_file:
            split = r.split("=")
            registered[split[0].strip()] = split[1].strip()

        if command == "register":
            if len(repos) == 0: printError("Need a name and a path")
            elif len(repos) == 1: printError("Need a path")
            else:
                repo_name, repo_path = repos

                if repo_name not in registered.keys():
                    with open(config_file, "a") as register:
                        register.write(repo_name + " = " + repo_path + "\n")
                    printSuccess(repo_name + " registered at path " + repo_path)
                else: printError(repo_name + " already registered at path " + registered[repo_name])
        elif command == "unregister":
            if len(repos) == 0: printError("Need a name")
            else:
                repo_name = repos[0]

                if repo_name in registered.keys():
                    open(config_file, "w").close()

                    with open(config_file, "a") as register:
                        for r, p in registered.iteritems():
                            if r != repo_name: register.write(r + " = " + p + "\n")
                            else: printSuccess(repo_name + " unregistered")
                else: printError(repo_name + " is not a registered repo")
        elif command == "list":
            pad_length = max(len(x) for x in registered) + 5

            if len(registered) > 0:
                print cPrint("bold", "Repo".ljust(pad_length, " ") + "Path")

                for r, p in registered.iteritems(): print r.ljust(pad_length, " ") + p
            else: print "No repos registered"
        elif command == "push" or command == "pull":
            if len(repos) > 0:
                for r in repos:
                    if r in registered.keys(): git(current_path, registered[r], command)
                    else: printError(r + " is not a registered repo")
            else:
                for r, p in registered.iteritems(): git(current_path, registered[r], command)
        elif command == "status":
            if len(repos) > 0:
                for r in repos:
                    if r in registered.keys(): git(current_path, registered[r], command)
                    else: printError(r + " is not a registered repo")
            else:
                for r, p in registered.iteritems(): git(current_path, registered[r], command)
        elif command == "modify":
            if len(repos) > 1:
                repo_name, repo_path = repos

                if repo_name in registered.keys() and repo_path in registered.values():
                    printError("path already exists with same name")
                elif repo_name in registered.keys() or repo_path in registered.values():
                    for r, p in registered.iteritems():
                        if r != repo_name and p == repo_path:
                            del registered[r]
                            break
                    
                    registered[repo_name] = repo_path
                    open(config_file, "w").close()

                    with open(config_file, "a") as register:
                        for r, p in registered.iteritems(): register.write(r + " = " + p + "\n")

                    printSuccess(repo_name + " now at " + repo_path)

                else: printError("both repo and path do not exist")
            else: printError("need both a repo and a path to modify")
        else: docs()
    else: docs()
else: docs()