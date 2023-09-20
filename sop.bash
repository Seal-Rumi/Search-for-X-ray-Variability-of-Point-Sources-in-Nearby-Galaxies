#! /bin/bash

#Last updated: 25/Aug/2022

get_script_dir () {
     SOURCE="${BASH_SOURCE[0]}"
     while [ -h "$SOURCE" ]; do
          DIR="$( cd -P "$( dirname "$SOURCE" )" && pwd )"
          SOURCE="$( readlink "$SOURCE" )"
          [[ $SOURCE != /* ]] && SOURCE="$DIR/$SOURCE"
     done
     DIR="$( cd -P "$( dirname "$SOURCE" )" && pwd )"
     echo "$DIR"
}
BASEDIR=$(get_script_dir)

for dir in ./*;do
if [ -d $dir ];then
    cd $dir
    bash $BASEDIR/reprocess.bash
    cd analysis/
    bash $BASEDIR/source_selection.bash
    bash $BASEDIR/makebg.bash
    bash $BASEDIR/bary.bash
    cd ../../
fi
done
