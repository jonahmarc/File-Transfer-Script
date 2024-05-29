# File Transfer Script
> Python script that runs every 24 hours since the script started. It automatically transfers files modified in less than 24 hours from source to destination. This script does not transfer hidden files.

## Pre-requisites
1. Python
2. virtual environment using pyenv (recommended)
3. python virtual environment

## Setup
1. Install python job schedule: `pip install schedule`
2. Manually add `source` and `destination` path on **line 59**
3. Run script on terminal
4. Stopped script using Ctrl + C on Windows, and Ctrl + Z on Unix.
