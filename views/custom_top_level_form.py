from tkinter import *

from tkinter import messagebox

from views.pin_login.pin_login_form import PinLoginForm
from views.customers.customers_forms import CustomersManageForm
from views.items_manage.items_manage_form import ItemsManageForm
from views.employee_administration.employee_adminstration_form import UserManageForm
from views.preferences_manage.preferences_manage_form import PreferencesManageForm
from views.receipts_manage.receipts_manage_form import ReceiptsManageForm

from constants import CUSTOMERS_FORM, ITEMS_FORM, RECEIPTS_FORM, EMPLOYEES_FORM, PREFERENCES_FORM, WRONG_PASSWORD_ERROR, WRONG_PASSWORD_ERROR_MESSAGE, BG_COLOR


class CustomToplevelForm(Toplevel):

    def __init__(self, _master, _root_x, _root_y, _db, _admin_id, _type):
        Toplevel.__init__(self, bg=BG_COLOR)
        self._db = _db
        self._admin_id = _admin_id
        self._type = _type
        self._create_views(_master, _root_x, _root_y)

        self._f_pin_login_form = PinLoginForm(self, self._db, _admin_id, self._login_succeed_event, self._login_error_event)
        self._f_pin_login_form.pack(side=TOP, anchor=CENTER, expand=True, padx=10, pady=10)

        self.wm_minsize(width=self.winfo_width(), height=self.winfo_height())

    def _create_views(self, _master, _root_x, _root_y):
        self.wm_title(self._type)
        self.grid_anchor(CENTER)
        self.wm_geometry(f'+{_root_x}+{_root_y}')
        self.wm_transient(_master)
        self.grab_set()

    def _login_succeed_event(self):
        self._f_pin_login_form.pack_forget()
        self._f_pin_login_form.hide_widgets()

        if self._type == CUSTOMERS_FORM:
            self._f_customers_form = CustomersManageForm(self, self._db, self._admin_id)
            self._f_customers_form.pack(side=TOP, anchor=CENTER, expand=True, padx=10, pady=10)
        elif self._type == ITEMS_FORM:
            self._f_items_form = ItemsManageForm(self, self._db)
            self._f_items_form.pack(side=TOP, anchor=CENTER, expand=True, padx=10, pady=10)
        elif self._type == RECEIPTS_FORM:
            self._f_receipts_form = ReceiptsManageForm(self, self._db)
            self._f_receipts_form.pack(fill=BOTH, expand=True, padx=10, pady=10)
        elif self._type == EMPLOYEES_FORM:
            self._f_employees_form = UserManageForm(self, self._db, self._admin_id)
            self._f_employees_form.pack(side=TOP, anchor=CENTER, expand=True, padx=10, pady=10)
        elif self._type == PREFERENCES_FORM:
            self._f_preferences_form = PreferencesManageForm(self, self._db, self._admin_id)
            self._f_preferences_form.pack(side=TOP, anchor=CENTER, expand=True, padx=10, pady=10)

    def _login_error_event(self):
        messagebox.showerror(WRONG_PASSWORD_ERROR, WRONG_PASSWORD_ERROR_MESSAGE)

