from abc import ABC, abstractmethod

class PreferencesManageFormContract(ABC):

    class View(ABC):

        @abstractmethod
        def show_admin(self, _admins): pass

        @abstractmethod
        def show_company_access(self, _update_count): pass

        @abstractmethod
        def show_sale_id_update_completed(self, _completed): pass

        @abstractmethod
        def show_password_update_completed(self, _admin_id): pass

    class Presenter(ABC):

        @abstractmethod
        def on_load_admin(self, _admin_id): pass

        @abstractmethod
        def on_update_company_access(self, _company_access): pass

        @abstractmethod
        def on_update_last_sale_id_btn_click(self, _last_sale_id): pass

        @abstractmethod
        def on_update_admin_password_btn_click(self, _admin_id, _password): pass