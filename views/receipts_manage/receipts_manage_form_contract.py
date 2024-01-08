from abc import ABC, abstractmethod


class ReceiptsManageFormContract(ABC):

    class View(ABC):

        @abstractmethod
        def show_all_receipts(self, _receipts): pass

        @abstractmethod
        def show_one_sale_and_receipts(self, _sale): pass

        @abstractmethod
        def show_save_receipt_completed(self, _param): pass

        @abstractmethod
        def show_save_receipt_error(self, _error): pass

        @abstractmethod
        def show_update_balance(self, _rowcount): pass

    class Presenter(ABC):

        @abstractmethod
        def on_load_all_receipts_by_date_and_customer(self, _customer_id, _date): pass

        @abstractmethod
        def on_load_one_sale_and_receipts(self, _sale_id): pass

        @abstractmethod
        def on_save_receipt_click(self, _sale_id, _company_id, _total_sale, _received_amt, _balance, _received_date, _remark): pass

        @abstractmethod
        def on_update_balance(self, _balance, _sale_id): pass
    