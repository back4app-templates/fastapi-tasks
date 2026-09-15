#!/usr/bin/env bash
# Stack: bash | Verifies a deployed FastAPI tasks API: health → create → read → update → delete → validation.
set -euo pipefail
BASE="${1:?usage: deploy-check.sh <base-url>}"
echo "1/6 health";   curl -fsS "$BASE/healthz" | grep -q '"ok":true'
echo "2/6 create";   ID=$(curl -fsS -X POST -H "Content-Type: application/json" -d '{"title":"Write the tutorial"}' "$BASE/tasks" | python3 -c 'import json,sys;print(json.load(sys.stdin)["objectId"])'); echo "    id: $ID"
echo "3/6 read";     curl -fsS "$BASE/tasks/$ID" | grep -q 'Write the tutorial'
echo "4/6 update";   curl -fsS -X PATCH -H "Content-Type: application/json" -d '{"done":true}' "$BASE/tasks/$ID" | grep -q updatedAt
echo "5/6 validate"; [ "$(curl -s -o /dev/null -w '%{http_code}' -X POST -H "Content-Type: application/json" -d '{"title":"   "}' "$BASE/tasks")" = "422" ]
echo "6/6 delete";   [ "$(curl -s -o /dev/null -w '%{http_code}' -X DELETE "$BASE/tasks/$ID")" = "204" ]
echo "OK"
