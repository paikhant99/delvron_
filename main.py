from tkinter import *
import sys

from views.login_form import LoginForm
from views.employee_administration.employee_adminstration_form import UserManageForm
from views.orders_manage.orders_manage_form import OrdersManageForm

from constants import TITLE, resource_path

from PIL import Image, ImageTk
import ctypes
from persistence.database import SQLiteDatabase

if getattr(sys, 'frozen', False):
    import pyi_splash

ctypes.windll.shcore.SetProcessDpiAwareness(1)


class Application(Tk):

    def __init__(self):
        Tk.__init__(self)
        self.wm_title(TITLE)
        if getattr(sys, 'frozen', False):
            pyi_splash.close()
        print(f"{self.winfo_geometry()}")
        self.wm_iconphoto(True, ImageTk.PhotoImage(Image.open(resource_path("images/logo_color.png"))))

        self.db = SQLiteDatabase()
        self.start_id = 0

        self.login_form = LoginForm(self.db, self._ua_form_login, self._do_form_login)
        self.login_form.pack(side=TOP, anchor=CENTER, expand=True, padx=10, pady=10)
        self.update_idletasks()

        self.wm_geometry('1483x840+0+0')
        self.wm_minsize(width=1483, height=840)

    def _edit_id(self, start_id):
        self.start_id = start_id
        print(self.start_id)

    def _ua_form_login(self):
        self.login_form.pack_forget()
        self.ua_form = UserManageForm(self.db, self._ua_form_logout)
        self.ua_form.pack(expand=True)

    def _do_form_login(self, _admin_id):
        self.login_form.pack_forget()
        # self.do_form = DeliveryOrderForm(self.persistence, self._do_form_logout, _admin_id)
        # self.do_form.pack(expand=True, padx=10, pady=10)

        self._frame_orders_manage = OrdersManageForm(self.db, _admin_id)
        self._frame_orders_manage.pack(fill=BOTH, expand=True)

    def _ua_form_logout(self):
        self.configure(menu=Menu(self.master))
        self.ua_form.destroy()
        self.login_form.pack(side=TOP, anchor=CENTER, expand=True, padx=10, pady=10)

    def _do_form_logout(self):
        self.configure(menu=Menu(self.master))
        self.do_form.destroy()
        self.login_form.pack(side=TOP, anchor=CENTER, expand=True, padx=10, pady=10)


Application().mainloop()
