@echo off
Rem
Rem Run the following commands in sequence. If any fail run again up to 3 times. See if you
Rem can get all 3 to run without error:
Rem Dism /Online /Cleanup-Image /StartComponentCleanup
Rem Dism /Online /Cleanup-Image /RestoreHealth
Rem SFC /scannow
Rem
date /t & time /t
echo Dism /Online /Cleanup-Image /StartComponentCleanup
Dism /Online /Cleanup-Image /StartComponentCleanup
echo ...
date /t & time /t
echo Dism /Online /Cleanup-Image /RestoreHealth
Dism /Online /Cleanup-Image /RestoreHealth
echo ...
date /t & time /t
echo SFC /scannow
SFC /scannow
date /t & time /t