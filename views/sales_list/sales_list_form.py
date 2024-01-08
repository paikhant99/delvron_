import datetime
from tkinter import *

from customs import *

from business.usecases import DisplaySalesUsecase, RetrieveAllAvailableItemsUsecase, RetrieveAllActiveSalesmenUsecase

from constants import COMBO_EVENT, BUTTON_EVENT, LABEL_TIME_PERIOD, LABEL_CUSTOMER_NAME, LABEL_PRODUCT_NAME, LABEL_SALESMAN_NAME, LABEL_NET_AMOUNT, LABEL_BTN_FILTER, VIEW_SUMMARY_LABEL, VIEW_DETAILS_LABEL, EXPORT_CSV_LABEL

import csv
from tkinter import filedialog

from views.sales_filter_form import SalesFilterForm
from views.customers.customers_forms import ItemsListForm

from persistence.repository import SalesRepositoryImpl, ItemsRepositoryImpl, UsersRepositoryImpl
from persistence.dao import UsersDaoImpl, ItemsDaoImpl, SalesDaoImpl
from business.models import Customer, CustomerType

from views.sales_list.sales_list_form_contract import SalesListFormContract
from views.sales_list.sales_list_form_presenter import SalesListFormPresenter


class SalesListForm(Toplevel, SalesListFormContract.View):

    def show_active_salesmen(self, _salesmen):
        self._active_salesmen_dict = {'All': None}
        self._active_salesmen_dict.update({_salesman.name: _salesman for _salesman in _salesmen})
        self._cb_slf_salesmen.set_values(self._active_salesmen_dict)

    def show_available_items(self, _items):
        self._items_available_dict = {'All': None}
        self._items_available_dict.update({_item.name: _item for _item in _items})
        self._cb_slf_products.set_values(self._items_available_dict)

    def show_sales(self, _sales):
        self.tv_sales.delete(*self.tv_sales.get_children())
        self.sales = _sales
        _net_amount = 0
        for sale_item in _sales:
            _total_amt = sum([int(order_product.unit_price) * int(order_product.qty) for order_product in sale_item.sales_order.order_products])
            _total_count = sum([int(order_product.qty) for order_product in sale_item.sales_order.order_products])
            self.tv_sales.insert('', END, iid=sale_item.id, values=(sale_item.created_at, sale_item.id, sale_item.sales_order.company.id, sale_item.sales_order.company.name, '', _total_count, f'{_total_amt:,}', sale_item.sell_by.name, sale_item.approve_by.name))
            for order_product in sale_item.sales_order.order_products:
                self.tv_sales.insert(sale_item.id, END, values=('', '', order_product.item.item_code, order_product.item.name, order_product.unit_price, order_product.qty, f'{int(order_product.unit_price) * int(order_product.qty):,}'))
            _net_amount += _total_amt
        self._lbl_net_amount['text'] = LABEL_NET_AMOUNT % f'{_net_amount:,}'

    def __init__(self, master, _bg_color, _db, root_x, root_y):
        Toplevel.__init__(self, bg=_bg_color)
        print("Sales List Form: Initiated")

        self._db = _db
        self._sale_repo = SalesRepositoryImpl(SalesDaoImpl(_db))
        self._items_repo = ItemsRepositoryImpl(ItemsDaoImpl(_db))
        self._users_repo = UsersRepositoryImpl(UsersDaoImpl(_db))
        self._presenter = SalesListFormPresenter(
            _mView=self, _display_sales_usecase=DisplaySalesUsecase(self._sale_repo),
            _retrieve_all_available_items_usecase=RetrieveAllAvailableItemsUsecase(self._items_repo),
            _retrieve_all_active_salesmen_usecase=RetrieveAllActiveSalesmenUsecase(self._users_repo)
        )

        self._items_available_dict = {'All': None}
        self._active_salesmen_dict = {'All': None}
        self._start_date = datetime.date.today()
        self._end_date = datetime.date.today()
        self._selected_company = Customer(id=0, name="All", address="All", phno="", serial_no="", installed_date="", customer_type=CustomerType.NORMAL.value, deactivated=False)

        self._lf_slf_filter = LabelFrame(self, text='FILTER BY')
        self._f_slf_filter = Frame(self._lf_slf_filter)

        self._lbl_time_period = Label(self._f_slf_filter,
                                      text=LABEL_TIME_PERIOD % (datetime.datetime.now().strftime('%d-%m-%Y'), datetime.datetime.now().strftime('%d-%m-%Y')))
        self._btn_slf_filter_control = Button(self._f_slf_filter, text=LABEL_BTN_FILTER)

        self._lbl_slf_customer_name = Label(self._f_slf_filter, text=LABEL_CUSTOMER_NAME)
        self._cb_slf_customers = ttk.Combobox(self._f_slf_filter, state="readonly", values=['All'])
        self._lbl_product_name = Label(self._f_slf_filter, text=LABEL_PRODUCT_NAME)
        self._cb_slf_products = CustomComboBox(self._f_slf_filter, state="readonly", values=self._items_available_dict)
        self._lbl_salesman_name = Label(self._f_slf_filter, text=LABEL_SALESMAN_NAME)
        self._cb_slf_salesmen = CustomComboBox(self._f_slf_filter, state="readonly", values=self._active_salesmen_dict)
        self._lbl_net_amount = Label(self._f_slf_filter, text=LABEL_NET_AMOUNT % '0')
        self._btn_view_summary = Button(self._f_slf_filter, text=VIEW_SUMMARY_LABEL)
        self._btn_export_csv = Button(self._f_slf_filter, text=EXPORT_CSV_LABEL)

        self._f_sale_list = Frame(self)
        self.tv_sales = ttk.Treeview(self._f_sale_list, show="headings", height=20)
        self.sc_sales = ttk.Scrollbar(self._f_sale_list, orient=VERTICAL, command=self.tv_sales.yview)

        self._f_sale_summary = Frame(self)
        self._lf_slf_customers_summary = LabelFrame(self._f_sale_summary, text='Customers Summary')
        self._lf_slf_sales_items_summary = LabelFrame(self._f_sale_summary, text='Sales Summary')
        self._lf_slf_salesmen_summary = LabelFrame(self._f_sale_summary, text='Salesmen Summary')

        self._tv_slf_customers_summary = ttk.Treeview(self._lf_slf_customers_summary, show='headings', height=20)
        self._sc_slf_customers_summary = ttk.Scrollbar(self._lf_slf_customers_summary, orient=VERTICAL, command=self._tv_slf_customers_summary.yview)

        self._create_views(master, root_x, root_y)
        self._bind_events()

        self._presenter.on_load_sales(self._start_date, self._end_date, self._selected_company, self._cb_slf_products.get(), self._cb_slf_salesmen.get())
        self._presenter.on_load_available_items()
        self._presenter.on_load_active_salesmen()

    def _create_views(self, master, root_x, root_y):
        self.wm_title("Sale Statement View")
        self.grid_anchor(CENTER)
        self.wm_geometry(f"+{root_x}+{root_y}")
        self.wm_transient(master)
        self.grab_set()

        self._cb_slf_customers.current(0)
        self._cb_slf_products.current(0)
        self._cb_slf_salesmen.current(0)

        self._lf_slf_filter.pack(fill=X, side=TOP, padx=5, pady=5)
        self._f_slf_filter.pack(anchor=CENTER, expand=True)
        self._lbl_time_period.grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky=W)
        self._btn_slf_filter_control.grid(row=0, column=2, padx=5, pady=5, sticky=E)
        self._lbl_slf_customer_name.grid(row=1, column=0, padx=5, pady=5, sticky=W)
        self._cb_slf_customers.grid(row=1, column=1, padx=5, pady=5, sticky=W)
        self._lbl_salesman_name.grid(row=1, column=2, padx=5, pady=5, sticky=W)
        self._cb_slf_salesmen.grid(row=1, column=3, padx=5, pady=5, sticky=W)
        self._lbl_product_name.grid(row=2, column=0, padx=5, pady=5, sticky=W)
        self._cb_slf_products.grid(row=2, column=1, padx=5, pady=5, sticky=W)
        self._lbl_net_amount.grid(row=2, column=2, padx=5, pady=5, sticky=W)
        self._btn_view_summary.grid(row=3, column=0, columnspan=2, padx=5, pady=5)
        self._btn_export_csv.grid(row=3, column=2, columnspan=2, padx=5, pady=5)

        self.tv_sales['columns'] = ('SALE DATE', 'SALE ID', 'CODE', 'NAME', 'UNIT PRICE', 'ORDERS QTY', 'TOTAL AMOUNT', 'SOLD BY', 'APPROVED BY')

        self.tv_sales.column('#1', width=100, stretch=YES, anchor=W, minwidth=100)
        self.tv_sales.column('#2', width=100, stretch=YES, anchor=E, minwidth=100)
        self.tv_sales.column('#3', width=100, stretch=YES, minwidth=150, anchor=W)
        self.tv_sales.column('#4', width=150, stretch=YES, anchor=W, minwidth=150)
        self.tv_sales.column('#5', width=150, stretch=YES, minwidth=150, anchor=E)
        self.tv_sales.column('#6', width=100, stretch=YES, anchor=E, minwidth=100)
        self.tv_sales.column('#7', width=150, stretch=YES, minwidth=150, anchor=E)
        self.tv_sales.column('#8', width=150, stretch=YES, minwidth=150, anchor=W)
        self.tv_sales.column('#9', width=200, stretch=YES, minwidth=200, anchor=W)

        self.tv_sales.heading('#1', text='Sale Date')
        self.tv_sales.heading('#2', text='Sale Id')
        self.tv_sales.heading('#3', text='Code')
        self.tv_sales.heading('#4', text='Name')
        self.tv_sales.heading('#5', text='Unit Price')
        self.tv_sales.heading('#6', text='Order Qty')
        self.tv_sales.heading('#7', text='Total Amount')
        self.tv_sales.heading('#8', text='Sold by')
        self.tv_sales.heading('#9', text='Approved by')

        self._f_sale_list.pack(fill=BOTH, expand=True, padx=5, pady=5)
        self.tv_sales.configure(yscrollcommand=self.sc_sales.set)
        self.tv_sales.pack(side=LEFT, fill=BOTH, expand=True)
        self.sc_sales.pack(side=RIGHT, fill=BOTH)

        self.update()
        self.wm_minsize(width=self.winfo_width(), height=self.winfo_height())

    def _bind_events(self):
        self._btn_slf_filter_control.bind(BUTTON_EVENT, self._btn_slf_filter_control_click_event)
        self._btn_export_csv.bind(BUTTON_EVENT, self._btn_export_csv_click_event)
        self._cb_slf_products.bind(COMBO_EVENT, self._cb_slf_products_selection_event)
        self._cb_slf_salesmen.bind(COMBO_EVENT, self._cb_slf_salesmen_selection_event)
        self._cb_slf_customers.bind(BUTTON_EVENT, self._cb_slf_customers_click_event)
        self._btn_view_summary.bind(BUTTON_EVENT, self._btn_view_summary_click_event)

    def _btn_slf_filter_control_click_event(self, event):
        SalesFilterForm(self, self.master.winfo_x(), self.master.winfo_y(), self._filter_succeed_event)
        self.update()
        self.wm_minsize(width=self.winfo_width(), height=self.winfo_height())

    def _filter_succeed_event(self, _start_date, _end_date):
        self._start_date = datetime.datetime.strptime(_start_date, '%d-%m-%Y').strftime('%Y-%m-%d')
        self._end_date = datetime.datetime.strptime(_end_date, '%d-%m-%Y').strftime('%Y-%m-%d')
        self._lbl_time_period['text'] = LABEL_TIME_PERIOD % (_start_date, _end_date)
        self._presenter.on_load_sales(datetime.datetime.strptime(_start_date, '%d-%m-%Y').strftime('%Y-%m-%d'), datetime.datetime.strptime(_end_date, '%d-%m-%Y').strftime('%Y-%m-%d'), self._selected_company, self._cb_slf_products.get(), self._cb_slf_salesmen.get())

    def _btn_export_csv_click_event(self, event):
        _file_name = filedialog.asksaveasfilename(parent=self, initialdir="/",
                                                  title=f"Select file : Sales form",
                                                  filetypes=[('csv file', '*.csv')])

        if _file_name:
            if _file_name.endswith('.csv'):
                _file_name = _file_name.split('.')[0]
            with open(f'{_file_name}.csv', 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(
                    ['SALE NO', 'SALE DATE', 'DESCRIPTION', 'UNIT PRICE', 'QUANTITY', 'TOTAL AMOUNT', 'CUSTOMER CODE',
                     'CUSTOMER NAME', 'SOLD BY', 'APPROVE BY'])
                _sales = [(sale.id, sale.created_at, order_product.item.name, order_product.unit_price,
                           order_product.qty, int(order_product.unit_price) * int(order_product.qty),
                           sale.sales_order.company.id, sale.sales_order.company.name, sale.sell_by.name,
                           sale.approve_by.name) for sale in self.sales for order_product in sale.sales_order.order_products ]
                writer.writerows(_sales)

    def _cb_slf_products_selection_event(self, event):
        self._presenter.on_load_sales(self._start_date, self._end_date, self._selected_company,
                              self._cb_slf_products.get(), self._cb_slf_salesmen.get())

    def _cb_slf_salesmen_selection_event(self, event):
        self._presenter.on_load_sales(self._start_date, self._end_date, self._selected_company,
                              self._cb_slf_products.get(), self._cb_slf_salesmen.get())

    def _cb_slf_customers_click_event(self, event):
        self._cb_slf_customers.configure(state=DISABLED)
        self.update_idletasks()

        ItemsListForm(self, self._db, self._cb_selection_company_event,
                      self.master.winfo_x() + event.widget.winfo_x(),
                      self.master.winfo_y() + event.widget.winfo_y(), _default_items=[Customer(id=0, name="All", address="All", phno="", serial_no="", installed_date="", customer_type=CustomerType.NORMAL.value, deactivated=False)])

    def _cb_selection_company_event(self, company):
        self._cb_slf_customers.configure(state="readonly")
        if company:
            self._selected_company = company
            self._cb_slf_customers.set(self._selected_company.name if self._selected_company.id != 0 else 'All')
            self._presenter.on_load_sales(self._start_date, self._end_date, self._selected_company,
                                  self._cb_slf_products.get(), self._cb_slf_salesmen.get())

    def _btn_view_summary_click_event(self, event):
        if self._btn_view_summary['text'] == VIEW_SUMMARY_LABEL:
            self._f_sale_list.pack_forget()
        else:
            self._f_sale_list.pack()
        self._btn_view_summary['text'] = VIEW_DETAILS_LABEL if self._btn_view_summary['text'] == VIEW_SUMMARY_LABEL else VIEW_SUMMARY_LABEL