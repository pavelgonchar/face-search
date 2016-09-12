#!/bin/bash

DEFAULT_FACE="mr_bean.jpg"
INPUT=${1:-$DEFAULT_FACE}
MONTAGE=1
MONTAGE=${2:-$MONTAGE}

if [[ $INPUT =~ .*http.* ]]
then
    IMAGE=${INPUT##*/}
    wget $INPUT -O /tmp/$IMAGE
    INPUT="/tmp/$IMAGE"
fi

OUTPUT=`CUDA_VISIBLE_DEVICES=0 python step1.py --input $INPUT 2>/dev/null`

if [[ $MONTAGE == 1 ]]
then
	RESULT=`echo $OUTPUT | CUDA_VISIBLE_DEVICES=0 python step2.py | perl montage.pl`
else
	RESULT=`echo $OUTPUT | CUDA_VISIBLE_DEVICES=0 python step2.py`
fi

echo "$RESULT"
