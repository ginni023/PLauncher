@echo off
REM KTOPIA.exe build script
pip install --upgrade pyinstaller pystray pillow ttkbootstrap
REM crawling(whl) package and Playwright driver are bundled for CRAWLING tasks
pyinstaller --onefile --noconsole --name KTOPIA --paths src\main --hidden-import pystray._win32 --collect-all crawling --collect-all playwright main.py
REM launcher version file next to the exe
copy /Y .launcher dist\
REM crawler settings next to the exe (paths in it are relative to the exe folder)
if exist crawler.properties copy /Y crawler.properties dist\
REM SQL XML files live next to ktopia.db (dist\resource\db)
if not exist dist\resource\db mkdir dist\resource\db
copy /Y resource\db\initSql.xml dist\resource\db\
copy /Y resource\db\mainSql.xml dist\resource\db\
echo.
echo Build done: dist\KTOPIA.exe
pause
