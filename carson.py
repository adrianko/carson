#! /usr/bin/env python

import subprocess
import sys
import os
import platform

"""
TODO check for all - commits waiting for push, changes staged and unstaged changes
TODO Ignore push/pull for repos that are already up to date.
TODO Colourise commits ahead or behind statements
"""


def docs():
    print colourise("bold", "Carson - git helper tool")
    print "list                        List all registered repos"
    print "status <repo>, <repo> ...   Show status of all repos"
    print "pull <repo>, <repo> ...     Pull commits from origin/master on all repos"
    print "push <repo>, <repo> ...     Push unsynced commits to origin/master on all repos"
    print "register <repo> <path>      Register a repo"
    print "unregister <repo>           Unregister a repo"
    print "modify <repo> <path>        Modify either the repo name or path"


def git(cur_path, repo, path, command):
    os.chdir(path)
    run = ["git", command]

    if command == "push" or command == "pull": run.extend(("origin", "master"))

    if command == "status":
        result = subprocess.check_output(run)
        if "nothing to commit" in result:
            print colourise("bold", repo) + result.split("\n")[1].replace("Your branch", "")
        elif "Changes to be committed" in result:
            print colourise("bold", repo) + colourise("red", " has changes to be committed")
        elif "Changes not staged" in result:
            print colourise("bold", repo) + colourise("red", " has unstaged changes")
        else:
            print colourise("bold", repo) + " " + result
    else:
        print colourise("bold", repo)
        subprocess.call(run)
        print

    os.chdir(cur_path)


def colourise(colour, string):
    if platform.system() == "Windows": return string
    return "\033[" + {"green": "92", "red": "91", "bold": "1"}[colour] + "m" + string + "\033[0m"


def print_error(string): print colourise("red", "ERROR: ") + string


def print_success(string): print colourise("green", "SUCCESS: ") + string


def rebuild_file(config_file, registered):
    open(config_file, "w").close()

    with open(config_file, "a") as register:
        for r, p in registered.iteritems(): register.write(r + " = " + p + "\n")


config_file = os.path.expanduser("~") + "/.carson"
args = sys.argv

if len(args) >= 2:
    # remove script
    args.pop(0)

    command = args.pop(0)
    repos = [repo.strip() for repo in args]

    if command:
        current_path = os.path.dirname(os.path.realpath(__file__))

        if not os.path.exists(config_file): open(config_file, "a").close()

        repositories_file = open(config_file, "r")
        registered = {}

        for r in repositories_file:
            split = r.split("=")
            registered[split[0].strip()] = split[1].strip()

        if command == "register":
            if len(repos) == 0:
                print_error("Need a name and a path")
            elif len(repos) == 1:
                print_error("Need a path")
            else:
                repo_name, repo_path = repos

                if repo_name not in registered.keys():
                    registered[repo_name] = repo_path
                    rebuild_file(config_file, registered)
                    print_success(repo_name + " registered at path " + repo_path)
                else:
                    print_error(repo_name + " already registered at path " + registered[repo_name])
        elif command == "unregister":
            if len(repos) == 0:
                print_error("Need a name")
            else:
                repo_name = repos[0]

                if repo_name in registered.keys():
                    del registered[repo_name]
                    rebuild_file(config_file, registered)
                    print_success(repo_name + " unregistered")
                else:
                    print_error(repo_name + " is not a registered repo")
        elif command == "list":
            pad_length = max(len(x) for x in registered) + 5

            if len(registered) > 0:
                print colourise("bold", "Repo".ljust(pad_length, " ") + "Path")

                for r, p in registered.iteritems(): print r.ljust(pad_length, " ") + p
            else:
                print "No repos registered"
        elif command == "push" or command == "pull":
            if len(repos) > 0:
                for r in repos:
                    if r in registered.keys():
                        git(current_path, r, registered[r], command)
                    else:
                        print_error(r + " is not a registered repo")
            else:
                for r, p in registered.iteritems(): git(current_path, r, registered[r], command)
        elif command == "status":
            if len(repos) > 0:
                for r in repos:
                    if r in registered.keys():
                        git(current_path, r, registered[r], command)
                    else:
                        print_error(r + " is not a registered repo")
            else:
                for r, p in registered.iteritems(): git(current_path, r, registered[r], command)
        elif command == "modify":
            if len(repos) > 1:
                repo_name, repo_path = repos

                if repo_name in registered.keys() and repo_path in registered.values():
                    print_error("path already exists with same name")
                elif repo_name in registered.keys() or repo_path in registered.values():
                    for r, p in registered.iteritems():
                        if r != repo_name and p == repo_path:
                            del registered[r]
                            break

                    registered[repo_name] = repo_path
                    rebuild_file(config_file, registered)
                    print_success(repo_name + " now at " + repo_path)

                else:
                    print_error("both repo and path do not exist")
            else:
                print_error("need both a repo and a path to modify")
        else:
            docs()
    else:
        docs()
else:
    docs()
