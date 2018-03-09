#!/bin/bash
# @GomesAR functions
# tools for terminal
# 2018-02 MIT License


function cdl() {	
	cd $1
	curr=`pwd`
	printf "\t\033[0;31mcd to: ${curr}\033[0m\n"
	ls -lhF
}

function externalip() {
	echo "Your external IP is: `python -c 'from requests import get;print(get("https://api.ipify.org").text)'`"
}
