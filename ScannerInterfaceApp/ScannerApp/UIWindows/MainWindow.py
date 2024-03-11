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
     # public fields
    scans = {} # dict of dicts where asset_tag_number is key
    scan_entry_primary_key = 'asset_tag_number' # global reference for 
    hearing_scans = False # whether app is listening for scans
    scans_file_path = "scans//scans.txt"
    settings_file_path = "settings//settings.txt"
    file_heading = f'# File generated at {datetime.now().strftime('%m/%d/%Y %H:%M')}\n#############################\n'
    invalid_chars = ['<', '>', '%', '@', '*', '\\', r'\'', r'\"']
    # end public fields
    
    # application state fields
    __app_title = 'Asset Scanner Application'
    __version_no = 'v0.0.1'
    __status = "Uninitialized"
    __sub_status = ""
    __db_handle = None
    # end application state fields

    # settings fields
    _default_db_host = ''
    _default_db_port = ''
    _default_db_name = ''
    _default_db_table = ''

    auto_push_scans = False # whether app-side item data is pushed to db without a user comparison
    __scan_polling_interval = 0.0
    # end settings fields

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

    def set_status(self, new_status: str):
        '''Sets the application status'''
        self.__status = new_status
        QtWidgets.QApplication.processEvents()

    def set_sub_status(self, new_sub_status: str):
        '''Sets application sub-status'''
        self.__sub_status = new_sub_status
        QtWidgets.QApplication.processEvents()

    def reset_sub_status(self):
        '''Resets sub status'''
        self.set_sub_status('')

    def show_loading(self):
        '''Show loading status'''
        self.set_sub_status("Loading...")

    @QtCore.pyqtSlot(bool)
    def set_auto_push(self, value: bool):
        '''Set settings for auto-pushing scans of existing items onto database'''
        self.auto_push_scans = value
  

    def __init__(self, *args, **kwargs):
        '''Main Window Initialization'''
        super().__init__(*args, **kwargs) # init QTMainWindow

        self.show_loading() # set initial status

        self.ui = Ui_MainWindow() # load passed ui
        self.ui.setupUi(self) # populate window with ui
        self.setWindowTitle(self.__app_title)

        # get settings from local stored file
        self.load_settings()
        self.ui.auto_push_scans.setChecked(self.auto_push_scans) 
        # get scans from local storage
        self.read_scans()

        # if file was empty or no scans returned
        if self.scans == None or len(self.scans) == 0:
            self.try_populate_scan_file() # populate and write default scans file
            self.read_scans()

        self.set_status("Running") # application is now running

        self.ui.vs_scans_table.populate(True) # populate scans table
        
    @QtCore.pyqtSlot()
    def closeEvent(self, event):
        '''Called when application is about to close'''
        self.save_settings()
        if self.db_connected:
            self.__disconnect_from_db()
        super(QtWidgets.QMainWindow, self).closeEvent(event)

    def try_populate_scan_file(self):
        '''Populate scans file with default values'''
        new_scan = {
            self.scan_entry_primary_key: '12345',
            "description": "laptop"
        }
        new_scan1 = {
            self.scan_entry_primary_key: '1224',
            'short_desc': 'Desktop'
        }
        # add new entries to runtime dict of dicts
        self.scans[new_scan[self.scan_entry_primary_key]] = new_scan
        self.scans[new_scan1[self.scan_entry_primary_key]] = new_scan1

        # try default values to scans file
        self.write_scans()


    def __write_scans_to(self, file_path: str):
        '''Write scans to target file at passed path'''
        
        self.set_sub_status("Writing to file...")

        # make scans folder if it doesn't exist
        dir_name = file_path.split('//')[0]
        if (not isdir(dir_name)):
            mkdir(dir_name)

        #  open scans file
        with open(file_path, 'w+') as f:
            # init payload list
            json = []
            # if scans dict is not None or empty
            if self.scans and len(self.scans) > 0: 
                # iterate thru scans and add new line between each scan entry
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

        self.reset_sub_status()


    def write_scans(self) -> None:
        '''Write runtime scans dict to file'''
        self.__write_scans_to(self.scans_file_path)


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
            
            self.set_sub_status("Reading scan file contents...")

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
            loaded_scans = '\n'.join(valid_lines)

            if loaded_scans: # if file is not empty
                # convert to list of dicts from JSON
                loaded_scans = loads(loaded_scans)

                # set global reference primary key for scans dict - first scan entry's first column name
                self.scan_entry_primary_key = list(loaded_scans[0].keys())[0]

                # iterate thru scan dicts
                for scan_dict in loaded_scans:
                    # add scan record to runtime dict with asset tag number (unique) as key
                    self.scans[scan_dict[self.scan_entry_primary_key]] = scan_dict 

            self.reset_sub_status() 


    def read_scans(self):
        '''Read scans from file to runtime scans dict'''
        self.__read_scans_from(self.scans_file_path)


    def try_populate_settings_file(self):
        '''Populate default settings file'''
        self._default_db_host = "localhost"
        self._default_db_port = ""
        self._default_db_name = "alpha2"
        self._default_db_table = 'ITEM'
        self.auto_push_scans = False
        self.__scan_polling_interval = 0.2
       

        self.save_settings()


    def load_settings(self):
        '''Read settings from settings file and apply them'''
        self.set_sub_status("Reading settings file contents...")
        
        # if no settings file found, make new one
        if not isfile(self.settings_file_path):
            OkWindow("No settings file found! Generating new one!", 
                     "No settings file found",
                     False,
                     None
                     )
            
            self.try_populate_settings_file()
        # if settings file found
        else:
            with open(self.settings_file_path) as f:
                lines = f.readlines()
                
                 # filter out file comments
                valid_lines = []
                for line in lines:
                    if line[0] == ('#' or '\n#' or '# '):
                        continue
                    else:
                        valid_lines.append(line)
                
                # join file contents back together
                loaded_settings = '\n'.join(valid_lines)

                if loaded_settings: # if file is not empty
                    # convert from JSON to each setting
                    loaded_settings = loads(loaded_settings)

                    self._default_db_host = loaded_settings[0]
                    self._default_db_port = loaded_settings[1]
                    self._default_db_name = loaded_settings[2]
                    self._default_db_table = loaded_settings[3]
                    self.auto_push_scans = loaded_settings[4]
                    self.__scan_polling_interval = loaded_settings[5]

        self.reset_sub_status()
        

    def save_settings(self):
        '''Save settings to local settings file'''
        self.set_sub_status("Writing to file...")

        targ_dir = self.settings_file_path.split('//')[0]
        if not isdir(targ_dir):
            mkdir(targ_dir)
        
        json = []
        json.append(self._default_db_host)
        json.append(self._default_db_port)
        json.append(self._default_db_name)
        json.append(self._default_db_table)
        json.append(self.auto_push_scans)
        json.append(self.__scan_polling_interval)

        # convert payload to json - indented 1 space
        json = dumps(json, indent=1)

        with open(self.settings_file_path , 'w+') as f:
            # write scans to file including file heading
            f.writelines(self.file_heading + json)

        self.reset_sub_status()
        

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
        inputWin.accepted.connect(callback)
        inputWin.exec()


    def __backup_scans(self, backup_file_name: str):
        '''Serialize current scans to backup local timestampted file'''
        if (backup_file_name is None or backup_file_name == ""): 
            #print("No file name given!")
            OkWindow("No file name given!", 'No file name given', True, None)
            return
        
        # add json extension to file name if not there already
        # TODO check for other extensions and correct them
        if ('.json' not in str(backup_file_name)):
            backup_file_name = 'scans//' + str(backup_file_name) + '.json'
        
        self.set_sub_status("Backing up scans...")

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
        
        self.reset_sub_status()
    
    def find_invalid_chars(self, test_string: str) -> list[str]:
        '''Return number of invalid chars in string'''
        if test_string == None or test_string == '' or len(test_string) == 0:
            return []
        else:
            found_invalid_chars = []
            # check input for invalid characters
            for char in self.invalid_chars:
                if char in test_string:
                    found_invalid_chars.append(char)
            return found_invalid_chars

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
        self.ui.vs_new_scan_btn.setStyleSheet("background-color: Orange; font: 12pt MS Shell Dlg 2; color: black")
        self.__update_scan_status()

    def enable_scan_listen(self):
        '''Enable listening for new scans'''
        if not self.db_connected:
            self.hearing_scans = True
            self.ui.vs_new_scan_btn.setStyleSheet("background-color: Green; font: 12pt MS Shell Dlg 2; color: white")
            self.__update_scan_status()
            self.__do_register_scans()

    def __update_scan_status(self):
        '''Updates text/color on scans button'''
        if self.hearing_scans:
            self.ui.vs_new_scan_btn.setText("Listening")
            self.set_sub_status("Listening for scans...")
        else:
            self.ui.vs_new_scan_btn.setText("Scan")
            self.reset_sub_status()


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
            selected_item = self.ui.vs_scans_table.currentItem()
            while (self.hearing_scans 
                   and selected_item == new_cell 
                   and (new_cell == None or len(new_cell.text()) == 0)):
                new_cell = self.ui.vs_scans_table.item(targ_row, 0)
                QtWidgets.QApplication.processEvents()
            if self.hearing_scans:
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
                self._default_db_host,
                self._default_db_port,
                self._default_db_name,
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
                        "Push data to database": lambda: self.__sync_with_db(True),
                        "Pull data from database": lambda: self.__sync_with_db(False)
                    }

                    # successfully connected to target database, can now sync
                    choose_push_pull = OptionWindow("Connection Successful\nChoose Database Sync Type:", 
                                  "Choose sync type", 
                                  True,
                                  options,
                                  False
                                  )
                    choose_push_pull.rejected.connect(self.__disconnect_from_db)
                    choose_push_pull.exec()
                else: # validation success, connection failed
                    self.set_sub_status("Connection Failed")
                    self.ui.statusbar.force_refresh()
                    label_port = port
                    if (port == "" or port == None):
                        label_port = str(3306)
                    label_text = f"Cannot connect to database\nHost: {host}\nPort: {label_port}\nTarget Database: {database}\nUsername: {user}"
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
        '''
        # if db is not connected
        if not self.db_connected:
            OkWindow("No DB connection detected. Cannot sync.",
                     "No database connected",
                     True,
                     None
                     ) 
        else: # if connected to a db
            if push:
                # prompt to save changes first
                self.ui.vs_scans_table.try_save_changes()
            
            targ_table = ''

            targ_table_input = InputWindow('Enter target table to push/pull',
                                           'Select target table',
                                           self._default_db_table,
                                           True,
                                           None,
                                           None,
                                           False
                                           )
            
            get_text = targ_table_input.ui.input.text
            
            def get_targ_table():
                nonlocal targ_table
                targ_table = get_text()

            targ_table_input.accepted.connect(get_targ_table)
            targ_table_input.exec()

            self.set_sub_status("Pushing to database...")

            # get db handle's cursorc and reset it
            cursor = self.__db_handle.cursor(dictionary=True)
            cursor.reset()

            # check if table is NOT in DB
            cursor.execute('SELECT COUNT(*) FROM information_schema.tables WHERE table_name = \'' + targ_table + '\'')
            result = list(cursor.fetchone().values())[0]
            if result == 0:
                OkWindow("Target table " + targ_table + " not found in database: " + self.__db_handle.database,
                         "Target table not found",
                         True,
                         None
                         )
                # close connection to db
                self.__disconnect_from_db()
                return

            cursor.reset()

            # query db ITEM table contents
            cursor.execute('SELECT * FROM ' + targ_table)

            # cache raw results
            db_data_raw = cursor.fetchall()

            # translate SQL to list of dicts for app use
            pull_working_data = self.__parse_db_to_runtime(db_data_raw)

            ## NOTE: if item's entry key was changed in this app, it will push a DUPLICATE entry (different key) onto db!
            ## NOTE: tracking the previously changed entry keys is a possible solution, but that would means comparing each item's previous keys to every row's key in the db...
            
            if push: # if pushing to db
                invalid_entries = []

                test_keys = None
                try:
                    test_keys = list(list(pull_working_data.values())[0].keys())
                except:
                    pass
                
                def push_scan():
                    # replace entry in pull working data with app scans entry
                    pull_working_data[asset_tag_no] = deepcopy(self.scans[asset_tag_no])
                
                yes_to_all = False
                
                def y_to_all():
                    nonlocal yes_to_all
                    yes_to_all = True

                # iterate through app-side item data
                for asset_tag_no in self.scans:
                    pull_data_keys = pull_working_data.keys()

                    # if db has item entry with same asset tag number
                    if asset_tag_no in pull_data_keys:
                        if self.auto_push_scans or yes_to_all:
                            # replace entry in pull working data with app scans entry
                            push_scan()
                        else:
                            # SHOW USER COMPARISON POPUP WINDOW
                            scans_option_text = '===== LOCAL SCAN: ====='
                            pull_data_option_text = '===== PULLED FROM DATABASE: ====='

                            # populate option button text with item entry data
                            for col, value in self.scans[asset_tag_no].items():
                                scans_option_text += f"\n{col} : {value}"
                            for col, value in pull_working_data[asset_tag_no].items():
                                pull_data_option_text += f"\n{col} : {value}"
                           
                            # define options menu options
                            options = {
                                scans_option_text: push_scan,
                                pull_data_option_text: None,
                                "Yes to All": lambda: [push_scan(), y_to_all()]
                            }

                            # show option menu
                            OptionWindow("Choose which item entry to push to database:",
                                         "Choose push entry",
                                         True,
                                         options
                                         )
                            
                    # if db does not already have item in it AND is a valid entry
                    # TODO check if all NOT NULL fields have values in them
                    elif test_keys == None or len(self.scans[asset_tag_no].keys()) >= len(test_keys) - 2:
                        # copy item entry into working data
                        push_scan()
                    # if an invalid entry was found
                    else: 
                        invalid_entries.append(asset_tag_no)
                    
                # notify user of any invalid entries
                if len(invalid_entries) > 0:
                    # populate label text
                    label_text = 'The following item entries did not have enough inputted information to be included in the database push:\n'
                    for entry_key in invalid_entries:
                        label_text += entry_key + '\n'

                    # notify user
                    OkWindow(label_text,
                             'Invalid entries not pushed',
                             False,
                             None
                             )
                    
                # copy pull working data back to app-side scans
                self.scans = deepcopy(pull_working_data)

                # translate dict of dicts working data back into SQL-readable data
                push_working_data = self.__parse_runtime_to_db(pull_working_data)
                
                try:
                    # iterate through push data and replace it in db ITEM table    
                    for item_data_entry in push_working_data:
                        # replace db item data with corresponding asset tag number with push_working_data's item_data
                        cursor.reset()
                        keys = list(item_data_entry.keys())
                        input = list(item_data_entry.values())
                        sql = "REPLACE INTO " + targ_table + " (" 
                        for i in range(len(keys) - 1):
                            sql += keys[i] + ', '
                        sql += keys[-1]
                        sql += ") "
                        sql += "VALUES ("
                        for i in range(len(input) - 1):
                            sql += '%s, '
                        sql += '%s'
                        sql += ')'
                        cursor.execute(sql, input)
                        
                        # commit changes to db
                        self.__db_handle.commit()

                    # notify user that push is done
                    OkWindow("Local item data successfully pushed to database.",
                            "DB update successful",
                            True,
                            None
                            )
                except sql_connector.DataError as e:
                    self.set_sub_status("Error during database push")
                    OkWindow(e.msg + '\nNo data was pushed.', "Error during push", True, None)
                
                cursor.close()

            self.reset_sub_status()

            # finally, copy updated pull working data back to app-side scans and update table display
            self.scans = deepcopy(pull_working_data)
            self.ui.vs_scans_table.populate(True)
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
        self.set_sub_status("Connecting...")
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
            self.__update_scan_status()
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
            # get first column name from first item in db data for use in populating dict of dicts
            # set global runtime reference for entry keys
            self.scan_entry_primary_key = list(db_data[0].keys())[0]

            # populate runtime dict of dicts with entries
            for entry in db_data:
                runtime[entry[self.scan_entry_primary_key]] = entry

            return runtime


    def __parse_runtime_to_db(self, runtime_dict: dict[dict]) -> list[dict]:
        '''Translate local runtime data to db-compliant data'''
        if runtime_dict == None or len(runtime_dict) == 0:
            return
        
        db_list = []
        for key, entry in runtime_dict.items():
            db_list.append(entry)

        return db_list