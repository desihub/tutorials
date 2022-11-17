#!/bin/bash

# EDR DOC sprint, 17th Nov 2022
# (e-mail to becky.canning@port.ac.uk)
#
# Running the tutorials with papermill
#

date > auto_test.html

# read in the kernal to use
kernel=$1
echo "<p> </p>" >> auto_test.html
echo $kernel >> auto_test.html

# make list of the notebooks
# uncomment t run for all
ls ../*/*.ipynb > list_notebooks.tmp
ls ../*/*/*.ipynb >> list_notebooks.tmp

while read line; 
do
  echo "testing $line"
  
    echo "papermill $line test_auto_output.ipynb -k $kernel" | sh
    echo "<p> </p>" >> auto_test.html
    echo "<header> "$line"</header>" >> auto_test.html
    grep Exception test_auto_output.ipynb >> auto_test.html

done < list_notebooks.tmp

# clean up
rm list_notebooks.tmp
rm test_auto_output.ipynb



