#!/bin/bash

INPUTS=Step4/inputs/step4_testcase.micro
mkdir Step4/usertest
for i in $INPUTS
	do
		filename=${i%.*}
		name=${filename##*/}
		echo "Testing input file $i"
		output="${name}Test.out"
		outtest="${name}.out"
		./Micro $i > Step4/usertest/$output
		diff -b -s Step4/usertest/$output Step4/outputs/$outtest
	done
