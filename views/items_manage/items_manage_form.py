from tkinter import *
from customs import *

from constants import TREEVIEW_SELECT_EVENT, BUTTON_EVENT, NO_DATA_INPUT_ERROR, UNKNOWN_ERROR, NUMBER_ERROR, REPEATED_ERROR, REPEATED_ERROR_MESSAGE

from business.usecases import DisplayItemsUsecase, SaveItemUsecase, DisplayProductsUsecase, SaveProductUsecase, RemoveProductUsecase
from business.models import Item
from persistence.repository import ProductsRepositoryImpl, ItemsRepositoryImpl
from persistence.dao import ItemsDaoImpl, ProductsDaoImpl

from tkinter import messagebox

from views.items_manage.items_manage_contract import ItemsManageFormContract
from views.items_manage.items_manage_form_presenter import ItemsManageFormPresenter


class ItemsManageForm(Frame, ItemsManageFormContract.View):

    def show_save_product_error(self, e):
        if e.args[0] == REPEATED_ERROR:
            messagebox.showerror(REPEATED_ERROR, REPEATED_ERROR_MESSAGE)
        elif e.args[0] == NO_DATA_INPUT_ERROR:
            messagebox.showerror(NO_DATA_INPUT_ERROR, e.args[0])
        else:
            messagebox.showerror(UNKNOWN_ERROR, e.args[0])

    def show_save_product_completed(self, last_id):
        if last_id:
            self._lb_imf_product_name['text'] = ''
            self._e_imf_product_local_price.delete(0, END)
            self._e_imf_product_distributor_price.delete(0, END)
            self._e_imf_product_defined_qty.delete(0, END)
            self._presenter.on_load_products()

    def show_products(self, _products):
        self._products = {}
        self._lb_imf_product_name['text'] = ''
        self._e_imf_product_local_price.delete(0, END)
        self._e_imf_product_distributor_price.delete(0, END)
        self._e_imf_product_defined_qty.delete(0, END)
        self._f_products_btn_layout._btn_imf_delete_product.grid_remove()
        self._f_products_btn_layout._btn_imf_delete_product.unbind(BUTTON_EVENT)
        self._tv_products.delete(*self._tv_products.get_children())
        if _products:
            _products.reverse()
            self._products = {self._tv_products.insert('', END, values=(_product.item.name, _product.item.measurement, _product.local_price, _product.distributor_price, _product.defined_qty)): _product for _product in _products}

    def show_save_item_completed(self, completed):
        """State that item creation procedure is completed"""
        if bool(completed):
            self.after(100, lambda: self.hide_buttons())
            self._presenter.on_load_items()

    def show_save_item_error(self, e):
        if e.args[0] == NO_DATA_INPUT_ERROR:
            messagebox.showerror(NO_DATA_INPUT_ERROR, "Data is Empty")
        elif e.args[0] == NUMBER_ERROR:
            messagebox.showerror(NUMBER_ERROR, "Check your fields. They should be numeric.")
        else:
            messagebox.showerror(UNKNOWN_ERROR, e.args[0])

    def __init__(self, master, _db):
        Frame.__init__(self, master)
        self._products_repo = ProductsRepositoryImpl(ProductsDaoImpl(_db))
        self._items_repo = ItemsRepositoryImpl(ItemsDaoImpl(_db))
        self._presenter = ItemsManageFormPresenter(
            _mView=self, _display_items_usecase=DisplayItemsUsecase(self._items_repo),
            _display_products_usecase=DisplayProductsUsecase(self._products_repo),
            _save_item_usecase=SaveItemUsecase(self._items_repo),
            _save_product_usecase=SaveProductUsecase(self._products_repo),
            _remove_product_usecase=RemoveProductUsecase(self._products_repo)
        )
        self._items_tree_columns = ['ITEM CODE', 'ITEM NAME', 'UNIT MEASUREMENT']
        self._products_tree_columns = ['DESCRIPTION', 'MEASUREMENT', 'LOCAL PRICE', 'DISTRIBUTOR PRICE', 'DEFINED QTY']

        self.lf_items = LabelFrame(self, text="Items")
        self.e_item_desc = Entry(self.lf_items)
        self.e_item_desc.focus()
        self.e_measurement = Entry(self.lf_items)
        self._f_items_list = Frame(self.lf_items)
        self._sc_items = ttk.Scrollbar(self._f_items_list, orient=VERTICAL)
        self._tv_items = ttk.Treeview(self._f_items_list, columns=self._items_tree_columns, show='headings', selectmode=BROWSE, yscrollcommand=self._sc_items.set)

        self.f_items_btn_layout = Frame(self.lf_items)
        self.f_items_btn_layout.btn_new_item = Button(self.f_items_btn_layout, text='New')
        self.f_items_btn_layout.btn_save_item = Button(self.f_items_btn_layout, text='Save')

        self.lf_products = LabelFrame(self, text="Products")
        self._lb_imf_product_name = Label(self.lf_products)
        self._e_imf_product_local_price = Entry(self.lf_products)
        self._e_imf_product_distributor_price = Entry(self.lf_products)
        self._e_imf_product_defined_qty = Entry(self.lf_products)

        self._f_products_list = Frame(self.lf_products)
        self._sc_products = ttk.Scrollbar(self._f_products_list, orient=VERTICAL)
        self._tv_products = ttk.Treeview(self._f_products_list, columns=self._products_tree_columns[0:], show='headings', selectmode=BROWSE, yscrollcommand=self._sc_products.set)

        self._f_products_btn_layout = Frame(self.lf_products)
        self._f_products_btn_layout._btn_imf_save_product = Button(self._f_products_btn_layout, text='SAVE')
        self._f_products_btn_layout._btn_imf_delete_product = Button(self._f_products_btn_layout, text='DELETE')
        self.create_views(master)
        self.bind_events()

        self.item = None
        self._presenter.on_load_items()
        self._presenter.on_load_products()

    def create_views(self, master):

        Label(self.lf_items, text="Description").grid(row=0, column=0, sticky=NSEW, padx=10, pady=10)
        self.e_item_desc.grid(row=0, column=1, sticky=NSEW, padx=10, pady=10)
        Label(self.lf_items, text="Measurement").grid(row=1, column=0, sticky=NSEW, padx=10, pady=10)
        self.e_measurement.grid(row=1, column=1, sticky=NSEW, padx=10, pady=10)

        Label(self.lf_products, text="Distributor Price").grid(row=0, column=2, sticky=W, padx=10, pady=10)
        self._e_imf_product_distributor_price.grid(row=0, column=3, sticky=W, padx=10, pady=10)
        Label(self.lf_products, text="Defined Qty").grid(row=1, column=2, sticky=W, padx=10, pady=10)
        self._e_imf_product_defined_qty.grid(row=1, column=3, sticky=W, padx=10, pady=10)

        self.f_items_btn_layout.grid(row=4, column=1, columnspan=2, sticky=NSEW, padx=10, pady=10)
        self.f_items_btn_layout.btn_save_item.grid(row=0, column=1, sticky=E)

        self._sc_items.configure(command=self._tv_items.yview)
        self._sc_items.pack(side=RIGHT, fill=BOTH)

        self._tv_items.heading('#1', text=self._items_tree_columns[0], anchor=CENTER)
        self._tv_items.heading('#2', text=self._items_tree_columns[1], anchor=CENTER)
        self._tv_items.heading('#3', text=self._items_tree_columns[2], anchor=CENTER)
        self._tv_items.column('#1', stretch=YES, width=100, minwidth=100, anchor=W)
        self._tv_items.column('#2', stretch=YES, width=250, minwidth=250, anchor=W)
        self._tv_items.column('#3', stretch=YES, width=150, minwidth=150, anchor=W)
        self._tv_items.pack(side=LEFT, fill=BOTH)
        self._f_items_list.grid(row=5, column=0, columnspan=5, sticky=NSEW, padx=10, pady=10)
        self.lf_items.grid(row=0, column=0, padx=10, pady=10)

        Label(self.lf_products, text="Item Desc").grid(row=0, column=0, sticky=W, padx=10, pady=10)
        self._lb_imf_product_name.grid(row=0, column=1, sticky=W, padx=10, pady=10)
        Label(self.lf_products, text="Local Price").grid(row=1, column=0, sticky=W, padx=10, pady=10)
        self._e_imf_product_local_price.grid(row=1, column=1, sticky=W, padx=10, pady=10)

        self._f_products_btn_layout.grid(row=4, column=1, sticky=W, padx=10, pady=10)
        self._f_products_btn_layout._btn_imf_save_product.grid(row=0, column=0, sticky=NSEW, padx=10, pady=10)

        self._tv_products.heading('#1', text=self._products_tree_columns[0], anchor=CENTER)
        self._tv_products.heading('#2', text=self._products_tree_columns[1], anchor=CENTER)
        self._tv_products.heading('#3', text=self._products_tree_columns[2], anchor=CENTER)
        self._tv_products.heading('#4', text=self._products_tree_columns[3], anchor=CENTER)
        self._tv_products.heading('#5', text=self._products_tree_columns[4], anchor=CENTER)
        self._tv_products.column('#1', stretch=YES, width=250, minwidth=250, anchor=W)
        self._tv_products.column('#2', stretch=YES, width=150, minwidth=150, anchor=W)
        self._tv_products.column('#3', stretch=YES, width=100, minwidth=100, anchor=E)
        self._tv_products.column('#4', stretch=YES, width=150, minwidth=150, anchor=W)
        self._tv_products.column('#5', stretch=YES, width=150, minwidth=150, anchor=E)

        self._sc_products.configure(command=self._tv_products.yview)
        self._sc_products.pack(fill=BOTH, side=RIGHT)
        self._tv_products.pack(fill=BOTH, side=LEFT)
        self._f_products_list.grid(row=5, column=0, columnspan=5, sticky=NSEW, padx=10, pady=10)
        self.lf_products.grid(row=0, column=1, padx=10, pady=10)

    def bind_events(self):
        self._tv_items.bind(TREEVIEW_SELECT_EVENT, self._tv_items_select_event)
        self.f_items_btn_layout.btn_new_item.bind(BUTTON_EVENT, self._btn_new_item_click_event)
        self.f_items_btn_layout.btn_save_item.bind(BUTTON_EVENT, self._btn_save_item_click_event)
        self._tv_products.bind(TREEVIEW_SELECT_EVENT, self._tv_products_select_event)
        self._f_products_btn_layout._btn_imf_save_product.bind(BUTTON_EVENT, self._btn_save_product_click_event)

    def show_items(self, _items):
        self._tv_items.delete(*self._tv_items.get_children())
        self.items = {self._tv_items.insert('', END, values=(item.item_code, item.name, item.measurement)): item for item in
                _items[::-1]}

    def _clear_all_items_selection(self):
        self._tv_items.focus("")
        self._tv_items.selection_remove(*self._tv_items.get_children())

    def _btn_new_item_click_event(self, event):
        """State that new button is clicked and hide new buttons and clear selections of tree
            --> avoid selection event calling not to disturb btn grid_remove statement.
        """
        self.e_item_desc.focus()
        self._lb_imf_product_name['text'] = ''
        self._clear_all_items_selection()
        event.widget.grid_remove()
        self.after(100, lambda: self.hide_buttons())

    def hide_buttons(self):
        """Hide Buttons for creating new item"""
        self.f_items_btn_layout.btn_new_item.grid_remove()

    def _btn_save_item_click_event(self, event):
        _item = self.items.get(self._tv_items.focus())
        self._presenter.on_save_item_btn_click(_item, self.e_item_desc.get(), self.e_measurement.get())

    def _tv_items_select_event(self, event):
        self.f_items_btn_layout.btn_new_item.grid(row=0, column=0, sticky=W, padx=10, pady=10)
        self.item: Item = self.items.get(self._tv_items.focus())

        self.e_item_desc.delete(0, END)
        self.e_measurement.delete(0, END)
        if self.item is not None and self.item != '':
            self._lb_imf_product_name['text'] = self.item.name
            self.e_item_desc.insert(END, self.item.name)
            self.e_measurement.insert(END, self.item.measurement)

    def _btn_save_product_click_event(self, event):
        _product = self._products.get(self._tv_products.focus())
        _existed_products = [product.item.item_code for product in self._products.values()]
        self._presenter.on_save_product_btn_click(_existed_products,
                                                  _product.item if _product else (self.item if self.item else None),
                                                  self._e_imf_product_local_price.get(),
                                                  self._e_imf_product_distributor_price.get(),
                                                  self._e_imf_product_defined_qty.get(),
                                                  _product.id if _product else _product)

    def _tv_products_select_event(self, event):
        self._product = self._products.get(event.widget.focus())
        if self._product:
            self._lb_imf_product_name['text'] = self._product.item.name
            self._e_imf_product_local_price.delete(0, END)
            self._e_imf_product_local_price.insert(END, self._product.local_price)
            self._e_imf_product_distributor_price.delete(0, END)
            self._e_imf_product_distributor_price.insert(END, self._product.distributor_price)
            self._e_imf_product_defined_qty.delete(0, END)
            self._e_imf_product_defined_qty.insert(END, self._product.defined_qty)
            self._f_products_btn_layout._btn_imf_delete_product.grid(row=0, column=1, sticky=NSEW, padx=10, pady=10)
            self._f_products_btn_layout._btn_imf_delete_product.bind(BUTTON_EVENT, self._btn_imf_delete_product_click_event)

    def _btn_imf_delete_product_click_event(self, event):
        self._presenter.on_remove_product_btn_click(self._product.id)
        self._presenter.on_load_products()
