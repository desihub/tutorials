The script will run papermill in whatever desi kernel you wish on all jupyter notebooks with fall within one or two directories of the main tutorial directories. It will produce an output html file called auto_test.html which will be in the 'testing' directory. This will contain a list of the notebooks and the first input line at which they failed.

To run the automated test use:

./test_papermill.sh kernel
e.g.
./test_papermill.sh desi-main
./test_papermill.sh desi-22.5

If you don't know what kernels you have avalible use:
jupyter kernelspec list

To install follow intructions here:
https://desi.lbl.gov/trac/wiki/Computing/JupyterAtNERSC 

for help/issues with this script contact becky.canning@port.ac.uk

