CALL exporter.bat
pyinstaller -F --noconsole --paths="/ScannerApp" "ScannerApp/bootstrap.py"
@pause