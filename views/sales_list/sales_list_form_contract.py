from abc import ABC, abstractmethod

class SalesListFormContract(ABC):

    class View(ABC):

        @abstractmethod
        def show_sales(self, _sales): pass

        @abstractmethod
        def show_available_items(self, _items): pass

        @abstractmethod
        def show_active_salesmen(self, _salesmen): pass

    class Presenter(ABC):

        @abstractmethod
        def on_load_sales(self, _start_date, _end_date, _selected_company, _product_name, _saleman_name): pass

        @abstractmethod
        def on_load_available_items(self): pass

        @abstractmethod
        def on_load_active_salesmen(self): pass
