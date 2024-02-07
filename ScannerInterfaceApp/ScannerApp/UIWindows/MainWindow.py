from PyQt6 import QtWidgets, QtCore
from .uielements import Popup
from .MainAppUI import Ui_MainWindow
from os import mkdir
from os.path import isfile, isdir
from json import loads, dumps


class MainWindow(QtWidgets.QMainWindow):
    '''Main window running ui'''
     # fields
    scans = {} # dict of dicts where serial no is key
    file_path = "scans//scans.txt"
    file_heading = '# Test file generated\n# test comment\n#############################\n'

    __app_title = 'Asset Database Interface'
    __version_no = 'v0.0.1'
    __status = "None"
    # end fields

    # properties
    @property
    def version(self) -> str:
        return self.__version_no
        
    @property
    def status(self) -> str:
        return self.__status
    # end properties

    @staticmethod
    def write_scans() -> None:
        '''Write runtime scans dict to file'''
        # make scans folder if it doesn't exist
        dir_name = MainWindow.file_path.split('//')[0]
        if (not isdir(dir_name)):
            mkdir(dir_name)

        with open(MainWindow.file_path, 'w+') as f:
            # init payload list
            json = []

            new_scan = {
                "serial_number": 12345,
                "short_desc": "laptop"
            }
            new_scan1 = {
                'serial_number': 1224,
                'short_desc': 'Desktop'
            }
            MainWindow.scans[new_scan['serial_number']] = new_scan
            MainWindow.scans[new_scan1['serial_number']] = new_scan1

            if MainWindow.scans and len(MainWindow.scans) > 0: # if scans dict is not None or empty
                # iterate thru scans and add new line between each
                for scan in MainWindow.scans.values():
                    json.append(scan)
                
                # convert payload to json - indented 1 space
                json = dumps(json, indent=1)
                
                # write scans to file including file heading
                f.writelines(MainWindow.file_heading + json)
            
            else: # if scans dict is None or empty
                # write empty file with file heading
                f.writelines(MainWindow.file_heading)

    @staticmethod
    def read_scans(): 
        '''Read scans from file to runtime scans dict'''
        # return if no file
        if (not isfile(MainWindow.file_path)):
                return

        with open(MainWindow.file_path) as f:
            lines = f.read() # read entire file as one string
            scans = lines.split(MainWindow.file_heading)[1] # get only scans part of file
            if scans: # if file is not empty
                # convert to list of dicts from JSON
                scans = loads(scans)

                # iterate thru scan dicts
                for scan_dict in scans:
                    # add scan record to runtime dict with serial number (unique) as key
                    MainWindow.scans[scan_dict['serial_number']] = scan_dict  

    def __init__(self, *args, **kwargs):
        '''Main Window Initialization'''
        super().__init__(*args, **kwargs)
        
        self.ui = Ui_MainWindow() # load passed ui
        self.ui.setupUi(self) # populate window with ui

        # DEBUG WRITE SCANS TO FILE
        self.write_scans()

        # get scans from local storage
        self.read_scans()

        # DEBUG PRINT RUNTIME SCANS LIST
        print(self.scans)

        self.goto_screen(0) # start at main menu
        self.connect_persistent_elements() # connect slots to persistent ui elements
    
    def connect_persistent_elements(self):
        '''Maps custom signals to slots that cannot be directly mapped in Qt Designer'''
        # Main Menu
        self.ui.mm_new_scan_btn.clicked.connect(lambda: self.goto_screen(1))
        self.ui.mm_view_scans_btn.clicked.connect(lambda: self.goto_screen(2))
        
        # New Scan
        self.ui.ns_back_btn.clicked.connect(lambda: self.goto_screen(0))

        # View Scans
        self.ui.vs_to_mm_btn.clicked.connect(lambda: self.goto_screen(0))

    def setup_view_scans(self):
        '''Populate current scans table'''
        print("Column number : ", self.ui.vs_scans_table.columnCount())
        
        # populate table
        self.ui.vs_scans_table.populate(self.scans)

    def show_dialog(self, value: str):
        '''Show dialog popup window'''
        new_popup = Popup(value)
        new_popup.exec()

    def goto_screen(self, value: int):
        '''Navigate to main menu'''
        # TODO clear all values on current screen
        
        # grab app title
        new_title = self.__app_title

        if value == 0:
            # move to main menu   
            new_title += ' - Main Menu'
        elif value == 1:
            # new scan
            pass
        elif value == 2:
            # view scans
            new_title += ' - View Scans'
            self.setup_view_scans() # populate scans table on new screen

        self.setWindowTitle(new_title) # set new window title
        # enable to corresponding screen
        self.ui.main_screen_stack.setCurrentIndex(value)

    def backup_scans(self):
        '''Serialize current scans to local timestamped file'''
        # TODO
        pass