#!/bin/bash

#./blah.sh to run from command line.   Use chmod to ensure it has execute permission

# Get the path tot he python project based upon where we are executing this shell
direc=${PWD##*/}

# Move to parent directory if executing from bin
if [ $direc == "scripts" ]
then
   cd ..
fi

# Activate Environment to ensure we have pycodestyle
source venv/bin/activate

# Check the main ebdjango directory
echo ""
echo ""
echo ""
echo " ********************************** "
echo " *** Checking Main App ebdjango *** "
echo " ********************************** "
echo ""
pycodestyle --statistics ./ebdjango/*.py
echo ""

# Scan through directories in apps directory that do not end in __
APPS=./apps/*
for A in $APPS
do
    if [[ -d $A ]] && [[ ${A: -2} != "__" ]]; then
        echo ""
        echo " *** checking App ${A} *** "
        echo ""
        pycodestyle --statistics $A/*.py
        echo ""
    fi
done

# Checking the scripts directory
echo ""
echo " *** checking Scripts directory *** "
echo ""
pycodestyle --statistics scripts/*.py
echo ""