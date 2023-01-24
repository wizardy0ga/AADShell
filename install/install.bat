rem Utilize this script to secure the file permissions
rem for the secrets store, source code, tools directory and launch file.
rem After executing, only Administrators and elevated processes
rem will be able to change the source, read the store, use the
rem scripts in the tools directory or execute the program.
rem This ensures that only administrator level processes can interact with the program and data.

Rem move back two directories to where AADShell is stored
cd ..\..

Rem remove inheritance from AADShell dir and all inside objects
icacls AADShell /q /t /c /inheritance:d

Rem give ownership of dir and sub-dirs to Administrator group
takeown /A /F AADShell /R

Rem set the main file, src, store and tools dirs integrity level to High
icacls AADShell\store /setintegritylevel H
icacls AADShell\tools /setintegritylevel H
icacls AADShell\src /setintegritylevel H
icacls AADShell\aadshell.py /setintegritylevel H

Rem remove the users group object from the store, tools dir acl
icacls AADShell\store /q /t /c /remove:g Users
icacls AADShell\tools /q /t /c /remove:g Users

rem remove current user from store, source tools dir and launch file.
icacls AADShell\store /q /t /c /remove:g %username%
icacls AADShell\tools /q /t /c /remove:g %username%
icacls AADShell\src /q /t /c /remove:g %username%
icacls AADShell\aadshell.py /q /t /c /remove:g %username%