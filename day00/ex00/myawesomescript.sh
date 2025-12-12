#!/bin/sh
curl -sI $1 | grep -i "^location" | cut -d ' ' -f2
