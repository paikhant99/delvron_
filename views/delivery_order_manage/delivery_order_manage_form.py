from tkinter import *
from tkinter import filedialog

import datetime

from customs import *

from business.usecases import (DisplayItemsWrtProductsUsecase, GetProductUsecase,
                               UpdateOrderUsecase, ReviewOrderUsecase)
from business.models import OrderProduct, CustomerType, OrderStatus

from persistence.repository import SalesOrdersRepositoryImpl, ItemsRepositoryImpl, ProductsRepositoryImpl
from persistence.dao import ItemsDaoImpl, SalesOrdersDaoImpl, ProductsDaoImpl

from constants import (COMBO_EVENT, TREEVIEW_SELECT_EVENT, BUTTON_EVENT, NUMBER_ERROR, NO_DATA_INPUT_ERROR,
                       INPUT_NUMBER_ERROR_MESSAGE, NO_DATA_INPUT_ERROR_MESSAGE, QUANTITY_LABEL)

from views.customers.customers_forms import ItemsListForm

from tkinter import messagebox

from views.delivery_order_manage.delivery_order_manage_form_presenter import DeliveryOrderManageFormPresenter
from views.delivery_order_manage.delivery_order_manage_form_contract import DeliveryOrderManageFormContract


class DeliveryOrderManageForm(Toplevel, DeliveryOrderManageFormContract.View):

    def show_order_reviewed(self, _order):

        if _order:
            self._company = _order.company
            self._cb_domf_companies.configure(state=DISABLED)
            self.show_company_data(_order.company)

            self._cart_list = {}
            self._in_cart_order_product_id_list = []
            for idx, _order_product in enumerate(_order.order_products):
                self._in_cart_order_product_id_list.append(_order_product.id)
                self._cart_list[self._tv_domf_order_details.insert('', END, values=(
                    (idx + 1), _order_product.item.name, _order_product.item.measurement, _order_product.qty,
                    _order_product.unit_price, _order_product.remark))] = _order_product

            self._presenter.on_load_items_wrt_products()
            # DisplayItemsWrtProductsUsecase()(self._items_repo).subscribe(
            #     on_next=self._next_items_wrt_products_retrieval_state)

        else:
            self._cb_domf_companies.bind(BUTTON_EVENT, self._cb_company_click_event)

    def show_ordering_completed(self, _completed):
        # todo call a dialog that asks for continue or deliver now.
        self._save_order_state()
        self.destroy()

    def show_ordering_error(self, error):
        messagebox.showerror(NO_DATA_INPUT_ERROR, error.args[0])

    def show_items_wrt_products(self, _items):
        self._product = None
        self._btn_domf_update_order_item['text'] = 'Add'
        self._ccb_domf_order_item_desc.set('')
        self._tv_domf_order_details.focus('')
        self._f_domf_order_extra_layout.pack_forget()
        self._lf_domf_order_item_info.pack_forget()
        self._btn_domf_order_save.pack_forget()
        self._ccb_domf_order_item_desc.unbind(COMBO_EVENT)
        self._btn_domf_delete_order_item.unbind(BUTTON_EVENT)
        self._btn_domf_delete_order_item.grid_remove()

        self._ccb_domf_order_item_desc.bind(COMBO_EVENT, self._ccb_domf_order_item_desc_select_event)
        self._f_domf_order_extra_layout.pack(fill=BOTH, side=RIGHT, expand=True, padx=5, pady=5)
        self._lf_domf_order_item_info.pack(fill=BOTH, side=TOP, expand=True)
        self._btn_domf_order_save.pack(fill=BOTH, side=BOTTOM, expand=True)
        if self._company.customer_type == CustomerType.SPECIAL.value:
            self._lb_domf_order_item_unit_price.grid(row=2, column=0, sticky=NSEW, padx=10, pady=10)
            self._e_domf_order_item_unit_price.grid(row=2, column=1, sticky=NSEW, padx=10, pady=10)
        else:
            self._lb_domf_order_item_unit_price.grid_remove()
            self._e_domf_order_item_unit_price.grid_remove()

        self._tv_domf_order_details.selection_remove(*self._tv_domf_order_details.get_children())
        self._e_domf_order_item_measurement.delete(0, END)
        self._e_domf_order_item_unit_price.delete(0, END)
        self._e_domf_order_item_qty.delete(0, END)
        self._e_domf_order_item_remark.delete(0, END)

        self._lbl_domf_order_total['text'] = sum(
            [(int(orderproduct.unit_price) * int(orderproduct.qty)) for orderproduct in self._cart_list.values()])

        self._items = {item.name: item for item in _items if
                       item.name not in [orderproduct.item.name for orderproduct in self._cart_list.values()]}
        self._ccb_domf_order_item_desc.set_values(self._items)

    def show_product(self, _product):
        self._product = _product
        self._e_domf_order_item_measurement.delete(0, END)
        self._e_domf_order_item_measurement.insert(END, _product.item.measurement)

    def __init__(self, master, _db, _bg_color, _order_id, _save_order_state):
        print("DeliveryOrderForm : Delivery Order Frame is initiated")
        self.order = None
        self._tree_columns = ['NO.', 'DESCRIPTION', 'COUNT', 'QUANTITY', 'PRICE', 'REMARK']
        Toplevel.__init__(self, bg=_bg_color)
        self._db = _db
        self._items_repo = ItemsRepositoryImpl(ItemsDaoImpl(_db))
        self._products_repo = ProductsRepositoryImpl(ProductsDaoImpl(_db))
        self._sales_order_repo = SalesOrdersRepositoryImpl(SalesOrdersDaoImpl(_db))
        self._presenter = DeliveryOrderManageFormPresenter(
            _mView=self, _review_order_usecase=ReviewOrderUsecase(self._sales_order_repo),
            _display_items_wrt_products_usecase=DisplayItemsWrtProductsUsecase(self._items_repo),
            _get_product_usecase=GetProductUsecase(self._products_repo),
            _update_order_usecase=UpdateOrderUsecase(self._sales_order_repo)
        )
        self._order_id = _order_id
        self._save_order_state = _save_order_state
        self._lf_domf_order_info = LabelFrame(self, text='ORDER INFO')

        self._f_domf_company_info = Frame(self._lf_domf_order_info)
        self._cb_domf_companies = ttk.Combobox(self._f_domf_company_info, state="readonly")
        self._lbl_domf_address = Label(self._f_domf_company_info)
        self._lbl_domf_contact = Label(self._f_domf_company_info)
        self.lbl_serial_no_label = Label(self._f_domf_company_info, text='MACHINE SERIAL NO')
        self._lbl_domf_serial_no = Label(self._f_domf_company_info)
        self.lbl_installed_date_label = Label(self._f_domf_company_info, text='INSTALLED DATE')
        self.lbl_installed_date = Label(self._f_domf_company_info)

        self._f_domf_extra_info = Frame(self._lf_domf_order_info)
        self._lbl_domf_date = Label(self._f_domf_extra_info, text=datetime.datetime.now().strftime('%d-%m-%Y'))
        self._lbl_domf_order_id = Label(self._f_domf_extra_info, text=f'{_order_id}')
        self._lbl_domf_order_total = Label(self._f_domf_extra_info, text='0')

        self._f_domf_order_fillup_layout = Frame(self)
        self._tv_domf_order_details = ttk.Treeview(self._f_domf_order_fillup_layout, columns=self._tree_columns[0:],
                                                   show='headings', selectmode=BROWSE,
                                                   takefocus=False, height=20)

        self._f_domf_order_extra_layout = Frame(self._f_domf_order_fillup_layout)
        self._lf_domf_order_item_info = LabelFrame(self._f_domf_order_extra_layout, text='ORDER ITEM INFO')
        self._ccb_domf_order_item_desc = CustomComboBox(self._lf_domf_order_item_info, state='readonly', values={})
        self._e_domf_order_item_measurement = Entry(self._lf_domf_order_item_info)
        self._lb_domf_order_item_unit_price = Label(self._lf_domf_order_item_info, text='UNIT PRICE')
        self._e_domf_order_item_unit_price = Entry(self._lf_domf_order_item_info)
        self._e_domf_order_item_qty = Entry(self._lf_domf_order_item_info)
        self._e_domf_order_item_remark = Entry(self._lf_domf_order_item_info)
        self._btn_domf_update_order_item = ttk.Button(self._lf_domf_order_item_info)
        self._btn_domf_delete_order_item = ttk.Button(self._lf_domf_order_item_info, text='DELETE')

        self._btn_domf_order_save = ttk.Button(self._f_domf_order_extra_layout, text='SAVE')

        self._create_views(master)
        self._bind_events()

        self._presenter.on_review_order(_order_id)

    def _create_views(self, master):
        """Show all initial views on Toplevel"""
        self.grid_anchor(CENTER)
        self.wm_geometry(
            f'{(self.winfo_screenwidth() // 2) + 250}x{(self.winfo_screenheight() // 2) + 150}+{1460 // 5}+{720 // 5}')
        self.wm_transient(master)
        self.grab_set()

        self._lf_domf_order_info.pack(fill=X, side=TOP, ipadx=10, ipady=10, padx=5, pady=5)
        self._f_domf_company_info.pack(side=LEFT, anchor=CENTER, expand=True)
        self._f_domf_extra_info.pack(side=RIGHT, anchor=CENTER, expand=True)
        Label(self._f_domf_company_info, text='COMPANY NAME').grid(row=0, column=0, sticky=W)
        self._cb_domf_companies.grid(row=0, column=1)
        Label(self._f_domf_company_info, text='ADDRESS').grid(row=1, column=0, sticky=W)
        self._lbl_domf_address.grid(row=1, column=1)
        Label(self._f_domf_company_info, text='CUSTOMER CONTACT').grid(row=3, column=0, sticky=W)
        self._lbl_domf_contact.grid(row=3, column=1)

        Label(self._f_domf_extra_info, text='DATE').grid(row=0, column=0, sticky=W)
        self._lbl_domf_date.grid(row=0, column=1, sticky=EW)
        Label(self._f_domf_extra_info, text='ORDER ID').grid(row=1, column=0, sticky=W)
        self._lbl_domf_order_id.grid(row=1, column=1, sticky=EW)
        Label(self._f_domf_extra_info, text='TOTAL AMOUNT').grid(row=2, column=0, sticky=W)
        self._lbl_domf_order_total.grid(row=2, column=1, sticky=EW)

        self._tv_domf_order_details.heading('#1', text=self._tree_columns[0], anchor=CENTER)
        self._tv_domf_order_details.heading('#2', text=self._tree_columns[1], anchor=CENTER)
        self._tv_domf_order_details.heading('#3', text=self._tree_columns[2], anchor=CENTER)
        self._tv_domf_order_details.heading('#4', text=self._tree_columns[3], anchor=CENTER)
        self._tv_domf_order_details.heading('#5', text=self._tree_columns[4], anchor=CENTER)
        self._tv_domf_order_details.heading('#6', text=self._tree_columns[5], anchor=CENTER)

        self._tv_domf_order_details.column('#1', width=50, stretch=YES, anchor=E, minwidth=50)
        self._tv_domf_order_details.column('#2', width=250, stretch=YES, anchor=W, minwidth=250)
        self._tv_domf_order_details.column('#3', width=100, stretch=YES, anchor=W, minwidth=100)
        self._tv_domf_order_details.column('#4', width=100, stretch=YES, anchor=E, minwidth=100)
        self._tv_domf_order_details.column('#5', width=150, stretch=YES, anchor=E, minwidth=150)
        self._tv_domf_order_details.column('#6', width=200, stretch=YES, anchor=W, minwidth=200)

        self._f_domf_order_fillup_layout.pack(fill=BOTH, expand=True)

        self._tv_domf_order_details.pack(fill=BOTH, side=LEFT, expand=True)

        Label(self._lf_domf_order_item_info, text='DESCRIPTION').grid(row=0, column=0, sticky='nsew', padx=10, pady=10)
        self._ccb_domf_order_item_desc.grid(row=0, column=1, sticky=NSEW, padx=10, pady=10)

        Label(self._lf_domf_order_item_info, text='MEASUREMENT').grid(row=1, column=0, sticky=NSEW, padx=10, pady=10)
        self._e_domf_order_item_measurement.grid(row=1, column=1, sticky=NSEW, padx=10, pady=10)

        Label(self._lf_domf_order_item_info, text=QUANTITY_LABEL).grid(row=3, column=0, sticky=NSEW, padx=10, pady=10)
        self._e_domf_order_item_qty.grid(row=3, column=1, sticky=NSEW, padx=10, pady=10)
        Label(self._lf_domf_order_item_info, text='REMARK').grid(row=4, column=0, sticky=NSEW, padx=10, pady=10)
        self._e_domf_order_item_remark.grid(row=4, column=1, sticky=NSEW, padx=10, pady=10)
        self._btn_domf_update_order_item.grid(row=5, column=1, padx=10, pady=10)

        self.update_idletasks()
        print(f"DO Form Before: {self.master.winfo_geometry()}")

    def show_company_data(self, _company):
        self._cb_domf_companies.set(_company.name)
        self._lbl_domf_address['text'] = _company.address
        self._lbl_domf_serial_no['text'] = _company.serial_no
        self._lbl_domf_contact['text'] = _company.phno

        if _company.installed_date is not None and _company.installed_date != '':
            self.lbl_serial_no_label.grid(row=4, column=0, sticky=W, pady=10)
            self._lbl_domf_serial_no.grid(row=4, column=1, sticky=W)
            self.lbl_installed_date_label.grid(row=5, column=0, sticky=W, pady=10)
            self.lbl_installed_date.grid(row=5, column=1, sticky=W)
            self.lbl_installed_date['text'] = _company.installed_date

    def _bind_events(self):
        """Bind all events in order delivery form"""

        self._tv_domf_order_details.bind(TREEVIEW_SELECT_EVENT, self._tv_domf_order_details_select_event)
        self._btn_domf_update_order_item.bind(BUTTON_EVENT, self._btn_domf_update_order_item_click_event)
        self._btn_domf_order_save.bind(BUTTON_EVENT, self._btn_domf_order_save_click_event)

    def _cb_company_click_event(self, event):
        self._cb_domf_companies.configure(state=DISABLED)
        self.update_idletasks()
        print(f"DO Form After: {self.master.winfo_x()} & {self.master.winfo_y()}")

        ItemsListForm(self, self._db, self._cb_selection_company_event,
                      self.master.winfo_x() + event.widget.winfo_x(),
                      self.master.winfo_y() + event.widget.winfo_y())

    def _cb_selection_company_event(self, company):
        """State that one company is selected"""

        if company is not None:
            self._cb_domf_companies.configure(state="readonly")

            self.lbl_installed_date.grid_forget()
            self.lbl_installed_date_label.grid_forget()
            self._lbl_domf_serial_no.grid_forget()
            self.lbl_serial_no_label.grid_forget()

            self._company = company
            self.show_company_data(self._company)

            self._cart_list = {}
            self._in_cart_order_product_id_list = []
            self._tv_domf_order_details.delete(*self._tv_domf_order_details.get_children())

            self._presenter.on_load_items_wrt_products()

            self._btn_domf_order_save.grid_forget()

        else:
            self._cb_domf_companies.configure(state="readonly")

    def _ccb_domf_order_item_desc_select_event(self, event):
        self._presenter.on_load_product(event.widget.get().item_code)

    def _btn_domf_order_item_delete_click_event(self, event):
        """Event that delete individual tree view item"""

        _selected_id = self._tv_domf_order_details.focus()
        if _selected_id:
            self._cart_list.pop(_selected_id)
            self._tv_domf_order_details.delete(_selected_id)
            self._presenter.on_load_items_wrt_products()

    # todo remove unwanted func;
    def _export_pdf_event(self):
        """Event that export pdf file"""

        filename = filedialog.asksaveasfilename(parent=self, initialdir="/",
                                                title=f"Select file : {self.order.company.name} {self.order.date}",
                                                filetypes=[('pdf file', '*.pdf')])
        if filename:
            CustomPDF(name=f"{filename}.pdf", size=A4, _expected_sale_id=self.order.id,
                      _sale_date=self.order.date, _items=self.order.items, _company=self.order.company,
                      _approved_by=self._users.get(self.order.approved_by).name,
                      _sell_by=self._users.get(self.order.sell_by).name,
                      image_path="images/logo_color.png").generate()

    def _btn_domf_order_save_click_event(self, event):
        """Event that handles all case when order save button is clicked"""
        self._deleted_order_products = list(set(self._in_cart_order_product_id_list) - set([order_product.id for order_product in self._cart_list.values()]))
        self._presenter.on_save_btn_clicked(self._order_id, self._company, datetime.datetime.now().strftime('%Y-%m-%d'),
                                            OrderStatus.PENDING.value,
                                            self._cart_list.values(), self._deleted_order_products)

    def _tv_domf_order_details_select_event(self, event):
        """Event that handles all cases when order is selected"""
        if event.widget.focus() != '':
            _order_product = self._cart_list[event.widget.focus()]
            self._presenter.on_load_product(_order_product.item.item_code)
            self._ccb_domf_order_item_desc.set(_order_product.item.name)
            self._e_domf_order_item_measurement.delete(0, END)
            self._e_domf_order_item_measurement.insert(END, _order_product.item.measurement)
            self._e_domf_order_item_qty.delete(0, END)
            self._e_domf_order_item_qty.insert(END, _order_product.qty)
            self._e_domf_order_item_remark.delete(0, END)
            self._e_domf_order_item_remark.insert(END, _order_product.remark)
            self._btn_domf_update_order_item['text'] = 'UPDATE'
            if self._company.customer_type == CustomerType.SPECIAL.value:
                self._e_domf_order_item_unit_price.delete(0, END)
                self._e_domf_order_item_unit_price.insert(END, _order_product.unit_price)

            self._btn_domf_delete_order_item.grid(row=5, column=0, padx=10, pady=10)
            self._btn_domf_delete_order_item.bind(BUTTON_EVENT, self._btn_domf_order_item_delete_click_event)

    def _btn_domf_update_order_item_click_event(self, event):
        """Event that handles all cases when update order item button is clicked"""
        _selected_id = self._tv_domf_order_details.focus()

        if self._product and self._e_domf_order_item_qty.get().isnumeric():
            if self._company.customer_type == CustomerType.NORMAL.value:
                _unit_price = self._product.local_price if (
                        self._product.defined_qty == '' or int(self._e_domf_order_item_qty.get()) < self._product.defined_qty) else (
                    self._product.distributor_price if int(self._e_domf_order_item_qty.get()) >= self._product.defined_qty else self._product.local_price)

                if _selected_id:
                    _order_id = self._cart_list[_selected_id].id
                    self._tv_domf_order_details.item(_selected_id, values=(
                        '', self._product.item.name, self._product.item.measurement, self._e_domf_order_item_qty.get(),
                        _unit_price, self._e_domf_order_item_remark.get()))
                    print(f'unit price {_unit_price}')
                    self._cart_list[_selected_id] = OrderProduct(_order_id, _unit_price,
                                                                 int(self._e_domf_order_item_qty.get()),
                                                                 self._product.defined_qty,
                                                                 self._e_domf_order_item_remark.get(),
                                                                 self._product.item)
                else:
                    print(f'unit price {_unit_price}')
                    self._cart_list[self._tv_domf_order_details.insert('', END, values=(
                        '', self._product.item.name, self._product.item.measurement, self._e_domf_order_item_qty.get(),
                        _unit_price, self._e_domf_order_item_remark.get()))] = OrderProduct(None, _unit_price,
                                                                                            int(self._e_domf_order_item_qty.get()),
                                                                                            self._product.defined_qty,
                                                                                            self._e_domf_order_item_remark.get(),
                                                                                            self._product.item)
                self._presenter.on_load_items_wrt_products()

            elif self._e_domf_order_item_unit_price.get().isnumeric():

                if _selected_id:
                    _order_id = self._cart_list[_selected_id].id
                    self._tv_domf_order_details.item(_selected_id, values=(
                        '', self._product.item.name, self._product.item.measurement, self._e_domf_order_item_qty.get(),
                        self._e_domf_order_item_unit_price.get(),
                        self._e_domf_order_item_remark.get()))
                    print(f'unit price {self._e_domf_order_item_unit_price.get()}')
                    self._cart_list[_selected_id] = OrderProduct(_order_id, int(self._e_domf_order_item_unit_price.get()),
                                                                 int(self._e_domf_order_item_qty.get()),
                                                                 self._product.defined_qty,
                                                                 self._e_domf_order_item_remark.get(),
                                                                 self._product.item)
                else:
                    print(f'unit price {self._e_domf_order_item_unit_price.get()}')
                    self._cart_list[self._tv_domf_order_details.insert('', END, values=(
                        '', self._product.item.name, self._product.item.measurement, self._e_domf_order_item_qty.get(),
                        self._e_domf_order_item_unit_price.get(),
                        self._e_domf_order_item_remark.get()))] = OrderProduct(None,
                                                                               int(self._e_domf_order_item_unit_price.get()),
                                                                               int(self._e_domf_order_item_qty.get()),
                                                                               self._product.defined_qty,
                                                                               self._e_domf_order_item_remark.get(),
                                                                               self._product.item)
                self._presenter.on_load_items_wrt_products()
            else:
                # todo show message to input data correctly
                messagebox.showerror(NO_DATA_INPUT_ERROR, NO_DATA_INPUT_ERROR_MESSAGE)
        else:
            # todo show message to enter data correctly
            messagebox.showerror(NUMBER_ERROR, INPUT_NUMBER_ERROR_MESSAGE % QUANTITY_LABEL)
