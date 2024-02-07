'''Custom child classes of QT widgets so custom slots can be added'''
from PyQt6 import QtCore, QtWidgets


class PushButton(QtWidgets.QPushButton):
    '''Custom push button'''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class Popup(QtWidgets.QDialog):
    '''Popup dialog box'''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class StackedWidget(QtWidgets.QStackedWidget):
    '''Custom stacked widget'''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class Dialog(QtWidgets.QDialog):
    '''Custom dialog window'''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class Table(QtWidgets.QTableWidget):
    '''Custom table widget'''
    default_headers = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def populate(self, scans: dict(dict())):
        ''' Populates table with values from passed list of dicts'''
        if len(scans) == 0:
            pass
        items = list(scans.values())

        # get number of columns from number of keys in either first or last item
        first_keys = list(items[0].keys())
        last_keys = list(items[-1].keys())

        chosen_keys = first_keys if len(first_keys) > len(last_keys) else last_keys
        # pick whichever item has more columns
        new_len = len(chosen_keys)
        if  new_len == 0:
            pass
        
        ### setup table columns        
        self.clear() # clear table contents and headers
        self.setColumnCount(new_len) # set table column count to new column name

        # iterate thru all columns of first item
        for i in range(new_len):  
            # init header item
            header = QtWidgets.QTableWidgetItem()
            # align text to v center 
            header.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignVCenter) 
            # set text to corresponding column name (key in dict)
            header.setText(chosen_keys[i])
            # place new table widget item on table header
            self.setHorizontalHeaderItem(i, header)

        ### populate rows
        for item_dict in items:
            

