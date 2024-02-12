from PyQt6 import QtWidgets, QtCore
from .uielements import ConfirmWindow
from .MainAppUI import Ui_MainWindow
from os import mkdir
from os.path import isfile, isdir
from json import loads, dumps


class MainWindow(QtWidgets.QMainWindow):
    '''Main window running ui'''
     # fields
    scans = {} # dict of dicts where serial no is key
    hearing_scans = False # whether app is listening for scans
    file_path = "scans//scans.txt"
    file_heading = '# Test file generated\n# test comment\n#############################\n'

    __app_title = 'Asset Scanner Application'
    __version_no = 'v0.0.1'
    __status = "Unitialized"
    __sub_status = ""
    # end fields

    # properties
    @property
    def version(self) -> str:
        return self.__version_no
        
    @property
    def status(self) -> str:
        return self.__status

    @property
    def sub_status(self) -> str:
        return self.__sub_status
    # end properties

    @classmethod
    def set_status(cls, new_status: str):
        '''Sets the application status'''
        cls.status = new_status
    
    @classmethod
    def set_sub_status(cls, new_sub_status: str):
        '''Sets application sub-status'''
        cls.sub_status = new_sub_status

    def __init__(self, *args, **kwargs):
        '''Main Window Initialization'''
        super().__init__(*args, **kwargs)
        
        self.set_status("Loading") # set initial status

        self.ui = Ui_MainWindow() # load passed ui
        self.ui.setupUi(self) # populate window with ui

        # get scans from local storage
        self.read_scans()

        # if file was empty or no scans returned
        if self.scans == None or len(self.scans) == 0:
            self.try_populate_scan_file()
            self.read_scans()

        # DEBUG PRINT RUNTIME SCANS LIST
        print(self.scans)

        self.goto_screen(2) # start at view scans screen
        self.connect_persistent_elements() # connect slots to persistent ui elements
        self.set_status("Running") # application is now running
        
    def try_populate_scan_file(self):
        '''Populate scans file with default values'''
        new_scan = {
            "serial_number": '12345',
            "short_desc": "laptop"
        }
        new_scan1 = {
            'serial_number': '1224',
            'short_desc': 'Desktop'
        }
        self.scans[new_scan['serial_number']] = new_scan
        self.scans[new_scan1['serial_number']] = new_scan1

        # try default values to scans file
        self.write_scans()
        
    def write_scans(self) -> None:
        '''Write runtime scans dict to file'''
        # make scans folder if it doesn't exist
        dir_name = self.file_path.split('//')[0]
        if (not isdir(dir_name)):
            mkdir(dir_name)

        with open(self.file_path, 'w+') as f:
            # init payload list
            json = []

            if self.scans and len(self.scans) > 0: # if scans dict is not None or empty
                # iterate thru scans and add new line between each
                for scan in self.scans.values():
                    # remove any blank values
                    for scan_key in scan:
                        if scan[scan_key] == "" or scan[scan_key] == None:
                            del scan[scan_key]
                    json.append(scan)
                
                # convert payload to json - indented 1 space
                json = dumps(json, indent=1)
                
                # write scans to file including file heading
                f.writelines(self.file_heading + json)
            
            else: # if scans dict is None or empty
                # write empty file with file heading
                f.writelines(self.file_heading)

    def read_scans(self): 
        '''Read scans from file to runtime scans dict'''
        # return if no file
        if (not isfile(self.file_path)):
                return

        with open(self.file_path) as f:
            lines = f.read() # read entire file as one string
            if lines == "" or lines == None: # if file is empty
                # TODO handle empty file 
                return

            ## get only scans part of file
            # split out file by line
            scan_lines = lines.split('\n')
            
            # filter out file comments
            valid_lines = []
            for line in scan_lines:
                if line[0] == ('#' or '\n#' or '# '):
                    continue
                else:
                    valid_lines.append(line)
            
            # join file contents back together
            scans = '\n'.join(valid_lines)

            if scans: # if file is not empty
                # convert to list of dicts from JSON
                scans = loads(scans)

                # iterate thru scan dicts
                for scan_dict in scans:
                    # add scan record to runtime dict with serial number (unique) as key
                    self.scans[scan_dict['serial_number']] = scan_dict  

    def connect_persistent_elements(self):
        '''Maps custom signals to slots that cannot be directly mapped in Qt Designer'''
        ### Main Menu
        self.ui.mm_new_scan_btn.clicked.connect(lambda: self.goto_screen(1))
        self.ui.mm_view_scans_btn.clicked.connect(lambda: self.goto_screen(2))
        
        ### New Scan
        self.ui.ns_back_btn.clicked.connect(lambda: self.goto_screen(0))

        ### View Scans
        # self.ui.vs_new_scan_btn.clicked.connect(lambda: ) # new scan btn
        # self.ui.vs_del_last_btn.clicked.connect(lambda: self.goto_screen(0)) # bck btn

    @QtCore.pyqtSlot(int)
    def goto_screen(self, value: int):
        '''Navigate to main menu'''
        # TODO clear all values on current screen
        if self.ui.main_screen_stack.currentIndex == value: return

        # grab app title
        new_title = self.__app_title

        if value == 0:
            # move to main menu   
            new_title += ' - Main Menu'
        elif value == 1:
            # new scan
            new_title += ' - New Scan'
        elif value == 2:
            # view scans
            new_title += ' - View Scans'
            self.ui.vs_scans_table.populate(True) # populate scans table on new screen

        self.setWindowTitle(new_title) # set new window title
        # enable to corresponding screen
        self.ui.main_screen_stack.setCurrentIndex(value)

    @QtCore.pyqtSlot()
    def backup_scans(self):
        '''Serialize current scans to backup local timestamped file'''
        # TODO
        pass

    @QtCore.pyqtSlot()
    def toggle_scan_listen(self):
        '''Toggle app listening for new scans'''
        self.hearing_scans = not self.hearing_scans
        self.update_scan_status()

    def enable_scan_listen(self):
        '''Enable listening for new scans'''
        self.hearing_scans = True
        self.update_scan_status()
    
    def disable_scan_listen(self):
        "Disable listening for new scans"
        self.hearing_scans = False
        self.update_scan_status()

    def update_scan_status(self):
        '''Updates text/color on scans button'''
        if self.hearing_scans:
            self.ui.vs_new_scan_btn.setText("Scanning")
            self.set_sub_status("Listening for scans...")
        else:
            self.ui.vs_new_scan_btn.setText("Scan")
            self.set_sub_status("")