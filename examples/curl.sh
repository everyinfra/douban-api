#!/usr/bin/env bash
# 豆瓣 API 的 curl 示例：所有能力都发到同一个地址，只换 action 和 params。
# curl examples for the Douban API: every capability uses the same URL; only action and params change.
#
#   export EVERYINFRA_API_KEY=<your API key>
#   bash examples/curl.sh search 小王子
#   bash examples/curl.sh comments "<item url>"           # search 结果里的 url / the url from a search result
#   bash examples/curl.sh reviews "<item url>"
#   bash examples/curl.sh group_topic "<group topic url>" # https://www.douban.com/group/topic/<ID>/
set -euo pipefail
: "${EVERYINFRA_API_KEY:?Set EVERYINFRA_API_KEY first: https://everyinfra.com/docs#quickstart}"
action=${1:?"usage: bash examples/curl.sh <search|comments|reviews|group_topic> <value>"}
value=${2:?"value: a keyword, an item url or a group topic url"}

case "$action" in
  search)                           params="{\"keyword\":\"$value\"}" ;;
  comments | reviews | group_topic) params="{\"url\":\"$value\"}" ;;
  *) echo "unknown action: $action (use search, comments, reviews or group_topic)" >&2; exit 2 ;;
esac

curl -sS -X POST https://api.everyinfra.com/api/v1/social \
  -H "Authorization: Bearer $EVERYINFRA_API_KEY" \
  -H "Content-Type: application/json" \
  -d "{\"platform\":\"douban\",\"action\":\"$action\",\"params\":$params}"
echo
