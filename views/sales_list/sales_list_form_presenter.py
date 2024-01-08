from views.sales_list.sales_list_form_contract import SalesListFormContract


class SalesListFormPresenter(SalesListFormContract.Presenter):

    def __init__(self, _mView, _display_sales_usecase, _retrieve_all_available_items_usecase, _retrieve_all_active_salesmen_usecase):
        self._mView = _mView
        self._display_sales_usecase = _display_sales_usecase
        self._retrieve_all_available_items_usecase = _retrieve_all_available_items_usecase
        self._retrieve_all_active_salesmen_usecase = _retrieve_all_active_salesmen_usecase

    def on_load_sales(self, _start_date, _end_date, _selected_company, _product_name, _saleman_name):
        self._display_sales_usecase(_start_date, _end_date, _selected_company, _product_name, _saleman_name).subscribe(on_next=self._mView.show_sales)

    def on_load_available_items(self):
        self._retrieve_all_available_items_usecase().subscribe(on_next=self._mView.show_available_items)

    def on_load_active_salesmen(self):
        self._retrieve_all_active_salesmen_usecase().subscribe(on_next=self._mView.show_active_salesmen)