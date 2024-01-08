from abc import ABC, abstractmethod


class CustomersFormContract(ABC):
    class View(ABC):

        @abstractmethod
        def show_customers(self, _companies): pass

        @abstractmethod
        def show_admin(self, _admins): pass

        @abstractmethod
        def show_customer_update_completed(self, _updated_count): pass

        @abstractmethod
        def show_customer_update_error(self, error): pass

        @abstractmethod
        def show_customer_add_completed(self): pass

        @abstractmethod
        def show_customer_add_error(self, _error): pass

    class Presenter(ABC):

        @abstractmethod
        def on_load_customers(self, _customer_id, _customer_name): pass

        @abstractmethod
        def on_load_admin(self, _admin_id): pass

        @abstractmethod
        def on_update_customer(self, _customer_code, _customer_name, _customer_address, _customer_phno, _customer_serialno, _customer_installed_date, _customer_deactivated, _customer_type, _customer_id): pass

        @abstractmethod
        def on_create_customer(self, _customer_code, _customer_name, _customer_address, _customer_phno, _customer_serialno, _customer_installed_date, _customer_deactivated, _customer_type): pass
