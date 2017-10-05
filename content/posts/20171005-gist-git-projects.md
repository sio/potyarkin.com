title: Execute the same git subcommand in all local repositories
tags: bash, script, gist
date: 2017-10-05 15:40

If you work with more than one git project simultaneously, you often need to
do the same maintenance tasks in each cloned repository:

- check if there are some changes waiting to be pushed
- check remote URLs for all repos (e.g. when considering to switch from HTTPS
  authentication with GitHub to using SSH keys)
- view last commit messages to refresh your memory

Doing so with standard tools would involve a lot of `cd`-ing, and the
inconvenience would deter you from checking all repos frequently.

That's why I wrote a simple bash script that helps to *automate the boring
stuff*. The script is well-documented, so I won't discuss implementation
details here.


## git-projects.sh
You can download the script from
[https://gist.github.com/sio/...](https://gist.github.com/sio/227da259cad7bb549c69909ba428884c)

The code is licensed under a permissive opensource license (Apache License,
Version 2.0) so feel free to use it for your hobby and work projects.

Report any bugs, ideas, feature requests via GitHub issues/comments -
all feedback is welcome!


## Installation
- Download the script from GitHub, add execution permissions
- List the paths to the local clones of your git repos in a text
  file (one path per line). If you're using relative paths they must
  be valid relative to the location of the script
- Update the value of `PROJECT_LIST` variable with the path of the file
  you've just created


## Usage
All command-line parameters are passed on to the `git` command.
When the script is launched without parameters, `git-projects.sh` checks the
status of each repo.

Repositories are processed in alphabetical order sorted by paths
listed in `PROJECT_LIST`.


## Examples
### Refreshing your memory
```bash
$ ./git-projects.sh log --oneline -3 --no-decorate

HomeLibraryCatalog
b5808f6 Always check the db before showing first run page
72d2481 Remove /quit route
75c707b Clean up destructors for WebUI and CatalogueDB

OpenShiftApp
b260276 Deploy from GitHub
05e0206 Deploy from GitHub
54e5cf1 Deploy from GitHub

server_common
bc33836 Indentation rule for Makefiles
72fb92a Use proper syntax for TODO in GitHub Flavored Markdown
a24e4f2 More familiar Home and Backspace behavior
```

### View latest tag (if any)
```bash
$ ./git-projects.sh describe --tags --always

HomeLibraryCatalog
v0.1.0-71-gb5808f6

OpenShiftApp
b260276

server_common
bc33836
```

### Checking project status
```bash
$ ./git-projects.sh

HomeLibraryCatalog
On branch master
Your branch is up-to-date with 'origin/master'.

nothing to commit, working tree clean

OpenShiftApp
On branch master
Your branch is up-to-date with 'origin/master'.

nothing to commit, working tree clean

server_common
On branch master
Your branch is up-to-date with 'origin/master'.

nothing to commit, working tree clean
```
