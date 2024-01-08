from abc import ABC, abstractmethod


class PinLoginFormContract(ABC):

    class View(ABC):

        @abstractmethod
        def show_admin(self, _admins): pass

    class Presenter(ABC):

        @abstractmethod
        def on_load_admin(self, _admin_id): pass