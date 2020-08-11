#!/usr/bin/env python3
import sys
import json
data = json.load(sys.stdin)['workflow_runs']
print(*[x['id'] for x in data if x['status']=='queued' or x['status']=='in_progress'])
