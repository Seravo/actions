#!/bin/bash
set -e
set -u
set -o pipefail

#
# bump Seravo/actions versions in all actions to specified version
#
# usage: bump-versions.sh v1.16.4
#

BASEDIR="$(dirname "$(dirname "$0")")"
VERSION="$1"

[ -z "${VERSION}" ] && echo >&2 "usage: $0 <version>" && exit 1

find "${BASEDIR}" -type f -name "action.yml" -print0 |while IFS= read -r -d '' actionfile
do
  echo "Checking file '${actionfile}'..."
  sed -i "s,seravo/actions/\(.*\)@.*,seravo/actions/\1@${VERSION},I" "${actionfile}"
done
