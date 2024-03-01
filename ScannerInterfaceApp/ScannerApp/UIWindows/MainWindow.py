from mysql import connector as sql_connector
from PyQt6 import QtWidgets, QtCore
from .uielements import InputWindow, ConfirmWindow, OkWindow, DBConnectWindow, OptionWindow
from .MainAppUI import Ui_MainWindow
from os import mkdir
from os.path import isfile, isdir
from json import loads, dumps
from datetime import datetime
from copy import deepcopy

class MainWindow(QtWidgets.QMainWindow):
    '''Main window running ui'''
     # fields
    scans = {} # dict of dicts where asset_tag_number is key
    scan_entry_key = 'asset_tag_number'
    hearing_scans = False # whether app is listening for scans
    file_path = "scans//scans.txt"
    file_heading = '# Test file generated\n# test comment\n#############################\n'

    __app_title = 'Asset Scanner Application'
    __version_no = 'v0.0.1'
    __status = "Unitialized"
    __sub_status = ""
    __db_handle = None
    __scan_polling_interval = 0.05
    __auto_push_scans = False # whether app-side item data is pushed to db without a user comparison
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
    
    @property
    def db_connected(self) -> bool:
        return self.__db_handle != None and self.__db_handle.is_connected()
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

        self.setWindowTitle(self.__app_title)

        # get scans from local storage
        self.read_scans()

        # if file was empty or no scans returned
        if self.scans == None or len(self.scans) == 0:
            self.try_populate_scan_file()
            self.read_scans()

        self.set_status("Running") # application is now running

        self.ui.vs_scans_table.populate(True) # populate scans table on new screen
        
    def try_populate_scan_file(self):
        '''Populate scans file with default values'''
        new_scan = {
            self.scan_entry_key: '12345',
            "description": "laptop"
        }
        new_scan1 = {
            self.scan_entry_key: '1224',
            'short_desc': 'Desktop'
        }
        self.scans[new_scan[self.scan_entry_key]] = new_scan
        self.scans[new_scan1[self.scan_entry_key]] = new_scan1

        # try default values to scans file
        self.write_scans()

    def __write_scans_to(self, file_path: str):
        '''Write scans to target file at passed path'''
        # make scans folder if it doesn't exist
        dir_name = file_path.split('//')[0]
        if (not isdir(dir_name)):
            mkdir(dir_name)

        with open(file_path, 'w+') as f:
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

    def write_scans(self) -> None:
        '''Write runtime scans dict to file'''
        self.__write_scans_to(self.file_path)

    def __read_scans_from(self, file_path: str): 
        '''Read scans from file to runtime scans dict'''
        # return if no file
        if (not isfile(file_path)):
                return

        with open(file_path) as f:
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
                    # add scan record to runtime dict with asset tag number (unique) as key
                    self.scans[scan_dict[self.scan_entry_key]] = scan_dict  

    def read_scans(self):
        '''Read scans from file to runtime scans dict'''
        self.__read_scans_from(self.file_path)

    @QtCore.pyqtSlot()
    def try_backup_scans(self):
        '''Serialize current scans to backup local timestamped file'''
        # prompt to save changes first
        self.ui.vs_scans_table.try_save_changes()
        # display input window 
        inputWin = InputWindow("Enter backup file name:",
                    "Backup file name input",
                    "scans" + datetime.now().strftime('%m_%d_%Y-%H_%M'),
                    True,
                    None,
                    None,
                    False
                )
        
        # hacky approach but achieves desired result
        # manually connecting inputWin dialog on_accept callback for inputWindow after its definition
        # to get around not referencing inputWin var within its own obj definition
        getText = inputWin.ui.input.text
        callback = lambda: self.__backup_scans(getText())
        inputWin.accepted.connect(lambda: callback())
        inputWin.exec()

    def __backup_scans(self, backup_file_name: str):
        '''Serialize current scans to backup local timestampted file'''
        if (backup_file_name is None): 
            print("No file anem given!")
            return
        
        # add json extension to file name if not there already
        # TODO check for other extensions and correct them
        if ('.json' not in str(backup_file_name)):
            backup_file_name = 'scans//' + str(backup_file_name) + '.json'
        
        # cache success notification 
        success = OkWindow("Backup file successfully overwritten!",
                            "Backup Success",
                            False,
                            None,
                            False
                        )
        
        # cache callbacks for writing scans and showing the success dialog
        writeScans = lambda: self.__write_scans_to(backup_file_name)
        showSuccess = lambda: success.exec()
        
        # if target backup file already exists
        if (isfile(backup_file_name)):
            # display confirm window for overwriting backup file
            conf = ConfirmWindow(f"Do you want to overwrite backup file {backup_file_name}?",
                                "Overwrite Backup File",
                                True,
                                lambda: [
                                    writeScans(), 
                                    showSuccess()
                                    ],
                                None
                            )
        else: # if writing new file, write file
            writeScans()
            success.ui.label.setText("Backup file successfully written!")
            showSuccess()

    @QtCore.pyqtSlot()
    def toggle_scan_listen(self):
        '''Toggle app listening for new scans'''
        # cannot enable scan hearing while db is connected
        if not self.hearing_scans and self.db_connected:
            pass
        elif self.hearing_scans:
            self.disable_scan_listen()
        else:
            self.enable_scan_listen()

    @QtCore.pyqtSlot()
    def disable_scan_listen(self):
        "Disable listening for new scans"
        self.hearing_scans = False
        self.__update_scan_status()

    def enable_scan_listen(self):
        '''Enable listening for new scans'''
        if not self.db_connected:
            self.hearing_scans = True
            self.__update_scan_status()
            self.__do_register_scans()

    def __update_scan_status(self):
        '''Updates text/color on scans button'''
        if self.hearing_scans:
            self.ui.vs_new_scan_btn.setText("Scanning")
            self.set_sub_status("Listening for scans...")
        else:
            self.ui.vs_new_scan_btn.setText("Scan")
            self.set_sub_status("")

    def __do_register_scans(self):
        '''Get scan data, convert it to a new row entry or update it if exists'''
        if self.hearing_scans: # only register scan if hearing scans
            # add new blank row if needed 
            self.ui.vs_scans_table.add_row()
            # get row index of newly added row
            targ_row = self.ui.vs_scans_table.rowCount() - 1
            
            # make table the focused widget
            self.ui.vs_scans_table.setFocus()

            # select current row to editing
            self.ui.vs_scans_table.setCurrentCell(targ_row, 0)

            # wait for enough text to be entered into asset_tag_number cell before refreshing scan listen 
            new_cell = self.ui.vs_scans_table.item(targ_row, 0)
            while new_cell == None or len(new_cell.text()) < 1:
                new_cell = self.ui.vs_scans_table.item(targ_row, 0)
                QtWidgets.QApplication.processEvents()
            QtCore.QTimer.singleShot(int(self.__scan_polling_interval*1000), self.__do_register_scans)

    @QtCore.pyqtSlot()
    def sync_db_btn_clicked(self):
        '''Register connected to database button clicked'''
        # disable scan listen if on
        if self.window().hearing_scans:
            self.window().disable_scan_listen()
            
        # if application is already connected to the database
        if self.db_connected:
            OkWindow(
                'Database already connected. Force DB Disconnect?',
                'Database already connected',
                True,
                self.__disconnect_from_db,
            )
        else: # if not already connected
            login_screen = DBConnectWindow(
                'Establish Database Connection',
                'Database Login',
                True,
                None,
                None,
                False
            )

            # defining action for clicking connect button in db conect window
            @QtCore.pyqtSlot()
            def on_connect():
                '''Validate input and try connecting to db'''
                host = login_screen.ui.db_host_nameip_input.text()
                port = login_screen.ui.db_port_input.text()
                database = login_screen.ui.db_name_input.text()
                user = login_screen.ui.username_input.text()
                pwd = login_screen.ui.password_input.text()
                
                previous_sub_status = self.sub_status
                self.set_sub_status("Connecting to database...")
                self.ui.statusbar.force_refresh()

                # validate input
                # if host is invalid
                if host == None or host == "":
                    OkWindow("No host given", "Invalid Host", True, None)
                # if a port is entered but not a number, notify user
                elif (port != None and port != "") and not str.isdigit(port):
                    OkWindow("Invalid port number given", "Invalid Port Number", True, None)
                elif database == None or database == "":
                    OkWindow("Invalid database name given", "Invalid Database Name", True, None)
                elif self.__try_connect_to_db(host, port, database, user, pwd): # validation success, connection success
                    self.disable_scan_listen() # turn off scan listening if on
                    self.set_sub_status("Connected To Database")
                    self.ui.statusbar.force_refresh()
                    
                    options = {
                        "Push data": lambda: self.__sync_with_db(True),
                        "Pull data": lambda: self.__sync_with_db(False)
                    }

                    # successfully connected to target database, can now sync
                    OptionWindow("Connection Successful\nChoose Database Sync Type:", 
                                  "Choose sync type", 
                                  True,
                                  options
                                  )
                else: # validation success, connection failed
                    self.set_sub_status("Connection Failed")
                    self.ui.statusbar.force_refresh()
                    label_port = port
                    if (port == "" or port == None):
                        label_port = str(3306)
                    label_text = f"Cannot connect to database\nHost: {host}\nPort: {label_port}\nUsername: {user}"
                    OkWindow(label_text, "Connection Failed", True, None)
                    self.set_sub_status(previous_sub_status)
                    self.ui.statusbar.force_refresh()
                    # clear all input fields
                    # login_screen.ui.reset_btn.clicked() 

            login_screen.accepted.connect(on_connect)
            login_screen.exec()

    def __sync_with_db(self, push: bool):
        '''
        Handle pushing updated versions of items onto DB.
        Prompts user to select from duplicates. 
        TODO MUST HANDLE DUPLICATE SCANS CONFLICTS PRIOR TO PUSHING TO DB'
        '''
        # if db is not connected
        if not self.db_connected:
            OkWindow("No DB connection detected. Cannot sync.",
                     "No database connected",
                     True,
                     None
                     ) 
        else: # if connected to a db
            # TODO check if there is an ITEM table in this 
            # get db handle's cursor and reset it
            cursor = self.__db_handle.cursor(dictionary=True)
            cursor.reset()
            # query db ITEM table contents
            cursor.execute('SELECT * FROM ITEM')
            # cache raw results
            db_data_raw = cursor.fetchall()
            # translate SQL to list of dicts for app use
            pull_working_data = self.__parse_db_to_runtime(db_data_raw)

            if push: # if pushing to db
                # iterate through app-side item data
                for asset_tag_no in self.scans:
                    # if db has item entry with same asset tag number
                    if asset_tag_no in pull_working_data.keys():
                        if self.__auto_push_scans:
                            # TODO replace entry in pull working data with app scans entry
                            pass
                        else: 
                            # TODO SHOW USER COMPARISON POPUP WINDOW
                            pass
                    else: # if db does not already have item in it
                        # copy item entry into working data
                        pull_working_data[asset_tag_no] = deepcopy(self.scans[asset_tag_no])

                # copy pull working data back to app-side scans
                self.scans = deepcopy(pull_working_data)

                # translate dict of dicts working data back into SQL-readable data
                push_working_data = self.__parse_runtime_to_db(pull_working_data)    
                # iterate through push data and replace it in db ITEM table    
                for item_data in push_working_data:
                    # TODO sql -> replace db item data with corresponding asset tag number with push_working_data's item_data
                    break

                OkWindow("Local item data successfully pushed to database.",
                         "DB update successful",
                         True,
                         None
                         )

            # finally, copy updated pull working data back to app-side scans
            self.scans = deepcopy(pull_working_data)
            OkWindow(
                "Local item info successfully updated from database.",
                "Local item info updated",
                True,
                None
            )
            # close connection to db
            self.__disconnect_from_db()

    def __try_connect_to_db(self, host: str, port :str, db_name: str, username: str, password: str) -> bool:
        '''Establish connection to DB and return connection handle'''
        if port == None or port == "": # use default port if none specified
            port = 3306
        try:
            db_handle = sql_connector.connect(
                host=host,
                port=port,
                database=db_name,
                user=username,
                password=password
            )
            self.__db_handle = db_handle
            return True
        except sql_connector.errors.DatabaseError:
            return False

    def __disconnect_from_db(self):
        '''End connection to DB'''
        # if db handle is already none
        if self.__db_handle != None:
            self.__db_handle.disconnect()
            self.__db_handle = None
            OkWindow("Database successfully disconnected.",
                     "Database disconnected sucessfully",
                     True,
                     None
                     )
    
    def __parse_db_to_runtime(self, db_data: list[tuple]) -> dict[dict]:
        '''Translate db data to locally stored runtime data'''
        if not self.db_connected: 
            OkWindow("Not connected to any database!",
                     "No Database Connection Detected",
                     True,
                     None)
        else: # if connected to the db
            runtime = dict()
            # get first column name from db data for use in populating dict of dicts
            target_key = db_data(0).keys()[0]
            for entry in db_data:
                runtime[target_key] = entry

            return runtime

    def __parse_runtime_to_db(self, json_dict: dict[dict]) -> list[tuple]:
        '''Translate local runtime data to db-compliant data'''
        pass


    '''
    @QtCore.pyqtSlot(int)
    def goto_screen(self, value: int):
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
    '''