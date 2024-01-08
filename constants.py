import os
import sys

TITLE = 'DELVRON Myanmar Company Limited'
COMBO_EVENT = '<<ComboboxSelected>>'
DATE_ENTRY_EVENT = "<<DateEntrySelected>>"
RETURN_EVENT = "<Return>"
BUTTON_EVENT = "<Button>"
TREEVIEW_SELECT_EVENT = "<<TreeviewSelect>>"

# Custom
LASTID_EDIT_EVENT = "<<LastIdEdit>>"
PERMISSION_EVENT = "<<PermissionEdit>>"

CUSTOMERS_FORM = "CUSTOMERS FORM"
ITEMS_FORM = "ITEMS FORM"
RECEIPTS_FORM = "RECEIPTS FORM"
EMPLOYEES_FORM = "EMPLOYEES FORM"
PREFERENCES_FORM = "PREFERENCES FORM"

CREATE_LABEL = "CREATE"
UPDATE_LABEL = "UPDATE"
DELIVER_LABEL = "DELIVER"
CANCEL_LABEL = "CANCEL"
QUANTITY_LABEL = "QUANTITY"
VIEW_SUMMARY_LABEL = "VIEW SUMMARY"
VIEW_DETAILS_LABEL = "VIEW DETAILS"
EXPORT_CSV_LABEL = "EXPORT TO CSV"

UNKNOWN_ERROR = "Error: Unknown Error"
NO_DATA_INPUT_ERROR = "Error: Input Error"
PHONE_NUMBER_ERROR = "Error: Wrong Phone Number Format Submitted"
NUMBER_ERROR = "Error: Numeric Error"
RESTRICTION_CHAR_ERROR = "Error: Restriction Character Error"
NO_ORDER_ID_ERROR = "Error: No Order Id Submitted"
NO_DATA_FOUND = "Error: Data Not Found"
EXCEEDED_ERROR = "Error: Entered Amount exceeded than Balance"
DESTROY_EVENT = "<Destroy>"

SAVE_ERROR_MESSAGE_TITLE = "Save Function Failed"
SAVE_ERROR_RESTRICTION_CHAR_MESSAGE = "Some entry contains restricted characters such as \\ "
SAVE_ERROR_PHONE_NUMBER_MESSAGE = "Added Phone number length must be between 9 and 11, Or Check if Phone number contains alphabets"

LOGIN_ERROR_MESSAGE_TITLE = "Login Failed"
LOGIN_ERROR_MESSAGE = "Invalid Username and Password"

SAVE_MESSAGE_TITLE = "Are you sure you want to save?"
SAVE_MESSAGE = "Please Reconfirm Before you Save"

INPUT_NUMBER_ERROR_MESSAGE = "The fields (%s) must be Numeric"
NO_DATA_INPUT_ERROR_MESSAGE = "Empty Input is submitted"

REPEATED_ERROR = "Error: Repeated"
REPEATED_ERROR_MESSAGE = "Chosen Item is repeated"

WRONG_PASSWORD_ERROR = "Error: Wrong Password"
WRONG_PASSWORD_ERROR_MESSAGE = "Wrong Password"

CONFIRMATION_TAG = "CONFIRMATION"
CONFIRMATED_QUESTION = "ARE YOU SURE YOU WANT TO %s ?"

PASSWORD_INVALID_ERROR = "PASSWORD INVALID ERROR"

LABEL_TIME_PERIOD = "FROM \t %s \t TO \t %s"
LABEL_BTN_FILTER = "Customize"
LABEL_CUSTOMER_NAME = "Customer : "
LABEL_PRODUCT_NAME = "Product : "
LABEL_SALESMAN_NAME = "Salesman : "
LABEL_NET_AMOUNT = "Net Amount : \t %s Ks"

LABEL_ORDER_QTY = "Order Qty : \t\t %s"
LABEL_SALES_AMT = "Sales Amount : \t\t %s \tKs"
LABEL_BALANCE = "Balance : \t\t\t %s \tKs"

BG_COLOR = '#d0f0c0'

# Versions

ALPHA_0_01 = "Alpha 0.01"


def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)
