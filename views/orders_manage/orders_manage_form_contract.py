from abc import ABC, abstractmethod


class OrdersManageFormContract(ABC):
    class View(ABC):
        """ These methods are implemented within Orders Manage Form Class"""

        @abstractmethod
        def showOrders(self, _orders): pass

    class Presenter(ABC):
        """ These methods need to be called in Orders Manage Form Class"""

        @abstractmethod
        def onLoadOrders(self): pass

        @abstractmethod
        def onCancelOrderBtnClick(self, _order_id): pass
