from business.models import OrderStatus

from views.orders_manage.orders_manage_form_contract import OrdersManageFormContract

class OrdersManageFormPresenter(OrdersManageFormContract.Presenter):

    def __init__(self, _mView, _display_orders_usecase, _update_orderstatus_usecase):
        self.mView = _mView
        self._display_orders_usecase = _display_orders_usecase
        self._update_orderstatus_usecase = _update_orderstatus_usecase

    def onLoadOrders(self):
        self._display_orders_usecase().subscribe(on_next=self.mView.showOrders)

    def onCancelOrderBtnClick(self, _order_id):
        self._update_orderstatus_usecase(OrderStatus.CANCELLED.value, _order_id)
