from views.receipts_manage.receipts_manage_form_contract import ReceiptsManageFormContract


class ReceiptsManageFormPresenter(ReceiptsManageFormContract.Presenter):

    def __init__(self, _mView, _get_all_receipts_by_date_and_customer_usecase, _display_one_sale_and_receipts_usecase, _insert_one_receipt_usecase, _update_balance_on_sale_id_usecase):
        self._mView = _mView
        self._get_all_receipts_by_date_and_customer_usecase = _get_all_receipts_by_date_and_customer_usecase
        self._display_one_sale_and_receipts_usecase = _display_one_sale_and_receipts_usecase
        self._insert_one_receipt_usecase = _insert_one_receipt_usecase
        self._update_balance_on_sale_id_usecase = _update_balance_on_sale_id_usecase

    def on_load_all_receipts_by_date_and_customer(self, _customer_id, _date):
        self._get_all_receipts_by_date_and_customer_usecase(_customer_id, _date).subscribe(on_next=self._mView.show_all_receipts)

    def on_load_one_sale_and_receipts(self, _sale_id):
        self._display_one_sale_and_receipts_usecase(_sale_id).subscribe(on_next=self._mView.show_one_sale_and_receipts)

    def on_save_receipt_click(self, _sale_id, _company_id, _total_sale, _received_amt, _balance, _received_date, _remark):
        self._insert_one_receipt_usecase(_sale_id, _company_id, _total_sale, _received_amt, _balance, _received_date, _remark).subscribe(on_next=self._mView.show_save_receipt_completed, on_error=self._mView.show_save_receipt_error)

    def on_update_balance(self, _balance, _sale_id):
        self._update_balance_on_sale_id_usecase(_balance, _sale_id).subscribe(on_next=self._mView.show_update_balance)
