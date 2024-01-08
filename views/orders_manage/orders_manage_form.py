from tkinter import *

from customs import *

from tkinter import messagebox

from business.usecases import DisplayOrdersUsecase, UpdateOrderStatusUsecase

from business.models import OrderStatus

from persistence.repository import SalesOrdersRepositoryImpl
from persistence.dao import SalesOrdersDaoImpl

from constants import BG_COLOR, BUTTON_EVENT, TREEVIEW_SELECT_EVENT, CUSTOMERS_FORM, ITEMS_FORM, RECEIPTS_FORM, \
    EMPLOYEES_FORM, PREFERENCES_FORM, CONFIRMATION_TAG, CONFIRMATED_QUESTION, CREATE_LABEL, UPDATE_LABEL, DELIVER_LABEL, \
    CANCEL_LABEL

from views.custom_top_level_form import CustomToplevelForm
from views.delivery_order_manage.delivery_order_manage_form import DeliveryOrderManageForm
from views.delivery_order_preview.delivery_order_preview_form import DeliveryOrderPreviewForm
from views.sales_list.sales_list_form import SalesListForm

from views.orders_manage.orders_manage_form_presenter import OrdersManageFormPresenter
from views.orders_manage.orders_manage_form_contract import OrdersManageFormContract


class OrdersManageForm(Frame, OrdersManageFormContract.View):

    def showOrders(self, orders):
        self.show_idle_state()

        self._tv_omf_orders.delete(*self._tv_omf_orders.get_children())
        if orders:
            self._last_order_id = orders[-1].id
            orders.reverse()
            self._orders = {}
            for order in orders:
                _tv_item_id = self._tv_omf_orders.insert('', END, iid=order.id, open=False, values=(
                    order.id, order.company.id, order.company.name, len(order.order_products), order.status,
                    order.order_date))
                self._orders[_tv_item_id] = order
                if order.status == OrderStatus.PENDING.value:
                    self._tv_omf_orders.item(_tv_item_id, tags=(f"tag_{_tv_item_id}_STATUS",))
                    self._tv_omf_orders.tag_configure(f"tag_{_tv_item_id}_STATUS", foreground="green")
                    # self._tv_omf_orders.tag_add(f"tag_{item_id}_{column}", item_id)
                for order_product in order.order_products:
                    self._tv_omf_orders.insert(order.id, END, values=(
                    '', order_product.item.item_code, order_product.item.name, order_product.qty,
                    order_product.unit_price, f"{int(order_product.qty) * int(order_product.unit_price)} Ks"))

        else:
            self._last_order_id = -1

    def _refresh_orders_state(self):
        self._presenter.onLoadOrders()

    def show_idle_state(self):
        self._tv_omf_orders.focus('')
        self._tv_omf_orders.selection_remove(*self._tv_omf_orders.get_children())
        self._btn_update_order.pack_forget()
        self._btn_deliver_order.pack_forget()
        self._btn_cancel_order.pack_forget()
        self._btn_update_order.unbind(BUTTON_EVENT)
        self._btn_deliver_order.unbind(BUTTON_EVENT)
        self._btn_cancel_order.unbind(BUTTON_EVENT)

    def __init__(self, _db, _admin_id):
        Frame.__init__(self, bg=BG_COLOR)
        self._db = _db
        self._sales_orders_repo = SalesOrdersRepositoryImpl(SalesOrdersDaoImpl(_db))
        self._presenter = OrdersManageFormPresenter(_mView=self, _display_orders_usecase=DisplayOrdersUsecase(self._sales_orders_repo), _update_orderstatus_usecase=UpdateOrderStatusUsecase(self._sales_orders_repo))
        self._admin_id = _admin_id
        self._tree_headings_orders = ['ORDER ID', 'CUSTOMER CODE', 'CUSTOMER NAME', 'Order QTY', 'STATUS',
                                      'DATE & TIME']

        self.menu = Menu(self.master)
        self.manageMenu = Menu(self.menu, tearoff=False)
        self.viewMenu = Menu(self.menu, tearoff=False)
        self.settingsMenu = Menu(self.menu, tearoff=False)

        self._sc_orders = ttk.Scrollbar(self, orient=VERTICAL)
        self._tv_omf_orders = ttk.Treeview(self, columns=self._tree_headings_orders[0:], show='headings',
                                           selectmode=BROWSE,
                                           takefocus=False, height=30, yscrollcommand=self._sc_orders.set)
        for i in range(len(self._tree_headings_orders)):
            self._tv_omf_orders.heading(f'#{i + 1}', text=self._tree_headings_orders[i], anchor=CENTER)
        self._tv_omf_orders.column('#1', width=100, minwidth=100, stretch=YES, anchor=E)
        self._tv_omf_orders.column('#2', width=150, minwidth=150, stretch=YES, anchor=W)
        self._tv_omf_orders.column('#3', width=250, minwidth=250, stretch=YES, anchor=W)
        self._tv_omf_orders.column('#4', width=100, minwidth=100, stretch=YES, anchor=E)
        self._tv_omf_orders.column('#5', width=100, minwidth=100, stretch=YES, anchor=W)
        self._tv_omf_orders.column('#6', width=200, minwidth=200, stretch=YES, anchor=W)

        self._frame_btn_cdc = Frame(self)
        self._btn_create_order = Button(self._frame_btn_cdc, text=CREATE_LABEL)
        self._btn_update_order = Button(self._frame_btn_cdc, text=UPDATE_LABEL)
        self._btn_deliver_order = Button(self._frame_btn_cdc, text=DELIVER_LABEL)
        self._btn_cancel_order = Button(self._frame_btn_cdc, text=CANCEL_LABEL)

        self._create_views()
        self._bind_events()

        self._presenter.onLoadOrders()

    def _create_views(self):
        self.master.configure(menu=self.menu)
        self.menu.add_cascade(label="Manage", menu=self.manageMenu)
        self.menu.add_cascade(label="View", menu=self.viewMenu)

        self.manageMenu.add_command(label="Customers", command=self._menu_customers_click_event)
        self.manageMenu.add_command(label="Items", command=self._menu_items_click_event)
        self.manageMenu.add_command(label="Receipts", command=self._menu_omf_receipts_click_event)
        self.manageMenu.add_command(label="Employees", command=self._menu_employees_click_event)
        self.manageMenu.add_separator()
        self.manageMenu.add_command(label="Preferences", command=self._menu_preferences_click_event)
        self.viewMenu.add_command(label="Sales", command=self._menu_sales_click_event)

        self._sc_orders.configure(command=self._tv_omf_orders.yview)
        self._sc_orders.pack(side=RIGHT, fill=Y)
        self._tv_omf_orders.pack(side=RIGHT, fill=Y, expand=False, anchor=CENTER, padx=10, pady=10)

        self._btn_create_order.pack(fill=BOTH, expand=True)

        self._frame_btn_cdc.pack(side=RIGHT, fill=BOTH, expand=True)

    def _bind_events(self):
        self._btn_create_order.bind(BUTTON_EVENT, self._btn_create_order_click_event)
        self._tv_omf_orders.bind(TREEVIEW_SELECT_EVENT, self._tv_omf_orders_select_event)

    def _menu_sales_click_event(self):
        print("Sale Form Must Pop up here")
        self.update_idletasks()
        print(f"DO Form After : {self.master.winfo_geometry()}")
        SalesListForm(self, BG_COLOR, self._db, self.master.winfo_x(), self.master.winfo_y())

    def _menu_preferences_click_event(self):
        self.update_idletasks()
        CustomToplevelForm(self, self.master.winfo_x(), self.master.winfo_y(), self._db, self._admin_id,
                           PREFERENCES_FORM)

    def _btn_create_order_click_event(self, event):
        print("Delivery Order Form Must Pop up here.")
        DeliveryOrderManageForm(self, self._db, BG_COLOR, self._last_order_id + 1, self._refresh_orders_state)

    def _menu_customers_click_event(self):
        self.update_idletasks()
        print(f"DO Form After: {self.master.winfo_x()} & {self.master.winfo_y()}")
        CustomToplevelForm(self, self.master.winfo_x(), self.master.winfo_y(), self._db, self._admin_id, CUSTOMERS_FORM)
        print("Customers Form Must Pop up here.")

    def _menu_items_click_event(self):
        CustomToplevelForm(self, self.master.winfo_x(), self.master.winfo_y(), self._db, self._admin_id, ITEMS_FORM)

    def _menu_employees_click_event(self):
        CustomToplevelForm(self, self.master.winfo_x(), self.master.winfo_y(), self._db, self._admin_id, EMPLOYEES_FORM)

    def _menu_omf_receipts_click_event(self):
        print("Receipt Clicked")
        CustomToplevelForm(self, self.master.winfo_x(), self.master.winfo_y(), self._db, self._admin_id, RECEIPTS_FORM)

    def _tv_omf_orders_select_event(self, event):
        print(f'{event.widget.focus()}')
        if not event.widget.focus().startswith('I') and event.widget.focus() != '':
            _order = self._orders[event.widget.focus()]
            if _order.status == OrderStatus.PENDING.value:
                self._btn_update_order.pack(fill=BOTH, expand=True)
                self._btn_deliver_order.pack(fill=BOTH, expand=True)
                self._btn_cancel_order.pack(fill=BOTH, expand=True)
                self._btn_update_order.bind(BUTTON_EVENT, self._btn_update_order_click_event)
                self._btn_deliver_order.bind(BUTTON_EVENT, self._btn_deliver_order_click_event)
                self._btn_cancel_order.bind(BUTTON_EVENT, self._btn_cancel_order_click_event)
            else:
                self._btn_update_order.pack_forget()
                self._btn_deliver_order.pack_forget()
                self._btn_cancel_order.pack_forget()
                self._btn_update_order.unbind(BUTTON_EVENT)
                self._btn_deliver_order.unbind(BUTTON_EVENT)
                self._btn_cancel_order.unbind(BUTTON_EVENT)

    def _btn_update_order_click_event(self, event):
        _order = self._orders[self._tv_omf_orders.focus()]
        DeliveryOrderManageForm(self, self._db, BG_COLOR, _order.id, self._refresh_orders_state)

    def _btn_cancel_order_click_event(self, event):
        _order = self._orders[self._tv_omf_orders.focus()]
        if messagebox.askyesno(CONFIRMATION_TAG, CONFIRMATED_QUESTION % CANCEL_LABEL):
            self._presenter.onCancelOrderBtnClick(_order.id)
            self._presenter.onLoadOrders()

    def _btn_deliver_order_click_event(self, event):
        _order = self._orders[self._tv_omf_orders.focus()]
        DeliveryOrderPreviewForm(self, self._db, self._admin_id, _order.id, self._refresh_orders_state)
