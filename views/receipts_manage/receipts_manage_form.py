from tkinter import *
from customs import *

from tkcalendar import *
from datetime import datetime

from tkinter import messagebox

from constants import LABEL_ORDER_QTY, LABEL_SALES_AMT, LABEL_BALANCE, BUTTON_EVENT, DATE_ENTRY_EVENT, SAVE_ERROR_MESSAGE_TITLE

from views.customers.customers_forms import ItemsListForm

from business.models import Customer, CustomerType
from business.usecases import GetAllReceiptsByDateAndCustomerUsecase, DisplayOneSaleAndReceiptsUsecase, InsertOneReceiptUsecase, UpdateBalanceOnSaleIdUsecase

from persistence.repository import ReceiptsRepositoryImpl
from persistence.dao import ReceiptsDaoImpl

from views.receipts_manage.receipts_manage_form_presenter import ReceiptsManageFormPresenter
from views.receipts_manage.receipts_manage_form_contract import ReceiptsManageFormContract


class ReceiptsManageForm(Frame, ReceiptsManageFormContract.View):

    def show_update_balance(self, rowcount):
        self._presenter.on_load_all_receipts_by_date_and_customer(self._selected_company.id if self._selected_company.id != 0 else '%',
                                                 datetime.strptime(self._de_rmf_date.get(), '%d-%m-%Y').strftime(
                                                  '%Y-%m-%d'))

    def show_save_receipt_completed(self, param):
        _sale_id, _balance = param
        self._cb_rmf_sale_id.set('')
        self._lbl_rmf_order_qty['text'] = LABEL_ORDER_QTY % '.....'
        self._lbl_rmf_sales_amt['text'] = LABEL_SALES_AMT % '.....'
        self._lbl_rmf_balance_amt['text'] = LABEL_BALANCE % '.....'
        self._e_rmf_received_amt.delete(0, END)
        self._e_rmf_remark.delete(0, END)

        self._presenter.on_update_balance(_balance, _sale_id)

    def show_save_receipt_error(self, _error):
        messagebox.showerror(SAVE_ERROR_MESSAGE_TITLE, _error.args[0])

    def show_one_sale_and_receipts(self, _sale):
        self._sale = _sale
        self._total_sale = sum([int(order_product.qty) * int(order_product.unit_price) for order_product in _sale.sales_order.order_products])
        self._balance = _sale.receipts[0].balance if len(_sale.receipts) > 0 else self._total_sale
        self._lbl_rmf_order_qty['text'] = LABEL_ORDER_QTY % len(_sale.sales_order.order_products)
        self._lbl_rmf_sales_amt['text'] = LABEL_SALES_AMT % f'{self._total_sale:,}'
        self._lbl_rmf_balance_amt['text'] = LABEL_BALANCE % f'{self._balance:,}'

    def show_all_receipts(self, _receipts):
        self._tv_rmf_receipts.delete(*self._tv_rmf_receipts.get_children())
        for _receipt in _receipts:
            self._tv_rmf_receipts.insert('', END, values=(_receipt.id, _receipt.sale_id, _receipt.sale_amount, _receipt.received_amount, _receipt.balance))

    def __init__(self, master, _db):
        Frame.__init__(self, master)
        self._db = _db
        self._receipts_repo = ReceiptsRepositoryImpl(ReceiptsDaoImpl(_db))
        self._presenter = ReceiptsManageFormPresenter(
            _mView=self, _get_all_receipts_by_date_and_customer_usecase=GetAllReceiptsByDateAndCustomerUsecase(self._receipts_repo),
            _display_one_sale_and_receipts_usecase=DisplayOneSaleAndReceiptsUsecase(self._receipts_repo),
            _insert_one_receipt_usecase=InsertOneReceiptUsecase(self._receipts_repo),
            _update_balance_on_sale_id_usecase=UpdateBalanceOnSaleIdUsecase(self._receipts_repo)
        )
        self._sale = None
        self._selected_company = Customer(id=0, name="All", address="All", phno="", serial_no="", installed_date="",
                                          customer_type=CustomerType.NORMAL.value, deactivated=False)

        self._f_rmf_filter = Frame(self)

        self._lbl_rmf_customer = Label(self._f_rmf_filter, text='Customer')
        self._cb_rmf_customer = ttk.Combobox(self._f_rmf_filter, state='readonly', values=['All'])
        self._lbl_rmf_date = Label(self._f_rmf_filter, text='Date')
        self._de_rmf_date = DateEntry(self._f_rmf_filter, date_pattern="dd-mm-yyyy", width=20, state="readonly")
        self._lbl_rmf_customer.pack(side=LEFT, padx=10, pady=10)
        self._cb_rmf_customer.pack(side=LEFT, padx=10, pady=10)

        self._f_rmf_receipt = Frame(self)
        self._tv_rmf_receipts = ttk.Treeview(self._f_rmf_receipt, show="headings", height=20)
        self._sc_rmf_receipts = ttk.Scrollbar(self._f_rmf_receipt, orient=VERTICAL, command=self._tv_rmf_receipts.yview)

        self._lf_rmf_receipt_info = LabelFrame(self._f_rmf_receipt, text='Receivable')
        self._lbl_rmf_sale_id = Label(self._lf_rmf_receipt_info, text='Sale Id')
        self._cb_rmf_sale_id = ttk.Combobox(self._lf_rmf_receipt_info, state="readonly")
        self._lbl_rmf_order_qty = Label(self._lf_rmf_receipt_info, text=LABEL_ORDER_QTY % '.....')
        self._lbl_rmf_sales_amt = Label(self._lf_rmf_receipt_info, text=LABEL_SALES_AMT % '.....')
        self._lbl_rmf_balance_amt = Label(self._lf_rmf_receipt_info, text=LABEL_BALANCE % '.....')
        self._lbl_rmf_received_amt = Label(self._lf_rmf_receipt_info, text='Received Amount')
        self._e_rmf_received_amt = Entry(self._lf_rmf_receipt_info)
        self._lbl_rmf_remark = Label(self._lf_rmf_receipt_info, text='Remark')
        self._e_rmf_remark = Entry(self._lf_rmf_receipt_info)
        self._btn_rmf_save = Button(self._lf_rmf_receipt_info, text='Save')

        self._create_views()
        self._bind_events()

        self._presenter.on_load_all_receipts_by_date_and_customer('%', datetime.strptime(self._de_rmf_date.get(), '%d-%m-%Y').strftime('%Y-%m-%d'))

    def _create_views(self):

        self._cb_rmf_customer.current(0)
        self._f_rmf_filter.pack(fill=X, side=TOP, padx=10, pady=10)
        self._f_rmf_receipt.pack(fill=BOTH, side=BOTTOM, expand=True)

        self._de_rmf_date.pack(side=RIGHT, padx=10, pady=10)
        self._lbl_rmf_date.pack(side=RIGHT, padx=10, pady=10)

        self._tv_rmf_receipts['columns'] = ('RECEIPT ID', 'INVOICE ID', 'SALE AMOUNT', 'RECEIVED AMOUNT', 'BALANCE')

        self._tv_rmf_receipts.column('#1', width=100, stretch=YES, anchor=E, minwidth=100)
        self._tv_rmf_receipts.column('#2', width=100, stretch=YES, anchor=E, minwidth=100)
        self._tv_rmf_receipts.column('#3', width=150, stretch=YES, minwidth=150, anchor=E)
        self._tv_rmf_receipts.column('#4', width=150, stretch=YES, anchor=E, minwidth=150)
        self._tv_rmf_receipts.column('#5', width=150, stretch=YES, minwidth=150, anchor=E)

        self._tv_rmf_receipts.heading('#1', text='Receipt Id')
        self._tv_rmf_receipts.heading('#2', text='Sale Id')
        self._tv_rmf_receipts.heading('#3', text='Sale Amount')
        self._tv_rmf_receipts.heading('#4', text='Received Amount')
        self._tv_rmf_receipts.heading('#5', text='Balance')

        self._tv_rmf_receipts.pack(side=LEFT, fill=BOTH, expand=True)
        self._sc_rmf_receipts.pack(side=LEFT, fill=BOTH)
        self._tv_rmf_receipts.configure(yscrollcommand=self._sc_rmf_receipts.set)

        self._lf_rmf_receipt_info.pack(side=RIGHT, fill=BOTH, padx=10, pady=10)
        self._lbl_rmf_sale_id.grid(row=0, column=0, padx=10, pady=10, sticky=W)
        self._cb_rmf_sale_id.grid(row=0, column=1, padx=10, pady=10)
        self._lbl_rmf_order_qty.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky=W)
        self._lbl_rmf_sales_amt.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky=W)
        self._lbl_rmf_balance_amt.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky=W)
        self._lbl_rmf_received_amt.grid(row=4, column=0, padx=10, pady=10, sticky=W)
        self._e_rmf_received_amt.grid(row=4, column=1, padx=10, pady=10)
        self._lbl_rmf_remark.grid(row=5, column=0, padx=10, pady=10, sticky=W)
        self._e_rmf_remark.grid(row=5, column=1, padx=10, pady=10)
        self._btn_rmf_save.grid(row=6, column=1, padx=10, pady=10)

    def _bind_events(self):
        self._cb_rmf_customer.bind(BUTTON_EVENT, self._cb_rmf_customer_click_event)
        self._de_rmf_date.bind(DATE_ENTRY_EVENT, self._de_rmf_date_click_event)
        self._cb_rmf_sale_id.bind(BUTTON_EVENT, self._cb_rmf_sale_id_click_event)
        self._btn_rmf_save.bind(BUTTON_EVENT, self._btn_rmf_save_click_event)

    def _cb_rmf_customer_click_event(self, event):
        self._cb_rmf_customer.configure(state=DISABLED)
        self.update_idletasks()

        ItemsListForm(self, self._db, self._cb_selection_company_event,
                      self.master.winfo_x() + event.widget.winfo_x(),
                      self.master.winfo_y() + event.widget.winfo_y(), _default_items=[
                Customer(id=0, name="All", address="All", phno="", serial_no="", installed_date="",
                         customer_type=CustomerType.NORMAL.value, deactivated=False)])

    def _cb_selection_company_event(self, _company):
        self._cb_rmf_customer.configure(state="readonly")
        if _company:
            self._selected_company = _company
            self._cb_rmf_customer.set(self._selected_company.name if self._selected_company.id != 0 else 'All')
            self._presenter.on_load_all_receipts_by_date_and_customer(_company.id if _company.id != 0 else '%', datetime.strptime(self._de_rmf_date.get(), '%d-%m-%Y').strftime('%Y-%m-%d'))

    def _de_rmf_date_click_event(self, event):
        self._presenter.on_load_all_receipts_by_date_and_customer(self._selected_company.id if self._selected_company.id != 0 else '%',
                                                 datetime.strptime(self._de_rmf_date.get(), '%d-%m-%Y').strftime(
                                                  '%Y-%m-%d'))

    def _cb_rmf_sale_id_click_event(self, event):
        self._cb_rmf_sale_id.configure(state=DISABLED)
        self.update_idletasks()

        ItemsListForm(self, self._db, self._cb_selection_sale_event,
                      self.master.winfo_x() + event.widget.winfo_x(),
                      self.master.winfo_y() + event.widget.winfo_y(), flag_label='Sales', _customer_id=self._selected_company.id if self._selected_company.id != 0 else '%')

    def _cb_selection_sale_event(self, _sale_id):
        self._cb_rmf_sale_id.configure(state="readonly")
        if _sale_id:
            self._cb_rmf_sale_id.set(_sale_id)
            self._presenter.on_load_one_sale_and_receipts(_sale_id)

    def _btn_rmf_save_click_event(self, event):
        print(datetime.now().strftime('%Y-%m-%d'))
        if self._sale:
            self._presenter.on_save_receipt_click(self._sale.id, self._sale.sales_order.company.id, self._total_sale, self._e_rmf_received_amt.get(), self._balance, datetime.now().strftime('%Y-%m-%d'), self._e_rmf_remark.get())