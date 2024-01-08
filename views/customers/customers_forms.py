from tkinter import *

from customs import *

from business.usecases import (UpdateCustomerUsecase, CreateCustomerUsecase, DisplayCustomersUsecase,
                               remove_customer_usecase, GetDelvronAdminUsecase, DisplayAllUnpaidOffSaleIdUsecase)
from business.models import Access, CustomerType

from constants import NO_DATA_INPUT_ERROR, BUTTON_EVENT, TREEVIEW_SELECT_EVENT, RETURN_EVENT, PHONE_NUMBER_ERROR, RESTRICTION_CHAR_ERROR, SAVE_ERROR_MESSAGE_TITLE, SAVE_ERROR_RESTRICTION_CHAR_MESSAGE, SAVE_ERROR_PHONE_NUMBER_MESSAGE, NO_DATA_INPUT_ERROR_MESSAGE

from tkinter import messagebox

import customtkinter as ctk

from persistence.repository import CustomersRepositoryImpl, UserAdminRepositoryImpl, ReceiptsRepositoryImpl
from persistence.dao import UserAdminDaoImpl, ReceiptsDaoImpl, CustomersDaoImpl

from views.customers.customers_form_presenter import CustomersFormPresenter
from views.customers.customers_form_contract import CustomersFormContract


