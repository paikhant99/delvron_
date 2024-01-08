from views.items_manage.items_manage_contract import ItemsManageFormContract


class ItemsManageFormPresenter(ItemsManageFormContract.Presenter):

    def __init__(self, _mView, _display_items_usecase, _display_products_usecase, _save_item_usecase, _save_product_usecase, _remove_product_usecase):
        self._mView = _mView
        self._display_items_usecase = _display_items_usecase
        self._display_products_usecase = _display_products_usecase
        self._save_item_usecase = _save_item_usecase
        self._save_product_usecase = _save_product_usecase
        self._remove_product_usecase = _remove_product_usecase

    def on_load_items(self):
        self._display_items_usecase().subscribe(on_next=self._mView.show_items)

    def on_load_products(self):
        self._display_products_usecase().subscribe(on_next=self._mView.show_products)

    def on_save_item_btn_click(self, _item, _item_desc, _item_measurement):
        self._save_item_usecase(_item, _item_desc, _item_measurement).subscribe(on_next=self._mView.show_save_item_completed, on_error=self._mView.show_save_item_error)

    def on_save_product_btn_click(self, _existed_products, _item, _local_price, _distributor_price, _defined_qty, _product_id):
        self._save_product_usecase(_existed_products, _item, _local_price, _distributor_price, _defined_qty, _product_id).subscribe(on_next=self._mView.show_save_product_completed, on_error=self._mView.show_save_product_error)

    def on_remove_product_btn_click(self, _product_id):
        self._remove_product_usecase(_product_id)