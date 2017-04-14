#!/bin/bash
for i in `seq 0 4096`;
do
	/problems/995871fcb203d3e223e9e4aaa65e4053/bashloop $i | grep flag
done
