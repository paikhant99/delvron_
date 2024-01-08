from abc import ABC, abstractmethod


class EmployeeAdministrationFormContract(ABC):

    class View(ABC):

        @abstractmethod
        def show_users(self, _users): pass

        @abstractmethod
        def show_admin(self, _admins): pass

        @abstractmethod
        def show_quit_user_completed(self, _user_count): pass

        @abstractmethod
        def show_save_user_completed(self, _user_id): pass

        @abstractmethod
        def show_save_user_error(self, _error): pass

    class Presenter(ABC):

        @abstractmethod
        def on_load_users(self): pass

        @abstractmethod
        def on_load_admin(self, _admin_id): pass

        @abstractmethod
        def on_quit_user_click(self, _user_id, _quit_date): pass

        @abstractmethod
        def on_save_new_user_click(self, _user_id, _user_name, _user_position, _start_date, _quit_date): pass
