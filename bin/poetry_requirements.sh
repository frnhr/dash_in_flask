#!/bin/sh
set -e

cd "${0%/*}/.."

poetry export --format=requirements.txt | grep -ve "^    --hash" | cut -d';' -f1  | cut -d'\' -f1 > requirements.txt
