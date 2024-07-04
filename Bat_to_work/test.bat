@echo off
setlocal enabledelayedexpansion

color 7E


Set current_date=%date%
Set current_time=%time%

echo current_date:!current_date!
echo current_time:!current_time!

Set formatted_date=!current_date:/=-!
Set formatted_date=!formatted_date: =!
Set formatted_date=!formatted_date:~0,10%!
Set formatted_time=!current_time::=-!
Set formatted_time=!formatted_time:.=!

echo formatted_date:!formatted_date!
echo formatted_time:!formatted_time!



Set icmpEchoLog_join=icmpEchoLog_!formatted_date!_!formatted_time!_.txt
Set a_join=a_!formatted_date!_!formatted_time!_.txt


echo testzxf >> !icmpEchoLog_join!


Timeout /T 5 /NOBREAK