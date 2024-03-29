CALL ui_exporter.bat
pyinstaller -F --noconsole --paths="/ScannerApp" "ScannerApp/bootstrap.py" -n "QRCodeScannerApp"
@pause