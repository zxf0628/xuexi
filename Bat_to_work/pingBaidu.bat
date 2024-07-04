@echo off

cd /d %~dp0

Set /A Count = 0
Set /A Offset = 1

:BEGIN
Set /A Count=%Count% + %Offset%

call armNQAarmNQA.exe >> icmpEchoLog.txt | type icmpEchoLog.txt

echo 
echo %date% %time% >> a.txt
for /f "tokens=*" %%A in ('ping 20.236.44.162 -n 60 -w 500') do (echo %%A>>a.txt )
echo %date% %time% >> a.txt

echo "The %Count% Times End."

Timeout /T 5 /NOBREAK

if %Count% lss 10 (

goto BEGIN

) else (

echo "Quit Test"

)
