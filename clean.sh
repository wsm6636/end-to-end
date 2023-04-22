#!/bin/bash

if [ $# -eq 0 ]
then
  echo “all rm /output/*”
  echo “n rm /output/2interconn/*”
  echo “y rm /output/1 and 2*”
  exit 1
elif [ $1 = "all" ] 
then
  rm ./output/1single/*.npz
  rm ./output/2interconn/*.npz 
  rm ./output/3plots/*.pdf
  echo "rm *.npz and *.pdf"
elif [ $1 = "n" ]
then
  rm ./output/2interconn/*.npz 
  echo "rm /output/2interconn/*.npz"
else [ $1 = "y"]
  rm ./output/1single/*.npz
  rm ./output/2interconn/*.npz 
  echo "rm *.npz"
fi
