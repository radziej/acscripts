# !/usr/bin/bash
# Script to load CMSSW
#
# This function is meant to be sourced into your .bashrc
# Example: source ~/cmsswscript.sh /user/radziej/CMSSW/
#
# The (optional) path argument tells the function where the CMSSW installations
# are located. By default, it assumes you have linked them to your home
# directory.
#
# Call the function by typing its name and the version number of CMSSW. The
# first matching CMSSW installation will be loaded.
# Example: cmssw 72
# If versions CMSSW_7_1_3, CMSSW_7_2_1 and CMSSW_7_2_3 are available, it will
# load CMSSW_7_2_1, which is the first match.

# define directory where CMSSW versions are installed
if [ -z "$1" ]; then
    CMSSW_DIR="${HOME}"
else
    CMSSW_DIR="$1"
fi

function cmssw() {
    # check if any input has been given, else print help text
    if [ -z "$1" ]; then
        echo "Usage: $0 A[BCD]"
        echo ""
        echo "A, B, C, and D represent the numbers that are part of the CMSSW release."
        echo "The environment of the first match will be loaded."
        echo "If no matches are found, an error is thrown."
        return 1
    fi

    local cmssw_versions=`ls ${CMSSW_DIR} | grep CMSSW`
    if [ -z "${cmssw_versions}" ]; then
        echo "No CMSSW versions found!"
        return 1
    fi
    local version_array
    read -a version_array <<< ${cmssw_versions}

    # build regex from input argument
    local regex="CMSSW_"
    for number in `grep -o . <<< $1`; do
        regex="${regex}${number}.*"
    done

    # search for a match
    local match=""
    for version in "${version_array[@]}"; do
        match=`sed -n "/${regex}/p" <<< ${version}`
        if [ ! -z ${match} ]; then
            break
        fi
    done

    if [ -z "${match}" ]; then
        echo "No matching CMSSW version found!"
        return 1
    fi

    echo "Loading ${match} ..."
    source /cvmfs/cms.cern.ch/cmsset_default.sh ;
    V=${HOME}/${match} ;
    cd $V && eval `scramv1 runtime -sh` && source /afs/cern.ch/cms/ccs/wm/scripts/Crab/crab.sh ;
    echo "Returning to"
    cd - ;
    return 0
}
