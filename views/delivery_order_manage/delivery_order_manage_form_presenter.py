from views.delivery_order_manage.delivery_order_manage_form_contract import DeliveryOrderManageFormContract


class DeliveryOrderManageFormPresenter(DeliveryOrderManageFormContract.Presenter):

    def __init__(self, _mView, _review_order_usecase, _display_items_wrt_products_usecase, _get_product_usecase, _update_order_usecase):
        self._mView = _mView
        self._review_order_usecase = _review_order_usecase
        self._display_items_wrt_products_usecase = _display_items_wrt_products_usecase
        self._get_product_usecase = _get_product_usecase
        self._update_order_usecase = _update_order_usecase

    def on_review_order(self, _order_id):
        self._review_order_usecase(_order_id).subscribe(on_next=self._mView.show_order_reviewed)

    def on_load_items_wrt_products(self):
        self._display_items_wrt_products_usecase().subscribe(on_next=self._mView.show_items_wrt_products)

    def on_load_product(self, _item_code):
        self._get_product_usecase(_item_code).subscribe(on_next=self._mView.show_product)

    def on_save_btn_clicked(self, _order_id, _company, _created_date, _order_status, _cart_list, _deleted_order_products):
        self._update_order_usecase( _order_id, _company, _created_date, _order_status, _cart_list, _deleted_order_products).subscribe(on_next=self._mView.show_ordering_completed, on_error=self._mView.show_ordering_error)
