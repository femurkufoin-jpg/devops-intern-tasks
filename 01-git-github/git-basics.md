Git and GitHub Fundamentals
Introduction
Git is a distributed version control system used to track changes in files and collaborate on software development projects.
GitHub is a cloud-based platform that hosts Git repositories and supports collaboration between developers.
Important Git Concepts
Repository: A location where project files and their history are stored.
Commit: A saved snapshot of changes.
Branch: An independent line of development.
Merge: Combining changes from different branches.
Remote: A repository hosted on another server, such as GitHub.
Pull Request: A request to review and merge proposed changes.
Common Git Commands
Command
Purpose
git init
Initialize a repository
git status
Check repository status
git add
Stage changes
git commit
Save changes
git branch
List branches
git switch
Switch branches
git push
Upload commits
git pull
Retrieve and integrate changes
git log
View commit history
Practical Progress
Initialized a local Git repository.
Created the main branch.
Created README.md.
Staged and committed the README.
Created the feature/git-fundamentals branch.
Git Merge Conflict Practice
Objective
To understand how Git merge conflicts occur and how to identify and resolve them.
Practical Activities
Created a feature branch named feature/merge-conflict-practice.
Modified the README file on the feature branch.
Switched to the main branch and introduced a different change to the same file.
Attempted to merge the feature branch into main.
Git reported a content conflict in README.md.
Inspected the conflicting changes.
Resolved the conflict by reviewing and retaining the required content.
Staged the resolved file using git add README.md.
Completed the merge using a Git commit.
Pushed the changes to GitHub.
Commands Practised
git switch -c feature/merge-conflict-practice
git add README.md
git commit -m "docs: add feature branch change"
git switch main
git add README.md
git commit -m "docs: update merge conflict section on main"
git merge feature/merge-conflict-practice
git status
git add README.md
git commit -m "docs: resolve README merge conflict"
git push origin main
Result
Successfully created and resolved a Git merge conflict. Verified that the main branch was synchronized with GitHub and the working tree was clean.
Learning Outcome
Gained practical experience with Git branching, merging, conflict identification, conflict resolution, and version control collaboration.
