'''Custom child classes of QT widgets so custom slots can be added'''
from PyQt6 import QtCore, QtWidgets
from .ConfirmUI import Ui_Dialog
from copy import deepcopy


class PushButton(QtWidgets.QPushButton):
    '''Custom push button'''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class StatusBar(QtWidgets.QStatusBar):
    '''Custom status bar'''
    # status bar refresh inverval in seconds
    __refresh_interval = 0.5

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # setup and run thread for updating status
        self.__refresh_status()

    @QtCore.pyqtSlot()
    def __refresh_status(self):
        '''Periodically refresh status bar'''
        self.showMessage(f'{self.parentWidget().version} | {self.parentWidget().status}')
        # call method again every tick of the app internal clock
        # slightly delayed due to internal clock being init'd before statusbar obj
        # print("Status bar refreshed!")
        QtCore.QTimer.singleShot(int(self.__refresh_interval*1000), self.__refresh_status)


class Popup(QtWidgets.QDialog):
    '''Popup dialog box'''
    def __init__(self, label_text:str, window_text: str, set_modal: bool, on_accept, on_reject, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setModal(set_modal)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.ui.label.setText(label_text)
        self.setWindowTitle(window_text)
        if (on_accept != None): self.accepted.connect(on_accept)
        if (on_reject != None): self.rejected.connect(on_reject)
        self.exec()

class StackedWidget(QtWidgets.QStackedWidget):
    '''Custom stacked widget'''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class Dialog(QtWidgets.QDialog):
    '''Custom dialog window'''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class Table(QtWidgets.QTableWidget):
    sorting_modes = [
        'asc',
        'desc',
    ]

    '''Custom table widget'''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.working_data = {} # init dict for holding data containing changes
        self.last_edited_Row_Serial = None # init last edited row var

    def populate(self, reset: bool = False):
        ''' Populates table with values from passed list of dicts'''
        '''TODO handle sorting on population'''
        if reset:
            self.working_data = deepcopy(self.window().scans)
       
        scans = self.working_data

        if len(scans) == 0:
            return
        items = list(scans.values())

        # get row with max number of columns and maps those columns
        prev_keys = list(items[0].keys())
        max_keys = prev_keys
        
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

        if row_count == 0:
            # TODO indicate no rows present
            return

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
        
        # TODO handle applying sorting

        print("Scans table populated! Num Cols: ", self.columnCount(),"Num Rows: ", self.rowCount())
    
    @QtCore.pyqtSlot(int, int)
    def update_scans(self, row, col):
        '''Update working data with new cell value'''
        new_value = self.item(row, col).text()
        scans_vals = list(self.working_data.values())

        # if adding new row
        if row > len(scans_vals) - 1:
            # if not adding new row by editing serial_no
            if col != 0 and self.item(row, col -1).text() == (None or ""):
                # TODO move selection over to serial_no
                return
            else: # if adding new row by editing serial_no
                self.working_data[new_value] = scans_vals[-1].copy()
                scans_vals = list(self.working_data.values())
                targ_row = list(scans_vals)[row]
                targ_col = list(targ_row.keys())[col]
                self.working_data[new_value][targ_col] = new_value

        scans_vals = list(self.working_data.values())
        targ_row = scans_vals[row]
        targ_row_keys = list(targ_row.keys())

        # if target column is not in scan record being updated
        if col >= len(targ_row_keys):
            # try to find corresponding column other rows
            test_col_name = self.try_find_scan_column(col)
            if (test_col_name == None):
                # TODO handle when there are no corresponding column entries in any rows 
                pass
            else: # if corresponding column name found
                targ_col = test_col_name
        else: # if target column is in scan entry
            targ_col = targ_row_keys[col]
        targ_key = int(targ_row['serial_number'])
        
        last_edited = dict()

        # if changing serial_number of same row
        if col == 0 and int(targ_key) != int(new_value):
            # copy over value to new key
            self.working_data[str(new_value)] = self.working_data[str(targ_key)].copy()
            # remove old key/value pair
            self.working_data.pop(str(targ_key))
            # cache new row entry as target row
            last_edited = self.working_data[str(new_value)]
        else:
            # cache existing row entry at target row
            last_edited = self.working_data[str(targ_key)]

        # update target cell with new value
        last_edited[str(targ_col)] = new_value

        # cache last edited row's serial number
        self.last_edited_Row_Serial = list(last_edited.items())[0][1]

        print('New scans: ', self.window().scans)

    @QtCore.pyqtSlot()
    def save_changes(self):
        '''Save table changes to runtime scans dict'''
        if self.working_data != None:
            # check for any blank rows
            for key in self.working_data:
                # if found blank row, delete it
                if key == None or len(self.working_data[key].values()) == 0:
                    del self.working_data[key]

            # copy working data w changes over to runtime dict      
            self.window().scans = deepcopy(self.working_data)
            self.window().write_scans()
            self.populate(True) # refresh table
            print("Table changes saved!")

    @QtCore.pyqtSlot()
    def try_save_changes(self):
        '''Show confirmation popup before saving changes'''
        Popup("Would you like to save any changes?", 
              "Confirm Save", 
              True,
              on_accept=lambda: self.save_changes(),
              on_reject=None)
        
    @QtCore.pyqtSlot()
    def reset_table(self):
        '''Resets the table to original values'''
        Popup("Do you want to reset all changes to last save?", 
                "Confirm Reset",
                True, 
                on_accept=lambda: self.populate(True), 
                on_reject=None, 
                parent=self)
    
    @QtCore.pyqtSlot()
    def add_row(self):
        '''Add an empty scan table row'''
        self.insertRow(self.rowCount())


    def del_last_edited_row(self):
        '''Deletes the last edited row from table'''
        #target = self.findItems(self.last_edited_Row_Serial)
        #print("Delete target: " + target)
        del self.working_data[self.last_edited_Row_Serial]
        self.populate()

    @QtCore.pyqtSlot()
    def try_del_last_edited_row(self):
        '''Show confirmation  pop-up for deleted last edited row'''
        if self.last_edited_Row_Serial == None:
            # TODO show ok menu notifying to edit a row first
            pass
        
        Popup("Would you like to delete the last edited row?\nSerial Number: " + self.last_edited_Row_Serial, 
              "Confirm Delete Row", 
              True,
              on_accept=lambda: self.del_last_edited_row(),
              on_reject=None)
        

    def try_find_scan_column(self, index: int) -> str:
        '''
        Try to find a scan column name in table data at passed index.
        Basically, find row serialnumber by row position in table.
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
        return None;            

