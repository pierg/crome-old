#!/bin/bash
filename=$1
steps=$2

nuXmv -int
read_model -i $filename
flatten_hierarchy
encode_variables
build_model
pick_state -i
simulate -i -k $steps