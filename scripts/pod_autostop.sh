#!/bin/bash
# Stop this RunPod pod when a marker file appears or a deadline passes, whichever comes first.
# A pod that idles costs money; this is the safety net for runs driven from outside the pod.
# Needs RUNPOD_API_KEY and RUNPOD_POD_ID in the environment (source /etc/rp_environment first).
# Usage:
#   source /etc/rp_environment; export RUNPOD_API_KEY RUNPOD_POD_ID
#   (setsid nohup bash scripts/pod_autostop.sh <deadline, epoch seconds> <marker> [<marker> ...] \
#       > /workspace/logs/autostop_<tag>.log 2>&1 < /dev/null &)
# It stops the pod (podStop); it never terminates it. Kill it by pid, never with pkill -f.
set -u
DEADLINE=$1
shift
: "${RUNPOD_API_KEY:?RUNPOD_API_KEY not set}" "${RUNPOD_POD_ID:?RUNPOD_POD_ID not set}"
echo "$(date -u +%FT%TZ) watching pod $RUNPOD_POD_ID, deadline $(date -u -d "@$DEADLINE" +%FT%TZ), markers: $*"
while true; do
  now=$(date +%s)
  why=""
  for m in "$@"; do [ -e "$m" ] && why="marker $m"; done
  [ "$now" -ge "$DEADLINE" ] && why="deadline"
  if [ -n "$why" ]; then
    echo "$(date -u +%FT%TZ) stopping: $why"
    [ "$why" != "deadline" ] && sleep 45            # let a final git push finish
    while true; do
      curl -s -m 30 -X POST "https://api.runpod.io/graphql" \
        -H "content-type: application/json" -H "Authorization: Bearer $RUNPOD_API_KEY" \
        --data "{\"query\":\"mutation { podStop(input: {podId: \\\"$RUNPOD_POD_ID\\\"}) { id desiredStatus } }\"}"
      echo
      command -v runpodctl > /dev/null && runpodctl stop pod "$RUNPOD_POD_ID"
      sleep 60                                       # still here: the stop did not take, try again
    done
  fi
  sleep 20
done
