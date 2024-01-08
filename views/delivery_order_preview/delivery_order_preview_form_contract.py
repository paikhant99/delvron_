from abc import ABC, abstractmethod

class DeliveryOrderPreviewFormContract(ABC):

    class View(ABC):

        @abstractmethod
        def show_order_reviewed(self, _order): pass

        @abstractmethod
        def show_admin(self, _admins): pass

        @abstractmethod
        def show_all_active_users(self, _users): pass

        @abstractmethod
        def show_make_sale_completed(self, _sale_id): pass

    class Presenter(ABC):

        @abstractmethod
        def on_review_order(self, _order_id): pass

        @abstractmethod
        def on_load_admin(self, _admin_id): pass

        @abstractmethod
        def on_load_all_active_users(self): pass

        @abstractmethod
        def on_make_sale_print(self, _expected_sale_id, _delivered_date, _order_id, _sell_by_id, _approved_by_id): pass

        @abstractmethod
        def on_update_order_status_finished(self, _order_id): pass

        @abstractmethod
        def on_update_next_sale_id_delvron_finished(self, _next_sale_id): pass