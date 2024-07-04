@echo off

set host=172.31.1.147
set logfile=Log_timeout_%host%_%date:~0,4%%date:~5,2%%date:~8,2%_%time:~0,2%%time:~3,2%.log
echo %logfile%

echo Target Host = %host% >%logfile%
for /f "tokens=*" %%A in ('ping %host% -n 1 -w 500') do (echo %%A>>%logfile% && GOTO Ping)
:Ping
for /f "tokens=* skip=2" %%A in ('ping %host% -n 1 -w 500') do (
    echo %date% %time:~0,2%:%time:~3,2%:%time:~6,2% %%A>>%logfile%
    echo %date% %time:~0,2%:%time:~3,2%:%time:~6,2% %%A
    timeout 1 >NUL 
    GOTO Ping)