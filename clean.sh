#!/bin/bash

if [ $# -eq 0 ]
then
  echo “rm none”
  exit 1
elif [ $1 = "y" ]
then
  rm ./output/1single/*.npz
  rm ./output/2interconn/*.npz 
  rm ./output/3plots/*.pdf
  echo "rm *.npz and *.pdf"
else [ $1 = "n" ]
  rm ./output/1single/*.npz
  rm ./output/2interconn/*.npz 
  echo "rm *.npz"
fi
