import datetime
from tkinter import *

from customs import *

from business.usecases import (RetrieveAllUsersUsecase,
                               SaveNewUserUsecase, GetDelvronAdminUsecase,
                               QuitUserUsecase)
from business.models import Role

from persistence.repository import UserAdminRepositoryImpl, UsersRepositoryImpl
from persistence.dao import UsersDaoImpl, UserAdminDaoImpl
from constants import BUTTON_EVENT, NO_DATA_INPUT_ERROR, TREEVIEW_SELECT_EVENT

from tkinter import messagebox

from views.employee_administration.employee_administration_form_contract import EmployeeAdministrationFormContract
from views.employee_administration.employee_administration_form_presenter import EmployeeAdministrationFormPresenter


class UserManageForm(Frame, EmployeeAdministrationFormContract.View):

    def show_admin(self, _admins):
        """Handle all cases when admin is received"""
        if _admins:
            self._admin = _admins[0]

    def show_users(self, users):
        self._tv_umf_users.delete(*self._tv_umf_users.get_children())
        self._users = {self._tv_umf_users.insert('', END, values=(user.id, user.name, user.position, user.start_date, user.quit_date)): user for user in users}

    def show_quit_user_completed(self, user_count):
        if user_count > 0:
            self._btn_umf_employee_quit.grid_forget()
            self._e_umf_employee_name.delete(0, END)
            self._presenter.on_load_users()

    def show_save_user_completed(self, user_id):
        if user_id >= 0:
            self._e_umf_employee_name.delete(0, END)
            self._cb_umf_employee_position.current(0)
            self._btn_umf_employee_save['text'] = 'ADD'
            self._btn_umf_employee_quit.grid_forget()
            self._presenter.on_load_users()

    def show_save_user_error(self, e):
        if e.args[0] == NO_DATA_INPUT_ERROR:
            messagebox.showerror("Save Failed", "Data is Empty")

    def __init__(self, master, _db, _admin_id):
        Frame.__init__(self, master)
        print("UserAdminForm : User Admin Form Toplevel is initiated")
        self._users_repo = UsersRepositoryImpl(UsersDaoImpl(_db))
        self._user_admins_repo = UserAdminRepositoryImpl(UserAdminDaoImpl(_db))
        self._presenter = EmployeeAdministrationFormPresenter(
            _mView=self, _retrieve_all_users_usecase=RetrieveAllUsersUsecase(self._users_repo),
            _get_delvron_admin_usecase=GetDelvronAdminUsecase(self._user_admins_repo),
            _quit_user_usecase=QuitUserUsecase(self._users_repo),
            _save_new_user_usecase=SaveNewUserUsecase(self._users_repo)
        )

        self._lf_umf_employee_info = LabelFrame(self, text='EMPLOYEE INFO')
        self._e_umf_employee_name = Entry(self._lf_umf_employee_info)
        self._cb_umf_employee_position = ttk.Combobox(self._lf_umf_employee_info, state='readonly', values=Role.values(), width=20)
        self._btn_umf_employee_save = Button(self._lf_umf_employee_info, text='ADD')
        self._btn_umf_employee_quit = Button(self._lf_umf_employee_info, text='QUIT')
        self._sc_users = ttk.Scrollbar(self, orient=VERTICAL)
        self._tv_umf_users = ttk.Treeview(self, show="headings", height=20, yscrollcommand=self._sc_users.set)
        self._tv_umf_users['columns'] = ('ID', 'NAME', 'POSITION', 'START DATE', 'QUIT DATE')

        self._tv_umf_users.heading('#1', text='Id')
        self._tv_umf_users.heading('#2', text='Name')
        self._tv_umf_users.heading('#3', text='Position')
        self._tv_umf_users.heading('#4', text='Start Date')
        self._tv_umf_users.heading('#5', text='Quit Date')

        self._tv_umf_users.column('#1', width=50, stretch=YES, minwidth=50, anchor=E)
        self._tv_umf_users.column('#2', width=250, stretch=YES, minwidth=250, anchor=W)
        self._tv_umf_users.column('#3', width=250, stretch=YES, minwidth=250, anchor=W)
        self._tv_umf_users.column('#4', width=200, stretch=YES, minwidth=200, anchor=W)
        self._tv_umf_users.column('#5', width=200, stretch=YES, minwidth=200, anchor=W)

        self._create_views(master)
        self._bind_events()

        self._presenter.on_load_users()
        self._presenter.on_load_admin(_admin_id)

    def _create_views(self, master):
        self._sc_users.configure(command=self._tv_umf_users.yview)

        self._tv_umf_users.pack(fill=BOTH, expand=True, side=LEFT)
        self._sc_users.pack(fill=BOTH, side=LEFT)
        self._lf_umf_employee_info.pack(fill=BOTH, expand=True, side=RIGHT)

        Label(self._lf_umf_employee_info, text="Name").grid(row=0, column=0, sticky=W, padx=10, pady=10)
        self._e_umf_employee_name.grid(row=0, column=1, sticky=W, padx=10, pady=10)
        Label(self._lf_umf_employee_info, text="Position").grid(row=1, column=0, sticky=W, padx=10, pady=10)
        self._cb_umf_employee_position.grid(row=1, column=1, sticky=W, padx=10, pady=10)
        self._btn_umf_employee_save.grid(row=2, column=1, sticky=W, padx=10, pady=10)

    def _bind_events(self):
        self._btn_umf_employee_save.bind(BUTTON_EVENT, self._click_user_save_event)
        self._tv_umf_users.bind(TREEVIEW_SELECT_EVENT, self._selection_users_event)

    def _selection_users_event(self, event):

        _user = self._users.get(event.widget.focus())
        if _user:
            self._e_umf_employee_name.delete(0, END)
            self._cb_umf_employee_position.set("")

            self._e_umf_employee_name.insert(0, _user.name)
            self._cb_umf_employee_position.set(_user.position)

            self._btn_umf_employee_save['text'] = 'UPDATE'
            if _user.quit_date == '':
                self._btn_umf_employee_quit.grid(row=2, column=0, sticky=W, padx=10, pady=10)
                self._btn_umf_employee_quit.bind(BUTTON_EVENT, self._btn_umf_employee_quit_click_event)

    def _btn_umf_employee_quit_click_event(self, event):
        _user = self._users.get(self._tv_umf_users.focus())
        _user.quit_date = datetime.datetime.now()
        self._users[self._tv_umf_users.focus()] = _user
        self._presenter.on_quit_user_click(_user.id, datetime.datetime.now())

    def _click_user_save_event(self, event):
        _user = self._users.get(self._tv_umf_users.focus())
        self._presenter.on_save_new_user_click(_user.id if _user else _user, self._e_umf_employee_name.get(),
                              self._cb_umf_employee_position.get(), '', _user.quit_date if _user else '')