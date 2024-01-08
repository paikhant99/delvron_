from tkinter import *
from customs import *

from business.usecases import GetDelvronAdminUsecase, UpdateDelvronCompanyAccessUsecase, RetrieveLastSaleId, UpdateDelvronSaleIdUsecase, UpdateDelvronAdminPasswordUsecase
from business.models import Access

from persistence.repository import SalesRepositoryImpl, UserAdminRepositoryImpl
from persistence.dao import UserAdminDaoImpl, SalesDaoImpl

from constants import COMBO_EVENT, BUTTON_EVENT

from views.preferences_manage.preferences_manage_form_presenter import PreferencesManageFormPresenter
from views.preferences_manage.preferences_manage_form_contract import PreferencesManageFormContract


class PreferencesManageForm(Frame, PreferencesManageFormContract.View):

    def show_password_update_completed(self, _admin_id):
        self._presenter.on_load_admin(_admin_id)

    def show_sale_id_update_completed(self, row_count):
        self._presenter.on_load_admin(self._admin.id)

    def show_company_access(self, update_count):
        """Handles all cases when company access is updated"""
        if update_count > 0:
            self._presenter.on_load_admin(self._admin.id)

    def show_admin(self, _admins):
        """Handles all cases when admin is received"""
        if _admins:
            self._admin = _admins[0]
            self.cb_company_access.set(_admins[0].company_access)
            self._e_password.delete(0, END)
            self._e_password.insert(END, self._admin.pwd)
            if self._admin.order_id == 0:
                self.e_start_id.delete(0, END)
                self.e_start_id.insert(END, str(int(self.start_id) + 1))
            else:
                self.e_start_id.delete(0, END)
                self.e_start_id.insert(END, self._admin.order_id)

    def __init__(self, master, _db, _admin_id):
        Frame.__init__(self, master)
        print("Settings : Settings Top level is initiated")

        self._user_admins_repo = UserAdminRepositoryImpl(UserAdminDaoImpl(_db))
        self._sale_repo = SalesRepositoryImpl(SalesDaoImpl(_db))
        self._presenter = PreferencesManageFormPresenter(
            _mView=self, _get_delvron_admin_usecase=GetDelvronAdminUsecase(self._user_admins_repo),
            _update_delvron_company_access_usecase=UpdateDelvronCompanyAccessUsecase(self._user_admins_repo),
            _update_delvron_sale_id_usecase=UpdateDelvronSaleIdUsecase(self._user_admins_repo),
            _update_delvron_admin_password_usecase=UpdateDelvronAdminPasswordUsecase(self._user_admins_repo)
        )

        self._f_company_permission = Frame(self)

        self.cb_company_access = ttk.Combobox(self._f_company_permission, values=Access.values(), state="readonly")

        self._lf_last_sale_id = LabelFrame(self, text="LAST SALE")
        self.e_start_id = Entry(self._lf_last_sale_id)
        self._lf_password = LabelFrame(self, text="PASSWORD CHANGE")
        self._e_password = Entry(self._lf_password)
        self._btn_password_change = Button(self._lf_password, text="CHANGE")

        self._create_views()
        self._bind_events()

        self.start_id = int(RetrieveLastSaleId()(self._sale_repo))
        self._presenter.on_load_admin(_admin_id)

    def _create_views(self):
        """Show all initial views on toplevel"""

        Label(self._f_company_permission, text="Company Permission").grid(row=0, column=0, padx=10, pady=10)
        self.cb_company_access.grid(row=0, column=1, padx=10, pady=10)
        self._f_company_permission.pack(fill=BOTH, expand=True)

        Label(self._lf_last_sale_id, text="Start Id").grid(row=0, column=0, padx=5, pady=5)
        self.e_start_id.grid(row=0, column=1, padx=5, pady=5)
        Button(self._lf_last_sale_id, text="Insert", command=self._btn_last_sale_id_click_event).grid(row=1, column=0, columnspan=2, padx=5, pady=5)
        self._lf_last_sale_id.pack(fill=BOTH, expand=True)

        self._e_password.pack(side=LEFT, padx=10, pady=10)
        self._btn_password_change.pack(side=RIGHT, padx=10, pady=10)
        self._lf_password.pack(fill=BOTH, expand=True, padx=10, pady=10)

    def _bind_events(self):
        """Bind all initial events to relevant widgets"""
        self.cb_company_access.bind(COMBO_EVENT, self._selection_company_permission_event)
        self._btn_password_change.bind(BUTTON_EVENT, self._btn_password_change_event)

    def _selection_company_permission_event(self, event):
        """Handles all cases when combobox is selected"""
        print("Settings : Combobox is selected")

        self._presenter.on_update_company_access(event.widget.get())

    def _btn_last_sale_id_click_event(self):
        if self.e_start_id.get().isnumeric() and int(self.e_start_id.get()) > self.start_id:
            self._presenter.on_update_last_sale_id_btn_click(int(self.e_start_id.get()))

    def _btn_password_change_event(self, event):
        self._presenter.on_update_admin_password_btn_click(self._admin.id, self._e_password.get())
