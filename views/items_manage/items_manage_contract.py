from abc import ABC, abstractmethod

class ItemsManageFormContract(ABC):

    class View(ABC):

        @abstractmethod
        def show_products(self, _products): pass

        @abstractmethod
        def show_items(self, _items): pass

        @abstractmethod
        def show_save_item_completed(self, _completed): pass

        @abstractmethod
        def show_save_item_error(self, _error): pass

        @abstractmethod
        def show_save_product_completed(self, _completed): pass

        @abstractmethod
        def show_save_product_error(self, _error): pass

    class Presenter(ABC):

        @abstractmethod
        def on_load_items(self): pass

        @abstractmethod
        def on_load_products(self): pass

        @abstractmethod
        def on_save_item_btn_click(self, _item, _item_desc, _item_measurement): pass

        @abstractmethod
        def on_save_product_btn_click(self, _existed_products, _item, _local_price, _distributor_price, _defined_qty, _product_id): pass

        @abstractmethod
        def on_remove_product_btn_click(self, _product_id): pass
