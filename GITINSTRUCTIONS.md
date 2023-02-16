## Basic git usage
- You should not push anything directly to main branch. Main branch is only used for storing the working and tested version of the code.
- Commits to main are created by making pull requests to main from feature branches.
- Squash the branch to minimal amount of commits. Each independent change or developement should have its own commit, but all commits regarding one feature should be squashed.

## Useful git commands
### Create a branch and check out to it
```bash
git checkout -b <branch name>
```
### Push the branch to remote
```bash
git push <remote name> <branch name>
```
Usually the remote is called origin
```bash 
git push origin <branch name>
```

### Put a file to the staging area
```bash
git add <filename>
```

### Revert changes of a file
