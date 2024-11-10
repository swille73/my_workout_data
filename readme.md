# Trainingstagebuch
Eintragen der Wiederholungen an Liegestütz oder anderen kalistenische Übungen
# Aufbau und Beschreibung des Programms
Über den Input im Terminal können die Wiederholungen eingtragen werden
Bei gültiger Prüfung wird der übergebene Wert in eine CSV Datei geschrieben.
Die Datei wird ausgelesen und die Summe bereits gemachter Wiederholungen vom 
aktuellen Tag angezeigt.
In weiterer Folge soll eine Auswertung möglich gemacht werden wo man die Tage
und deren Wiederholungen dargestellt werden.
# Technischer Aufbau
Erstellen einer Exe Datei mittels pyInstaller:
1. Mit nur einem Script
Beispiel: pyinstaller --onefile hello_pyinstaller.py
2. Mit zusätzlichen Dateien
Beispiel: pyinstaller --onefile --add-data 'data\data_file.txt;data' app_with_data.py