class CustomersManageForm(Frame, CustomersFormContract.View):

    def show_admin(self, _admins):
        if _admins:
            self._admin = _admins[0]
            if self._admin.company_access == Access.DELETE.value:
                self.btn_delete = ttk.Button(self, text='Delete')

            if self._admin.company_access in [Access.ALL.value, Access.READPUT.value, Access.READPUSH.value,
                                              Access.DELETE.value]:

                Label(self.lf_customer_info, text='CUSTOMER CODE').grid(row=0, column=0, sticky='nsew', padx=10, pady=10)
                self.e_ccode.grid(row=0, column=1, sticky=NSEW, padx=10, pady=10)
                self.e_ccode.focus()
                Label(self.lf_customer_info, text='CUSTOMER NAME').grid(row=1, column=0, sticky='nsew', padx=10, pady=10)
                self.e_cname.grid(row=1, column=1, sticky=NSEW, padx=10, pady=10)
                Label(self.lf_customer_info, text='ADDRESS').grid(row=2, column=0, sticky=NSEW, padx=10, pady=10)
                self.e_c_address.grid(row=2, column=1, sticky=NSEW, padx=10, pady=10)
                Label(self.lf_customer_info, text='CUSTOMER CONTACT').grid(row=3, column=0, sticky=NSEW, padx=10, pady=10)
                self.e_c_phno.grid(row=3, column=1, sticky=NSEW, padx=10, pady=10)
                Label(self.lf_customer_info, text='MACHINE SERIAL NO').grid(row=4, column=0, sticky=NSEW, padx=10, pady=10)
                self.e_c_serial_no.grid(row=4, column=1, sticky=NSEW, padx=10, pady=10)
                Label(self.lf_customer_info, text='INSTALLED DATE').grid(row=5, column=0, sticky=NSEW, padx=10, pady=10)
                self.e_c_installed_date.grid(row=5, column=1, sticky=NSEW, padx=10, pady=10)
                Label(self.lf_customer_info, text='CUSTOMER TYPE').grid(row=6, column=0, sticky=NSEW, padx=10, pady=10)
                self._cb_cmf_customer_type.grid(row=6, column=1, sticky=NSEW, padx=10, pady=10)
                self.btn_save.grid(row=7, column=1, padx=10, pady=10)
                self.lf_customer_info.pack(side=RIGHT, fill=Y, padx=10, pady=10, ipadx=5, ipady=5)

            self.btn_save.bind(BUTTON_EVENT,
                               self._update_customer_event if self._admin.company_access == Access.READPUT.value else (
                                   self._add_customer_event if self._admin.company_access == Access.READPUSH.value else
                                   self._save_customer_event))

            if self._admin.company_access in [Access.ALL.value, Access.READPUT.value, Access.DELETE.value]:
                self._tv_customers.bind(TREEVIEW_SELECT_EVENT, self._selection_customer_event)

            if self._admin.company_access == Access.DELETE.value:
                self.btn_delete.bind(BUTTON_EVENT, self._delete_customer_event)

    def _next_customer_deleted_state(self, _company_count):
        self.btn_new.unbind(BUTTON_EVENT)
        self.btn_new.grid_forget()
        self.btn_delete.grid_forget()
        self.e_cname.delete(0, END)
        self.e_c_phno.delete(0, END)
        self.e_c_address.delete(0, END)
        self.e_c_serial_no.delete(0, END)
        self.e_c_installed_date.delete(0, END)
        self.ckb_deactivate.grid_forget()

        self._presenter.on_load_customers(None, None)

    def show_customers(self, companies):
        companies.reverse()
        self._tv_customers.delete(*self._tv_customers.get_children())
        self.customers = {self._tv_customers.insert('', END, values=(company.id, company.name, company.address,
                                                                     company.phno, company.serial_no,
                                                                     company.installed_date, company.customer_type)):
                                                                        company for company in companies}

    def show_customer_update_completed(self, updated_count):

        if updated_count > 0:
            self.e_ccode.delete(0, END)
            self.e_cname.delete(0, END)
            self.e_c_phno.delete(0, END)
            self.e_c_address.delete(0, END)
            self.e_c_serial_no.delete(0, END)
            self.e_c_installed_date.delete(0, END)
            self.ckb_deactivated_var.set(False)

            self._presenter.on_load_customers(None, None)

            self.btn_new.unbind(BUTTON_EVENT)
            self.btn_new.grid_forget()
            self.ckb_deactivate.grid_forget()

    def show_customer_update_error(self, e):
        if e.args[0] == NO_DATA_INPUT_ERROR:
            messagebox.showerror(SAVE_ERROR_MESSAGE_TITLE, NO_DATA_INPUT_ERROR_MESSAGE)
        elif e.args[0] == PHONE_NUMBER_ERROR:
            messagebox.showerror(SAVE_ERROR_MESSAGE_TITLE, SAVE_ERROR_PHONE_NUMBER_MESSAGE)
        elif e.args[0] == RESTRICTION_CHAR_ERROR:
            messagebox.showerror(SAVE_ERROR_MESSAGE_TITLE, SAVE_ERROR_RESTRICTION_CHAR_MESSAGE)
        else:
            messagebox.showerror(SAVE_ERROR_MESSAGE_TITLE, e.args[0])

    def show_customer_add_completed(self):
        """State that company addition procedure is completed"""
        self.e_ccode.delete(0, END)
        self.e_cname.delete(0, END)
        self.e_c_phno.delete(0, END)
        self.e_c_address.delete(0, END)
        self.e_c_serial_no.delete(0, END)
        self.e_c_installed_date.delete(0, END)
        self.ckb_deactivated_var.set(False)
        self.btn_new.grid_forget()

        self._presenter.on_load_customers(None, None)

    def show_customer_add_error(self, e):
        if e.args[0] == NO_DATA_INPUT_ERROR:
            messagebox.showerror(SAVE_ERROR_MESSAGE_TITLE, NO_DATA_INPUT_ERROR_MESSAGE)
        elif e.args[0] == PHONE_NUMBER_ERROR:
            messagebox.showerror(SAVE_ERROR_MESSAGE_TITLE, SAVE_ERROR_PHONE_NUMBER_MESSAGE)
        else:
            messagebox.showerror(SAVE_ERROR_MESSAGE_TITLE, e.args[0])

    def __init__(self, _master, _db, _admin_id):
        Frame.__init__(self, _master)
        print("CustomerEditForm : Customer Edit Form Toplevel is initiated")
        # self._customer_edit_access = _customer_edit_access
        self._admin_id = _admin_id
        self._user_admins_repo = UserAdminRepositoryImpl(UserAdminDaoImpl(_db))
        self._customer_repo = CustomersRepositoryImpl(CustomersDaoImpl(_db))
        self._presenter = CustomersFormPresenter(
            _mView=self, _get_delvron_admin_usecase=GetDelvronAdminUsecase(self._user_admins_repo),
            _display_customers_usecase=DisplayCustomersUsecase(self._customer_repo),
            _update_customer_usecase=UpdateCustomerUsecase(self._customer_repo),
            _create_customer_usecase=CreateCustomerUsecase(self._customer_repo)
        )

        self.lf_customer_info = LabelFrame(self, text='CUSTOMER INFO')
        self.e_ccode = Entry(self.lf_customer_info)
        self.e_cname = Entry(self.lf_customer_info)
        self.e_c_address = Entry(self.lf_customer_info)
        self.e_c_phno = Entry(self.lf_customer_info)
        self.e_c_serial_no = Entry(self.lf_customer_info)
        self.e_c_installed_date = Entry(self.lf_customer_info)
        self._cb_cmf_customer_type = ttk.Combobox(self.lf_customer_info, state='readonly', values=CustomerType.values())
        self._cb_cmf_customer_type.current(0)
        self.ckb_deactivated_var = BooleanVar()
        self.ckb_deactivate = Checkbutton(self.lf_customer_info, text="Deactivated", variable=self.ckb_deactivated_var)
        self.btn_new = ttk.Button(self.lf_customer_info, text='New')
        self.btn_save = ttk.Button(self.lf_customer_info, text='Save')

        self._tv_customers = ttk.Treeview(self, show="headings", selectmode=BROWSE)
        self._sc_companies = ttk.Scrollbar(self, orient=VERTICAL, command=self._tv_customers.yview)
        self.create_views(_admin_id)
        self._bind_events(_admin_id)
        self._presenter.on_load_admin(_admin_id)
        self._presenter.on_load_customers(None, None)

    def create_views(self, _admin_id):
        """Show all initial views on toplevel"""

        self._tv_customers['columns'] = ('CODE', 'COMPANY NAME', 'ADDRESS', 'CONTACT', 'MACHINE SERIAL NO',
                                        'INSTALLED DATE', 'CUSTOMER_TYPE')

        self._tv_customers.column('#1', width=100, stretch=YES, anchor=W, minwidth=100)
        self._tv_customers.column('#2', width=250, stretch=YES, anchor=W, minwidth=250)
        self._tv_customers.column('#3', width=250, stretch=YES, anchor=W, minwidth=250)
        self._tv_customers.column('#4', width=100, stretch=YES, anchor=E, minwidth=100)
        self._tv_customers.column('#5', width=150, stretch=YES, anchor=E, minwidth=150)
        self._tv_customers.column('#6', width=150, stretch=YES, anchor=W, minwidth=150)
        self._tv_customers.column('#7', width=150, stretch=YES, anchor=W, minwidth=150)

        self._tv_customers.heading('#1', text='CODE')
        self._tv_customers.heading('#2', text='CUSTOMER NAME')
        self._tv_customers.heading('#3', text='ADDRESS')
        self._tv_customers.heading('#4', text='CONTACT')
        self._tv_customers.heading('#5', text='MACHINE SERIAL NO')
        self._tv_customers.heading('#6', text='INSTALLED DATE')
        self._tv_customers.heading('#7', text='CUSTOMER TYPE')
        self._tv_customers.configure(yscrollcommand=self._sc_companies.set)
        # self._tv_customers.grid(row=8, column=0, columnspan=4, padx=10, pady=10, sticky="NSE")
        # self._sc_companies.grid(row=8, column=0, columnspan=4, padx=10, pady=10, sticky="NSE")
        self._tv_customers.pack(side=LEFT, fill=Y, padx=10, pady=10)
        self._sc_companies.pack(side=LEFT, fill=Y, padx=10, pady=10)

        self.update()

    def _bind_events(self, _admin_id):
        """Bind all initial events to relevant widgets"""

        self.e_ccode.bind(RETURN_EVENT, lambda e: e.widget.tk_focusNext().focus_set())
        self.e_cname.bind(RETURN_EVENT, lambda e: e.widget.tk_focusNext().focus_set())
        self.e_c_phno.bind(RETURN_EVENT, lambda e: e.widget.tk_focusNext().focus_set())
        self.e_c_address.bind(RETURN_EVENT, lambda e: e.widget.tk_focusNext().focus_set())
        self.e_c_serial_no.bind(RETURN_EVENT, lambda e: e.widget.tk_focusNext().focus_set())
        self.e_c_installed_date.bind(RETURN_EVENT, lambda e: e.widget.tk_focusNext().focus_set())

    def _save_customer_event(self, event):
        """Insert new company clicking add button"""
        _customer = self.customers.get(self._tv_customers.focus())
        if _customer:
            self._presenter.on_update_customer(self.e_ccode.get(), self.e_cname.get(), self.e_c_address.get(),
                                     self.e_c_phno.get(), self.e_c_serial_no.get(), self.e_c_installed_date.get(),
                                     self.ckb_deactivated_var.get() if _customer else False, self._cb_cmf_customer_type.get(),
                                     _customer.id)

        else:
            self._presenter.on_create_customer(self.e_ccode.get(), self.e_cname.get(), self.e_c_address.get(),
                                     self.e_c_phno.get(), self.e_c_serial_no.get(), self.e_c_installed_date.get(),
                                     self.ckb_deactivated_var.get() if _customer else False,
                                     self._cb_cmf_customer_type.get())

    def _update_customer_event(self, event):
        _customer = self.customers.get(self._tv_customers.focus())
        if _customer:
            self._presenter.on_update_customer(self.e_ccode.get(), self.e_cname.get(), self.e_c_address.get(),
                                     self.e_c_phno.get(), self.e_c_serial_no.get(), self.e_c_installed_date.get(),
                                     self.ckb_deactivated_var.get() if _customer else False, self._cb_cmf_customer_type.get(),
                                     _customer.id)

    def _add_customer_event(self, event):
        self._presenter.on_create_customer(self.e_ccode.get(), self.e_cname.get(), self.e_c_address.get(),
                                 self.e_c_phno.get(), self.e_c_serial_no.get(), self.e_c_installed_date.get(),
                                 False, self._cb_cmf_customer_type.get())

    def _delete_customer_event(self, event):
        # todo need to reconsider whether it should be deleted
        _customer_id = self.customers.get(self._tv_customers.focus()).id
        remove_customer_usecase(self._customer_repo, _customer_id).subscribe(on_next=self._next_customer_deleted_state)

    def _selection_customer_event(self, event):
        """Select a company to edit or delete"""

        if event.widget.focus() != "":

            # if self._admin.company_access in [Access.READPUSH.value, Access.ALL.value]:
            #     self.btn_new.grid(row=7, column=1, padx=10, pady=10, sticky=W)
            #     self.btn_new.bind(BUTTON_EVENT, self._new_form_refresh_event)
            self.ckb_deactivate.grid(row=5, column=2, padx=10, pady=10, sticky=W)
            if self._admin.company_access == Access.DELETE.value:
                self.btn_delete.grid(row=7, column=1, padx=10, pady=10, sticky=E)

            self.e_ccode.delete(0, END)
            self.e_cname.delete(0, END)
            self.e_c_phno.delete(0, END)
            self.e_c_address.delete(0, END)
            self.e_c_serial_no.delete(0, END)
            self.e_c_installed_date.delete(0, END)
            self.ckb_deactivated_var.set(False)
            _customer = self.customers.get(event.widget.focus())
            self.e_ccode.insert(END, _customer.id)
            self.e_cname.insert(END, _customer.name)
            self.e_c_address.insert(END, _customer.address)
            self.e_c_phno.insert(END, _customer.phno)
            self.e_c_serial_no.insert(END, _customer.serial_no)
            self.e_c_installed_date.insert(END, _customer.installed_date)
            self._cb_cmf_customer_type.set(_customer.customer_type)
            self.ckb_deactivated_var.set(_customer.deactivated)

    def _new_form_refresh_event(self, event):
        self.btn_new.unbind(BUTTON_EVENT)
        self.btn_new.grid_forget()
        self.ckb_deactivate.grid_forget()

        self.e_ccode.delete(0, END)
        self.e_cname.delete(0, END)
        self.e_c_phno.delete(0, END)
        self.e_c_address.delete(0, END)
        self.e_c_serial_no.delete(0, END)
        self.e_c_installed_date.delete(0, END)
        self.e_cname.focus_set()
        self._tv_customers.selection_remove(self._tv_customers.focus())
        self._tv_customers.focus("")


