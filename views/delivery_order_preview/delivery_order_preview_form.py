import datetime
import time
from tkinter import *
from PDFViewer import ShowPdf

from tkcalendar import *
from tkinter import messagebox

from customs import *
from constants import BUTTON_EVENT, COMBO_EVENT, DATE_ENTRY_EVENT

import win32con
import win32print
import win32ui
import fitz
from PIL import Image, ImageWin

from business.usecases import MakeSaleUsecase, ReviewOrderUsecase, RetrieveAllActiveUsersUsecase, UpdateOrderStatusUsecase, GetDelvronAdminUsecase, UpdateDelvronSaleIdUsecase

from business.models import Role, OrderStatus
from persistence.repository import SalesRepositoryImpl, SalesOrdersRepositoryImpl, UserAdminRepositoryImpl, UsersRepositoryImpl
from persistence.dao import UsersDaoImpl, UserAdminDaoImpl, SalesDaoImpl, SalesOrdersDaoImpl

from views.delivery_order_preview.delivery_order_preview_form_presenter import DeliveryOrderPreviewFormPresenter
from views.delivery_order_preview.delivery_order_preview_form_contract import DeliveryOrderPreviewFormContract


class DeliveryOrderPreviewForm(Toplevel, DeliveryOrderPreviewFormContract.View):

    def show_admin(self, admins):
        self._expected_sale_id = admins[0].order_id
        self._show_preview_form(self._order, self._expected_sale_id)
        self._pv_order_preview.pack(fill=BOTH, side=RIGHT)

    def show_all_active_users(self, _users):
        if _users:
            _office_staffs = {_user.name: _user for _user in _users if _user.position == Role.OFFICE.value}
            self._cb_dopf_approve_by.set_values(_office_staffs)
            _salemen = {_user.name: _user for _user in _users if _user.position == Role.SALES.value}
            self._cb_dopf_sell_by.set_values(_salemen)

    def show_order_reviewed(self, _order):
        self._order = _order
        self._lbl_dopf_customer_name['text'] = self._order.company.name
        self._presenter.on_load_admin(self._admin_id)

    def show_make_sale_completed(self, _sale_id):
        """State that order making is successful"""
        self._presenter.on_update_order_status_finished(self._order_id)
        self._presenter.on_update_next_sale_id_delvron_finished(_sale_id + 1)
        self._make_sale_completed_state()
        self._close_window()

    def __init__(self, master, _db, _admin_id, _order_id, _make_sale_completed_state):
        Toplevel.__init__(self)
        self.wm_title("Preview")
        # self.grid_anchor(CENTER)
        self.wm_transient(master)
        self.grab_set()
        print("Print Preview Form: Print Preview Form initiated")

        self._admin_id = _admin_id
        self._order_id = _order_id
        self._make_sale_completed_state = _make_sale_completed_state
        self._users_repo = UsersRepositoryImpl(UsersDaoImpl(_db))
        self._user_admins_repo = UserAdminRepositoryImpl(UserAdminDaoImpl(_db))
        self._sale_repo = SalesRepositoryImpl(SalesDaoImpl(_db))
        self._sales_orders_repo = SalesOrdersRepositoryImpl(SalesOrdersDaoImpl(_db))
        self._presenter = DeliveryOrderPreviewFormPresenter(
            _mView=self, _review_order_usecase=ReviewOrderUsecase(self._sales_orders_repo),
            _get_delvron_admin_usecase=GetDelvronAdminUsecase(self._user_admins_repo),
            _retrieve_all_active_users_usecase=RetrieveAllActiveUsersUsecase(self._users_repo),
            _make_sale_usecase=MakeSaleUsecase(self._sale_repo),
            _update_order_status_usecase=UpdateOrderStatusUsecase(self._sales_orders_repo),
            _update_delvron_sale_id_usecase=UpdateDelvronSaleIdUsecase(self._user_admins_repo)
        )

        self._printer_name = win32print.GetDefaultPrinter()
        self.dot_matrix_printers = ['EPSON LQ-630K ESC/P2']
        _handle = win32print.OpenPrinter(self._printer_name)
        self._temp_printer_info = win32print.GetPrinter(_handle, 4)

        self._f_dopf_info_preview = Frame(self)
        self._f_dopf_extra_info_preview = Frame(self._f_dopf_info_preview)
        self._lbl_dopf_customer_name = Label(self._f_dopf_extra_info_preview)
        self._de_deliver_date = self._de_sff_to = DateEntry(self._f_dopf_extra_info_preview, date_pattern="dd-mm-yyyy", width=20, state="readonly", mindate=datetime.datetime.now())
        self._cb_dopf_approve_by = CustomComboBox(self._f_dopf_extra_info_preview, values={}, state="readonly", width=30)
        self._cb_dopf_sell_by = CustomComboBox(self._f_dopf_extra_info_preview, values={}, state="readonly", width=30)

        self.btn_save_print = Button(self._f_dopf_info_preview, text="Save & Print")

        self._create_views()
        self._bind_events()
        self._presenter.on_review_order(self._order_id)
        self._presenter.on_load_all_active_users()

        win32print.ClosePrinter(_handle)

    def _create_views(self):

        Label(self._f_dopf_extra_info_preview, text='CUSTOMER NAME').grid(row=0, column=0, padx=10, pady=10, sticky=W)
        self._lbl_dopf_customer_name.grid(row=0, column=1, padx=10, pady=10, sticky=E)
        Label(self._f_dopf_extra_info_preview, text='DELIVER DATE').grid(row=1, column=0, padx=10, pady=10, sticky=W)
        self._de_deliver_date.grid(row=1, column=1, padx=10, pady=10, sticky=E)
        Label(self._f_dopf_extra_info_preview, text='SELL BY').grid(row=2, column=0, padx=10, pady=10, sticky=W)
        self._cb_dopf_sell_by.grid(row=2, column=1, padx=10, pady=10, sticky=E)
        Label(self._f_dopf_extra_info_preview, text='APPROVE BY').grid(row=3, column=0, padx=10, pady=10, sticky=W)
        self._cb_dopf_approve_by.grid(row=3, column=1, padx=10, pady=10, sticky=E)
        self._f_dopf_extra_info_preview.pack(expand=True)

        self.btn_save_print.pack(expand=True, padx=5, pady=5)
        self._f_dopf_info_preview.pack(fill=BOTH, side=RIGHT)

    def _bind_events(self):
        self._de_deliver_date.bind(DATE_ENTRY_EVENT, self._de_deliver_date_select_event)
        self._cb_dopf_sell_by.bind(COMBO_EVENT, self._cb_dopf_sell_by_select_event)
        self._cb_dopf_approve_by.bind(COMBO_EVENT, self._cb_dopf_approve_by_select_event)
        self.protocol("WM_DELETE_WINDOW", lambda: self._close_window())
        self.btn_save_print.bind(BUTTON_EVENT, self._btn_dopf_save_print_click__event)

    def _show_preview_form(self, _order, _expected_sale_id):
        self.filename = f"{os.getcwd()}/{self._de_deliver_date.get_date().strftime('%d-%m-%Y')}.pdf"
        self.print_pdf = CustomPDF(self.filename, _expected_sale_id,
                                   self._de_deliver_date.get_date().strftime('%d-%m-%Y'), _order.order_products,
                                   _order.company, self._cb_dopf_approve_by.get(), self._cb_dopf_sell_by.get(),
                                   size=LETTER if self._temp_printer_info[
                                                      'pPrinterName'] in self.dot_matrix_printers else A4)
        self.print_pdf.generate()
        self._pv_order_preview = ShowPdf().pdf_view(self, pdf_location=self.filename, width=80,
                                                    height=LETTER[1] * 0.047 if self._temp_printer_info[
                                                                                    'pPrinterName'] in self.dot_matrix_printers else
                                                    A4[1] * 0.047)

    def _de_deliver_date_select_event(self, event):
        self._pv_order_preview.pack_forget()
        self._show_preview_form(self._order, self._expected_sale_id)
        self._pv_order_preview.pack(fill=BOTH, side=RIGHT)

    def _cb_dopf_approve_by_select_event(self, event):
        self._pv_order_preview.pack_forget()
        self._show_preview_form(self._order, self._expected_sale_id)
        self._pv_order_preview.pack(fill=BOTH, side=RIGHT)

    def _cb_dopf_sell_by_select_event(self, event):
        self._pv_order_preview.pack_forget()
        self._show_preview_form(self._order, self._expected_sale_id)
        self._pv_order_preview.pack(fill=BOTH, side=RIGHT)

    def _btn_dopf_save_print_click__event(self, event):
        print("Print Preview Form: Print Button Event Clicked")
        _print_defaults = {"DesiredAccess": win32print.PRINTER_ALL_ACCESS}
        _handle = win32print.OpenPrinter(self._printer_name, _print_defaults)
        # win32print.JOB_CONTROL_RESTART
        printer_info = win32print.GetPrinter(_handle, 2)
        print("Print Preview Form: Printer Opened")

        if self._cb_dopf_approve_by.get() and self._cb_dopf_sell_by.get():

            if self._printer_name.startswith('\\'):
                win32print.AddPrinterConnection(self._printer_name)

            print(f"Printer Info : {printer_info}")
            print(f"Printer Status : {(printer_info['Attributes'] & win32print.PRINTER_ATTRIBUTE_WORK_OFFLINE) >> 10}")

            if (printer_info['Attributes'] & win32print.PRINTER_ATTRIBUTE_WORK_OFFLINE) >> 10:
                messagebox.showwarning(title="PRINTER IS OFFLINE", message="Please connect your printer")
                win32print.ClosePrinter(_handle)
            else:

                pDevMode = printer_info['pDevMode']
                pDevMode.Orientation = win32con.DMORIENT_PORTRAIT
                pDevMode.Copies = 1 if printer_info['pPrinterName'] in self.dot_matrix_printers else 2
                pDevMode.PaperSize = win32con.DMPAPER_LETTER if printer_info[
                                                                    'pPrinterName'] in self.dot_matrix_printers else win32con.DMPAPER_A4
                printer_info['pDevMode'] = pDevMode

                win32print.SetPrinter(_handle, 2, printer_info, 0)

                bdc = win32ui.CreateDC()
                bdc.CreatePrinterDC(self._printer_name)

                try:
                    printerwidth = bdc.GetDeviceCaps(win32con.PHYSICALWIDTH)
                    printerheight = bdc.GetDeviceCaps(win32con.PHYSICALHEIGHT)

                    bdc.StartDoc(f"{self.filename}")
                    pdf_document = fitz.open(self.filename)
                    _, job = win32print.AddJob(_handle)
                    for page_no in range(pdf_document.page_count):
                        bdc.StartPage()
                        print("Print Preview Form: Printing Service Started")
                        pdf_page = pdf_document[page_no]
                        image = pdf_page.get_pixmap(matrix=fitz.Matrix(5, 5))
                        image = Image.frombytes("RGB", (image.width, image.height), image.samples)
                        """Printing image convert"""
                        # png_path = "temp.png"
                        # image.save(png_path)

                        dib_image = ImageWin.Dib(image)
                        print(
                            f"Print Preview Form: Image = {dib_image.size[0]}, {dib_image.size[1]} & Printer = {printerwidth}, {printerheight}")
                        dib_image.draw(bdc.GetHandleOutput(), (0, 0, printerwidth, printerheight))
                        bdc.EndPage()
                    pdf_document.close()
                    bdc.EndDoc()

                    self._presenter.on_make_sale_print(int(self._expected_sale_id),
                                       self._de_deliver_date.get_date().strftime('%Y-%m-%d'),
                                       self._order.id,
                                       self._cb_dopf_sell_by.get().id, self._cb_dopf_approve_by.get().id)

                except Exception as e:
                    print(f"Print Preview Form: Printing Service Stopped due to {e}")

                finally:
                    bdc.DeleteDC()
                    print("Print Preview Form: Printing Service Ended")

                    win32print.ClosePrinter(_handle)
                    print("Print Preview Form: Printer Closed")

        else:
            messagebox.showerror("Error", "Access Denied")
            win32print.ClosePrinter(_handle)

    def _monitor_job_status(self, handle, job):
        while True:
            # job_info = win32print.GetJob(handle, job, 2)
            job_info = win32print.EnumJobs(handle, 0, -1, 2)
            print(job_info)
            if job_info[0]['Status'] == win32print.JOB_STATUS_COMPLETE:
                self._close_window()
                print("Printed")
                break
            time.sleep(1)

    def _close_window(self):
        """Close X Button at top-right corner of window"""
        print("Print Preview Form: Exit Button X is clicked")

        self.print_pdf.delete_pdf()
        print("Print Preview Form: Temporary Print pdf file deleted")
        self.destroy()
        print("Print Preview Form: Exit Print Preview Form")