'''
THIS SOFTWARE, ITS SOURCE CODE, AND ANY DISTRIBUTIONS THEREOF IS PROPERTY OF GEORGE MASON UNIVERSITY.
AUTHOR : MARTIN HAYNESWORTH
'''

'''Custom child classes of QT widgets so custom slots can be added'''
from copy import deepcopy

from PyQt6 import QtCore, QtWidgets

from .ConfirmUI import Ui_DialogConfirm
from .DBSyncLoginUI import Ui_DBSyncLogin
from .OkUI import Ui_DialogOk
from .BackupInputUI import Ui_BackupFileInput
from.OptionsUI import Ui_DialogOptions


class PushButton(QtWidgets.QPushButton):
    '''Custom push button'''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Popup(QtWidgets.QDialog):
    '''Base class for all dialogs'''
    def __init__(self, ui: type, label_text: str, window_text: str, set_modal: bool, on_accept, on_reject, auto_exec: bool = True, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setModal(set_modal)
        self.ui = ui()
        self.ui.setupUi(self)
        self.ui.label.setText(label_text)
        self.setWindowTitle(window_text)

        # connect passed accept/reject signals to dialog slots
        if (on_accept != None): self.accepted.connect(on_accept)
        if (on_reject != None): self.rejected.connect(on_reject)
        
        if auto_exec: self.exec()


############ CUSTOM POPUPS
class OkWindow(Popup):
    '''Notification (Ok) Dialog Box'''
    def __init__(self, label_text: str, window_text: str, set_modal: bool, on_ok, auto_exec: bool = True, *args, **kwargs):
        super().__init__(Ui_DialogOk, label_text, window_text, set_modal, on_ok, None, auto_exec, *args, **kwargs)

class ConfirmWindow(Popup):
    '''Confirmation dialog box'''
    def __init__(self, label_text:str, window_text: str, set_modal: bool, on_accept, on_reject, auto_exec: bool = True, *args, **kwargs):
        super().__init__(Ui_DialogConfirm, label_text, window_text, set_modal, on_accept, on_reject, auto_exec, *args, **kwargs)

class InputWindow(Popup):
    '''Single line input dialog box'''
    def __init__(self, label_text: str, window_text: str, default_input_text: str, set_modal: bool, on_accept, on_reject, auto_exec: bool = True, *args, **kwargs):
        super().__init__(Ui_BackupFileInput, label_text, window_text, set_modal, on_accept, on_reject, auto_exec, *args, **kwargs)
        self.ui.input.setText(default_input_text)

class DBConnectWindow(Popup):
    '''Dialog box for establishing connection to database'''
    def __init__(self, label_text: str, window_text: str, set_modal: bool, on_accept, on_reject, default_host, default_port, default_db, auto_exec: bool = True, *args, **kwargs):
        super().__init__(Ui_DBSyncLogin, label_text, window_text, set_modal, on_accept, on_reject, auto_exec, *args, **kwargs)
        self.ui.db_host_nameip_input.setFocus()
        if default_host != None:
            self.ui.db_host_nameip_input.setText(default_host)
        if default_port != None:
            self.ui.db_port_input.setText(default_port)
        if default_db != None:
            self.ui.db_name_input.setText(default_db)

        if self.ui.db_name_input.text() != "":
            self.ui.username_input.setFocus()

class OptionWindow(Popup):
    '''
    Dialog box containing n option buttons to choose from.
    Accepts a dictionary of string, callback which connects to auto-populated buttons in the window.
    '''
    def __init__(self, label_text: str, window_text: str, set_modal: bool, callbacks: dict, auto_exec: bool = True, *args, **kwargs):
        if len(callbacks) == 0:
            self.close()
        else:
            super().__init__(Ui_DialogOptions, label_text, window_text, set_modal, None, None, False, *args, **kwargs)
            self.ui.option_btn.hide() # hide the initial button
            self.ui.option_btn.setFocus()
            # populate option buttons and connect them with passed slots

            self.font().setPointSize(10)

            for button_text, callback in callbacks.items():    
                option_btn = QtWidgets.QPushButton(parent=self.ui.button_box)
                option_btn.setObjectName(button_text)
                option_btn.setText(button_text)
                if callback != None:
                    option_btn.clicked.connect(callback)
                option_btn.clicked.connect(self.accept)
                self.ui.verticalLayout.addWidget(option_btn)
            QtWidgets.QApplication.processEvents()

            if auto_exec:
                self.exec()
############ END CUSTOM POPUPS

     
class StackedWidget(QtWidgets.QStackedWidget):
    '''Custom stacked widget'''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class MenuBar(QtWidgets.QMenuBar):
    '''Custom menu bar'''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.ui.auto_push_scans.triggered.connect(self.window().set_auto_push)


class StatusBar(QtWidgets.QStatusBar):
    '''Custom status bar'''
    # status bar refresh inverval in seconds
    __refresh_interval = 0.2

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # setup and run thread for updating status
        self.__refresh_status()

    def force_refresh(self) -> None:
        '''Forces Status Bar UI refresh'''
        self.__populate_status()
        QtWidgets.QApplication.processEvents()

    @QtCore.pyqtSlot()
    def __refresh_status(self) -> None:
        '''Periodically refresh status bar'''
        self.__populate_status()
         # call method again every tick of the app internal clock
        # slightly delayed due to internal clock being init'd before statusbar obj
        # print("Status bar refreshed!")
        QtCore.QTimer.singleShot(int(self.__refresh_interval*1000), self.__refresh_status)

    def __populate_status(self) -> None:
        '''Handle populating status bar ui with target string(s)'''
        if (self.parentWidget().sub_status == "" or self.parentWidget().sub_status == None):
            self.showMessage(f'{self.parentWidget().version} | {self.parentWidget().status}')
        else:
            self.showMessage(f'{self.parentWidget().version} | {self.parentWidget().status} - {self.parentWidget().sub_status}')


class Table(QtWidgets.QTableWidget):
    '''Custom table widget'''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.working_data = {} # init dict for holding data containing changes
        self.last_edited_Row_Key = None # init last edited row var
        self.__dup_notif = None # init existing entry found notification var

    def populate(self, reset: bool = False) -> None:
        ''' Populates table with values from passed list of dicts'''
        '''TODO handle sorting on population'''
        if reset:
            self.working_data = deepcopy(self.window().scans)

        if len(self.working_data) == 0:
            return
        items = list(self.working_data.values())

        # get row with max number of columns and maps those columns
        prev_keys = list(items[0].keys())
        max_keys = prev_keys
        
        # find row with the most entries (columns)
        for i in range(1, len(items)):
            cur_keys = items[i].keys()
            if len(cur_keys) > len(prev_keys):
                max_keys = list(cur_keys)
            prev_keys = cur_keys

        # pick whichever item has more columns
        col_count = len(max_keys)
        row_count = len(items)
        if  col_count == 0:
            return
        
        ### setup table columns        
        self.clear() # clear table contents and headers
        self.setColumnCount(col_count) # set table column count to new column name

        if row_count == 0:
            # TODO indicate no rows present
            return
        
        # iterate thru all columns of first item
        for i in range(col_count):  
            # init header item
            header = QtWidgets.QTableWidgetItem()
            # align text to v center 
            header.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignVCenter) 
            # set text to corresponding column name (key in dict)
            header.setText(max_keys[i])
            # place new table widget item on table header
            self.setHorizontalHeaderItem(i, header)

        # set row size of table to number of items to display
        self.setRowCount(row_count)

        ### populate rows
        # iterate through all items 
        for i in range(len(items)):
            # key column keys for each item
            keys = list(items[i].keys())
            # iterate thru keys
            for j in range(len(keys)):
                # generate table item
                cell = QtWidgets.QTableWidgetItem()
                cell.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignVCenter) 
                # assign value to cell
                content = items[i][keys[j]]
                cell.setText(str(content))
                # place cell on table
                self.setItem(i, j, cell)
        # print("Scans table populated! Num Cols: ", self.columnCount(),"Num Rows: ", self.rowCount())
   
    @QtCore.pyqtSlot(int, int)
    def update_scans(self, row, col) -> None:
        '''
        Update working data with new cell value.
        This is called when something is manually typed into cell.
        '''
        if self.item(row, col) == None: 
            return
        
        scans_vals = list(self.working_data.values())

        # find cell with the typed value in it
        new_value = self.item(row, col).text()
        
        # check input for invalid characters
        inv_chars = self.window().find_invalid_chars(new_value)
        
        if  len(inv_chars) > 0:
            self.__register_invalid_scan()
            OkWindow('Invalid character(s) entered: ' + str(inv_chars), 'Invalid char entered', True, None)
            return 
        
        # if target row is not the first one
        # make sure there are no empty rows above target
        if row != 0:
            found_valid = False
            num_up = 1
            checked_row = 1
            # if this is not the first now
            while not found_valid and checked_row > 0:
                try:
                    checked_row = row - num_up
                    row_above = scans_vals[checked_row]
                    found_valid = True
                except IndexError:
                   num_up += 1
                   checked_row = row - num_up
            
            # if no valid found all the way up to the top, make this new target row
            if not found_valid:
                row = 0
            else: # if there was a valid row found, make target row right below it
                row = checked_row + 1

        # if adding new row
        if row > len(scans_vals) - 1:
            new_entry_key = "0" + scans_vals[-1][self.window().scan_entry_primary_key]
            # if not adding new row by editing entry key
            if col != 0 and (self.item(row, col -1) == None or self.item(row, col-1).text() == (None or "")):
                # clear current cell value
                self.item(row, col).setText('')
                # add placeholder entry key to row
                self.setItem(row, 0, QtWidgets.QTableWidgetItem(new_entry_key))
                # register table update
                self.update_scans(row, 0)
                return
            elif col == 0: # if adding new row by editing entry key
                # if clearing entry key to blank
                if new_value == "" or new_value == None:
                    # set entry key of default value
                    self.item(row, col).setText(new_entry_key)
                    # register table update
                    self.update_scans(row, col)
                    return
                
                found_duplicate = False
                duplicate_row = 0
                # if new value is not blank
                # check for duplicate entry keys
                for entry_key in self.working_data.keys():
                    # if duplicate found
                    if new_value == entry_key:
                        found_duplicate = True
                        break
                    else:
                        duplicate_row += 1
                
                if found_duplicate:
                    self.__register_invalid_scan()
                    
                    # select current row to editing
                    self.setCurrentCell(duplicate_row, 0)

                    if self.window().notify_on_existing_found:
                    # notify user that existing entry found
                        if self.__dup_notif != None:
                            self.__dup_notif.close()
                        self.__dup_notif = OkWindow(
                            "Existing entry value found: " + new_value,
                            "Existing entry found",
                            False,
                            None
                        )

                     # clear out newly added row
                    # for column in range(self.columnCount()):
                    #     self.setItem(row, column, None)
                    
                    '''
                    # init notification window
                    dup_notif = OkWindow(
                        "Cannot enter duplicate entry key.",
                        "Duplicate entry key detected: " + new_value,
                        True,
                        None,
                        False
                    )
                    # notify user
                    dup_notif.exec()
                    '''
                    return 
                
                # copy previous row's content to new row
                if new_value not in self.working_data.keys():
                    # self.working_data[new_value] = scans_vals[-1].copy()
                    self.working_data[new_value] = {self.window().scan_entry_primary_key : new_value}
                    # placeholder row of "undefined" values
                    for column in range(1, self.columnCount()):
                        self.setItem(row, column, QtWidgets.QTableWidgetItem("Undefined"))

                row_columns = list(self.working_data[new_value].keys())

                # show new row contents on target row cells
                for i in range(1, len(row_columns)):
                    self.setItem(row, i, QtWidgets.QTableWidgetItem(self.working_data[new_value][row_columns[i]]))

                scans_vals = list(self.working_data.items())
                targ_row = scans_vals[row][1]
                targ_col = list(targ_row.keys())[col]
                self.working_data[new_value][targ_col] = new_value

        scans_vals = list(self.working_data.values())
        targ_row = scans_vals[row]
        targ_row_keys = list(targ_row.keys())

        # if target column is not in scan record being updated
        if col >= len(targ_row_keys):
            # try to find corresponding column any other row
            test_col_name = self.__try_find_col_in_scans(col)
            if (test_col_name == None):
                # TODO handle when there are no corresponding column entries in any rows 
                pass
            else: # if corresponding column name found
                targ_col = test_col_name
        else: # if target column is in scan entry
            targ_col = targ_row_keys[col]
        targ_key = targ_row[self.window().scan_entry_primary_key]
        
        last_edited = dict()

        # if changing entry key of same row
        if col == 0 and targ_key != new_value:
            def on_confirm():
                nonlocal new_value
                nonlocal targ_key
                nonlocal last_edited

                # copy over value to new key
                self.working_data[str(new_value)] = self.working_data[str(targ_key)].copy()
                # remove old key/value pair
                self.working_data.pop(str(targ_key))
                # cache new row entry as target row
                last_edited = self.working_data[str(new_value)]

            ConfirmWindow(
                "You are about to alter entry key " + targ_key + ".\nProceed?",
                "Confirm entry key change",
                True,
                on_confirm,
                None
            )
        else:
            # cache existing row entry at target row
                last_edited = self.working_data[str(targ_key)]

        # update target cell with new value
        last_edited[str(targ_col)] = new_value

        # cache last edited row's entry key
        self.last_edited_Row_Key = list(last_edited.items())[0][1]

        #print('New scans: ', self.working_data)

    def __save_changes(self) -> None:
        '''Save table changes to runtime scans dict'''
        if self.working_data != None:
            self.window().show_loading()
            # check for any blank rows
            for key in self.working_data:
                # if found blank row, delete it
                if key == None or len(self.working_data[key].values()) == 0:
                    del self.working_data[key]
            # copy working data w changes over to runtime dict      
            self.window().scans = deepcopy(self.working_data)
            self.window().write_scans()
            self.window().reset_sub_status()
            OkWindow("Table changes saved!",
                     "Changes Saved",
                     False,
                     None
                     )
            self.populate(True) # refresh table

    @QtCore.pyqtSlot()
    def try_save_changes(self) -> None:
        '''Show confirmation popup before saving changes'''
        # disable scan listen if on
        if self.window().hearing_scans:
            self.window().disable_scan_listen()

        ConfirmWindow("Would you like to save any changes?", 
              "Confirm Save", 
              True,
              on_accept=self.__save_changes,
              on_reject=None)
    
    @QtCore.pyqtSlot()
    def reset_table(self) -> None:
        '''Resets the table to original values'''
        # disable scan listen if on
        if self.window().hearing_scans:
            self.window().disable_scan_listen()

        ConfirmWindow("Do you want to reset all changes to last save?", 
                "Confirm Reset",
                True, 
                on_accept=lambda: self.populate(True), 
                on_reject=None, 
                parent=self)
    
    @QtCore.pyqtSlot()
    def add_row(self) -> None:
        '''Add an empty scan table row'''
        previous_row_key = self.item(self.rowCount() - 1, 0)
        if  previous_row_key != None and previous_row_key.text() != ("" or None):
            self.insertRow(self.rowCount())
            QtWidgets.QApplication.processEvents()


    def __del_last_edited_row(self) -> None:
        '''Deletes the last edited row from table'''
        del self.working_data[self.last_edited_Row_Key]
        self.populate()


    @QtCore.pyqtSlot()
    def try_del_last_edited_row(self) -> None:
        '''Show confirmation  pop-up for deleted last edited row'''
        if self.last_edited_Row_Key == None:
            # TODO show ok menu notifying to edit a row first
            pass
        
        # disable scan listen if on
        if self.window().hearing_scans:
            self.window().disable_scan_listen()
            
        ConfirmWindow("Would you like to delete the last edited row?\nEntry Key: " + self.last_edited_Row_Key, 
              "Confirm Delete Row", 
              True,
              on_accept=self.__del_last_edited_row,
              on_reject=None)
        

    def __try_find_col_in_scans(self, index: int) -> str:
        '''
        Try to find a scan column name in table data at passed index.
        Basically, find row entry key by row position in table.
        '''
        for item in self.working_data:
            # try to find corresponding column in list
            try:
                targ_col = list(self.working_data[item].keys())[index]
                return targ_col
            # if index error, assume row does not have an entry for the column
            except IndexError:
                continue
        
        # if no rows have an column entry at the passed index
        return None
    

    def __register_invalid_scan(self) -> None:
        # disable scan listen so cursor doesnt stay at the bottom of the table
        self.window().disable_scan_listen()

        # close the editor on the new row's cell
        # self.closeEditor(self, QtWidgets.QAbstractItemDelegate.EndEditHint.NoHint)
        # QtCore.QCoreApplication.processEvents()

        # remove newly added blank row
        self.removeRow(self.rowCount() - 1)

        # make table the focused widget
        self.setFocus()