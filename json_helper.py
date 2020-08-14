#!/usr/bin/env python3
# The following env variables are assumed available and valid:
# GITHUB_ACTOR, GITHUB_RUN_ID, GITHUB_HEAD_REF
import os
import re
import sys
import json

def check_skip(data):
  ub=min(10, len(data))
  msg=[x["head_commit"]["message"] for x in data[:ub] if x["id"]==int(os.environ["GITHUB_RUN_ID"])]

  if re.search("skip-ci", msg[0]):
    return 'yes'
  return 'no'

def cancel_workflow(data):
  # GITHUB_ACTOR is the same 
  # GITHUB_HEAD_REF is the same 
  # GITHUB_RUN_ID is different (or GITHUB_SHA is different)
  # either queued or in_progress
  wfs=[x["id"] for x in data if x["head_repository"] is not None and
        re.search(os.environ["GITHUB_ACTOR"], x["head_repository"]["owner"]["login"]) and
        x["head_branch"]=="master" and x["id"]!=int(os.environ["GITHUB_RUN_ID"]) and
        (x["status"]=="queued" or x["status"]=="in_progress")]

  return wfs

def main():
  data = json.load(sys.stdin)["workflow_runs"]

  if sys.argv[1]=="check_skip":
    answer=check_skip(data)
    print(answer)
  elif sys.argv[1]=="cancel_workflow":
    wfs = cancel_workflow(data)
    if len(wfs)==0:
      print("")
    else:
      print(*wfs)

if __name__ == "__main__": main()
