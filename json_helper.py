#!/usr/bin/env python3
# The following env variables are assumed available and valid:
# GITHUB_ACTOR, GITHUB_RUN_ID, GITHUB_HEAD_REF
import os
import re
import sys
import json

def check_skip(data):
  msg = data["head_commit"]["message"]
  if re.search("skp-ci", msg):
    return data["id"]
  else:
    return -1

def cancel_workflow(data):
  # GITHUB_HEAD_REF is the same 
  wfs=[x["id"] for x in data if x["head_repository"] is not None and
        re.search(os.environ["GITHUB_ACTOR"], x["head_repository"]["owner"]["login"]) and
        x["head_branch"]=="master" and x["id"]!=int(os.environ["GITHUB_RUN_ID"]) and
        (x["status"]=="queued" or x["status"]=="in_progress")]

  return wfs

def main():

  if sys.argv[1]=="check_skip":
    data = json.load(sys.stdin)["workflow_run"]
    cancel_id = check_skip(data)
    print(cancel_id)
  elif sys.argv[1]=="cancel_workflow":
    data = json.load(sys.stdin)["workflow_runs"]
    wfs = cancel_workflow(data)
    if len(wfs)==0:
      print("")
    else:
      print(*wfs)
  else:
    print("ERROR")

if __name__ == "__main__": main()