class ItemsListForm(Toplevel):

    def _next_items_retrieval_state(self, _items):
        self.tv_selection_items.delete(*self.tv_selection_items.get_children())
        if self._flag_label == 'Companies':
            self._items = {self.tv_selection_items.insert('', END, values=(_default_item.id, _default_item.name,)): _default_item for _default_item in self._default_items} if self._default_items else {}
            self._items.update({self.tv_selection_items.insert('', END, values=(_item.id, _item.name,)): _item for _item in _items})
        else:
            self._items = {self.tv_selection_items.insert('', END, values=(_default_item)): _default_item for _default_item in self._default_items} if self._default_items else {}
            self._items.update(
                {self.tv_selection_items.insert('', END, values=(_item)): _item for _item in _items})

    def _on_e_code_change(self, *args):
        (DisplayCustomersUsecase(self._repo)(self.e_ccode_var.get(), self.e_ccode_var.get()) if self._flag_label == 'Companies' else (DisplayAllUnpaidOffSaleIdUsecase(self._repo)(self._customer_id, self.e_ccode_var.get() if self.e_ccode_var.get() != '' else '%'))).subscribe(
                                                    on_next=self._next_items_retrieval_state)
        print(self.e_ccode_var.get())

    def __init__(self, master, db, _select_item, x_pos, y_pos, _default_items=None, flag_label='Companies', _customer_id=None):
        Toplevel.__init__(self)
        self._flag_label = flag_label
        self.wm_title(f"Search {flag_label}")
        self.grid_anchor(CENTER)
        self.wm_transient(master)
        self.wm_maxsize(width=300, height=300)
        self.wm_minsize(width=300, height=300)
        self.wm_geometry(f'300x300+{x_pos}+{y_pos}')
        self.grab_set()

        self.db = db
        self._select_item = _select_item
        self._default_items = _default_items
        self._customer_id = _customer_id
        self._repo = CustomersRepositoryImpl(CustomersDaoImpl(db)) if flag_label == 'Companies' else ReceiptsRepositoryImpl(ReceiptsDaoImpl(db))

        self.e_ccode_var = StringVar()
        self.e_ccode_var.trace('w', self._on_e_code_change)
        self.e_ccode = ctk.CTkEntry(self, placeholder_text='Search by Code', textvariable=self.e_ccode_var)

        self.tv_selection_items = ttk.Treeview(self, show="", selectmode=BROWSE, height=10, )
        self.sc_items = ttk.Scrollbar(self, orient=VERTICAL, command=self.tv_selection_items.yview)
        self.tv_selection_items.configure(yscrollcommand=self.sc_items.set)
        self.tv_selection_items['columns'] = ('Company Codes', 'Company Names') if flag_label == 'Companies' else ('Sale Id')

        if flag_label == 'Companies':
            self.tv_selection_items.column('#1', width=50, stretch=YES, anchor=CENTER, minwidth=50)
            self.tv_selection_items.column('#2', width=100, stretch=YES, anchor=W, minwidth=100)
            self.tv_selection_items.heading('#1', text='Company Code')
            self.tv_selection_items.heading('#2', text='Company Names')
        else:
            self.tv_selection_items.column('#1', width=100, stretch=YES, anchor=W, minwidth=100)
            self.tv_selection_items.heading('#1', text='Sale Id')

        self._create_views()
        self._bind_events()

        (DisplayCustomersUsecase(self._repo)(None, None) if flag_label == 'Companies' else DisplayAllUnpaidOffSaleIdUsecase(self._repo)(self._customer_id, '%')).subscribe(on_next=self._next_items_retrieval_state)

    def _create_views(self):
        """Show all initial views on toplevel"""
        self.e_ccode.pack(fill=X)
        self.sc_items.pack(fill=Y, side=RIGHT)
        self.tv_selection_items.pack(fill=X, expand=TRUE, side=RIGHT)
        self.tv_selection_items.focus_set()

    def _bind_events(self):
        """Bind all initial events to relevant widgets"""
        self.protocol("WM_DELETE_WINDOW", lambda: self._close_window())
        self.tv_selection_items.bind(TREEVIEW_SELECT_EVENT, self._selection_company_event)

    def _selection_company_event(self, event):
        print(f"CompaniesListForm : {event.widget.focus()} in treeview is selected")
        self._select_item(self._items.get(event.widget.focus()))
        self.destroy()

    def _close_window(self):
        self._select_item(None)
        self.destroy()
