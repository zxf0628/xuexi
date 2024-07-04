@echo off
setlocal enabledelayedexpansion

cd /d %~dp0

Set /A Count = 0
Set /A Offset = 1


Set date_time=%date:~0,4%-%date:~5,2%-%date:~8,2%_%time:~0,2%-%time:~3,2%

Set icmpEchoLog_join=icmpEchoLog_!date_time!.txt
Set a_join=a_!date_time!.txt


:BEGIN
Set /A Count=%Count% + %Offset%


call armNQAarmNQA.exe >> !icmpEchoLog_join! | type !icmpEchoLog_join!

echo 
echo %date% %time% >> !a_join!
for /f "tokens=*" %%A in ('ping 20.236.44.162 -n 60 -w 500') do (echo %%A>>!a_join! )
echo %date% %time% >> !a_join!

echo "The %Count% Times End."

Timeout /T 5 /NOBREAK

if %Count% lss 10 (

goto BEGIN

) else (

echo "Quit Test"

)
