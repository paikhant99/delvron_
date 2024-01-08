from tkinter import *
from customs import *
from tkinter import messagebox

from PIL import Image, ImageTk


from constants import BUTTON_EVENT, LOGIN_ERROR_MESSAGE_TITLE, LOGIN_ERROR_MESSAGE, resource_path

from business.usecases import RetrieveAllAdminsUsecase

from persistence.repository import UserAdminRepositoryImpl
from persistence.dao import UserAdminDaoImpl


class LoginForm(Frame):

    def _next_all_admins_retrieval_state(self, _admins):
        """Handles all cases when admins are received"""
        self._admins = _admins

    def __init__(self, _db, ua_form_login, do_form_login):
        Frame.__init__(self)
        print("LoginForm : Login Form Frame is initiated")
        self._user_admins_repo = UserAdminRepositoryImpl(UserAdminDaoImpl(_db))
        self._ua_form_login = ua_form_login
        self._do_form_login = do_form_login
        # todo change it into presenter method
        RetrieveAllAdminsUsecase()(self._user_admins_repo).subscribe(on_next=self._next_all_admins_retrieval_state)
        # print(os.path.abspath("."))

        photo = ImageTk.PhotoImage(Image.open(resource_path("images/main_banner.png")))
        self._cover_img_label = Label(self, image=photo)
        self._cover_img_label.image = photo
        self.cb_username = ttk.Combobox(self, state='readonly', values=[admin.name for admin in self._admins], width=10)
        # self.e_password = ctk.CTkEntry(self, placeholder_text='Password', width=20, show='*')
        self.btn_login = Button(self, text='Login', bg='#287FE2', width=20, fg='white')

        self._create_views()
        self._bind_events()

    def _create_views(self):
        """Show all initial views on frame"""
        print(self._admins)
        self._cover_img_label.pack(fill=X, anchor=CENTER, expand=True, padx=10, pady=10)
        self.cb_username.current(0)
        self.cb_username.pack(fill=X, expand=True, padx=50, pady=20)
        self.btn_login.pack(anchor=CENTER, expand=True, padx=10, pady=10)
        self.update()

    def _bind_events(self):
        """Bind all initial events to relevant widgets"""
        # self.e_password.bind(RETURN_EVENT, self.click_login_event)
        self.btn_login.bind(BUTTON_EVENT, self.click_login_event)

    def click_login_event(self, event):
        if self.cb_username.get() == self._admins[0].name:
            self._do_form_login(self._admins[0].id)
        else:
            messagebox.showerror(LOGIN_ERROR_MESSAGE_TITLE, LOGIN_ERROR_MESSAGE)

