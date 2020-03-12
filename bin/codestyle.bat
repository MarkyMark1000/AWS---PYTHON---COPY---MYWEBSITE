:: WARNING - UNTESTED AT PRESENT AND SCRIPT NEEDS A LOT OF WORK

set "direc=%cd%"

:: Move to parent directory if executing from scripts
if ($direc EQU "scripts" ) ( cd .. )

:: Activate Environment to ensure we have pycodestyle
./venv/bin/activate

:: Check the main ebdjango directory
echo ""
echo ""
echo ""
echo " ********************************** "
echo " *** Checking Main App ebdjango *** "
echo " ********************************** "
echo ""
for %%f in (.\ebdjango\*.py) do pycodestyle --statistics %%f
echo ""

:: Scan through directories in apps directory that do not end in __
:: THIS COULD DEFINATELY DO WITH SOME WORK
for %%d in (.\apps\*) do ( for %%f in (%%d\*.py) do pycodestyle --statistics %%f )