#!/bin/bash

for dir in /gbo/AGBT17A_477/*
do 
    #echo "I'm in $dir$"
    containsfits="false"
    containspfd="false"
    for files in $dir/*
    do
	echo "$files"
	IFS='/' read -ra ADDR <<< "$files"
	echo "$ADDR"
	for i in "${ADDR[@]}"; do
	    if [[ "$i" == *"_1929+16_"*".fits" ]]; then
		containsfits="true"
	    fi
	    if [[ "$i" == *"_1929+16.pfd" ]]; then
		#echo "$i"
		containspfd="true"
		#echo $containspfd
		#echo [ "$containspfd" != "true" ]
		#echo "im here"
	    fi 
	done
	#echo $containfits
	#echo $containspfd
     if [ "$containsfits" = "true" ] && [ "$containspfd" = "false" ]; then
         echo $containsfits
	 echo $containspfd
	 echo "I need a a pfd file in $dir"
     fi
    done
done
