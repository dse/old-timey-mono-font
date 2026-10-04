#!/usr/bin/env bash
set -o errexit
set -o pipefail
set -o nounset
shopt -s lastpipe

main () {
    for script in "$(dirname "$0")"/*.py ; do
        "${script}" "$@"
    done
}

main "$@"
