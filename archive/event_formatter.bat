setlocal EnableDelayedExpansion
copy BEVENT.EXE event_files\
cd D:\GitHub\Baseball-Stats\event_files
FOR %%f in (D:\GitHub\Baseball-Stats\event_files\*.EVA) DO (
  set fname=%%f
  set fshort=!fname:~-11,7!
  echo !fname:~-11!
  bevent -y !fname:~-11,4! !fname:~-11! > !fshort!.csv
  del %%f
)
FOR %%f in (D:\GitHub\Baseball-Stats\event_files\*.EVN) DO (
  set fname=%%f
  set fshort=!fname:~-11,7!
  echo !fname:~-11!
  bevent -y !fname:~-11,4! !fname:~-11! > !fshort!.csv
  del %%f
)
