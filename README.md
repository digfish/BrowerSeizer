BrowserSeizer
=============

## Purpose

Browser Seizer allows you to take into consideration the fact that you can already have a browser open and if even if that browser it's not the one selected as default on the system, it will open (in the already running browser) any link you clicked outside. Useful, because it avoids from having to launch one completely new instance of the default browser. 

Being all browsers nowadays memory hoggers, specially if you don't have a system with an abundance in memory, this small script can be useful from having to wait from the default to have to complete its entire launch.

## How it works
Simply register the script as the default browser. What it does is that it will search for all installed browsers using its usual location in each operating system.

The script was tested in Linux Ubuntu and Windows 10. For MacOs I haven't tried.

## Instructions on how to register `seizer.py` as the default browser

### Windows

### Linux Ubuntu
The provided `browser-seizer.desktop` can be used to register the script as the default browser. Copy this file to the dir `$HOME/local/share/applications` that is where it resides normally all the shortcuts for the menu. Take care to first edit the .desktop file and change the line where is located the `Exec=` entry to reflect the location of the script. From there if you access the System Settings > Details > Default Applications on 'Web' in the dropdown box you'll see a new entry called 'Browser Seizer' select that one and your application
