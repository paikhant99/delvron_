from tkinter import *

from constants import BUTTON_EVENT, RETURN_EVENT

from business.usecases import GetDelvronAdminUsecase

from persistence.repository import UserAdminRepositoryImpl
from persistence.dao import UserAdminDaoImpl

from views.pin_login.pin_login_form_contract import PinLoginFormContract
from views.pin_login.pin_login_form_presenter import PinLoginFormPresenter


class PinLoginForm(Frame, PinLoginFormContract.View):

    def show_admin(self, admins):
        self._password = admins[0].pwd

    def __init__(self, _master, _db, _admin_id, _login_succeed_event, _login_error_event):
        Frame.__init__(self, _master, bg="red")
        self._user_admins_repo = UserAdminRepositoryImpl(UserAdminDaoImpl(_db))
        self._presenter = PinLoginFormPresenter(_mView=self, _get_delvron_admin_usecase=GetDelvronAdminUsecase(self._user_admins_repo))
        self._login_succeed_event = _login_succeed_event
        self._login_error_event = _login_error_event
        self._lbl_plf_password = Label(_master, text="Password")
        self._e_plf_password = Entry(_master, show="*")
        self._e_plf_password.focus()
        self._btn_plf_login = Button(_master, text='LOGIN')
        self._create_views()
        self._bind_events()
        self._presenter.on_load_admin(_admin_id)

    def _create_views(self):
        self._lbl_plf_password.pack(padx=10, pady=10)
        self._e_plf_password.pack(padx=10, pady=10)
        self._btn_plf_login.pack(padx=10, pady=10)

    def _bind_events(self):
        self._e_plf_password.bind(RETURN_EVENT, self._plf_login_click_event)
        self._btn_plf_login.bind(BUTTON_EVENT, self._plf_login_click_event)

    def _plf_login_click_event(self, event):
        if self._e_plf_password.get() == self._password:
            self._login_succeed_event()
        else:
            self._login_error_event()

    def hide_widgets(self):
        self._lbl_plf_password.pack_forget()
        self._e_plf_password.pack_forget()
        self._btn_plf_login.pack_forget()

