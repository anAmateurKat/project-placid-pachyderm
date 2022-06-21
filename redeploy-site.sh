#!/bin/bash

#This script redeploys my portfolio site after any changes have been made to the site
#on the GitHub repo. It automates all the manual steps previously taken to do so

tmux kill-server
cd /root/project-placid-pachyderm
git fetch
git reset origin/main --hard

source python3-virtualenv/bin/activate
pip install -r requirements.txt
tmux new -ds flask-placidportfolio 'flask run --host=0.0.0.0;'