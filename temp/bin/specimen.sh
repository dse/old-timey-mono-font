#!/usr/bin/env bash
set -o errexit                  # exit if any pipeline fails
set -o nounset                  # set your variables first
set -o pipefail                 # if one component fails the pipeline fails
shopt -s lastpipe               # last component is exec'd in foreground
# set -o xtrace

BINDIR="$(realpath "$(dirname "$0")")"
MAINDIR="$(realpath "${BINDIR}/..")"

echo "BINDIR=${BINDIR}"
echo "MAINDIR=${MAINDIR}"

main () {
    for font_file in "${MAINDIR}"/dist/ttf/*.ttf ; do
        basename="$(basename "$font_file")"
        basename_no_ext="${basename%.ttf}"
        woff2_file="${MAINDIR}/specimen/src/fonts/${basename_no_ext}.woff2"
        mkdir -p "$(dirname "${woff2_file}")"
        "${MAINDIR}/bin/fontconvert" "${font_file}" "${woff2_file}"
        echo "Generated ${woff2_file}"
    done
}

###############################################################################
main "$@"
