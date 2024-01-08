from abc import ABC, abstractmethod

class DeliveryOrderManageFormContract(ABC):

    class View(ABC):
        """ These methods are implemented within Delivery Order Manage Form Class"""

        @abstractmethod
        def show_order_reviewed(self, _order): pass

        @abstractmethod
        def show_items_wrt_products(self, _items): pass

        @abstractmethod
        def show_product(self, _product): pass

        @abstractmethod
        def show_ordering_completed(self, _completed): pass

        @abstractmethod
        def show_ordering_error(self, _error): pass

    class Presenter(ABC):
        """ These methods need to be called in Delivery Order Manage Form Class"""


        @abstractmethod
        def on_review_order(self, _order_id): pass

        @abstractmethod
        def on_load_items_wrt_products(self): pass

        @abstractmethod
        def on_load_product(self, _item_code): pass

        @abstractmethod
        def on_save_btn_clicked(self, _order_id, _company, _created_date, _order_status, _cart_list, _deleted_order_products): pass

