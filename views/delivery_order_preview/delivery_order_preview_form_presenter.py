from business.models import OrderStatus
from views.delivery_order_preview.delivery_order_preview_form_contract import DeliveryOrderPreviewFormContract


class DeliveryOrderPreviewFormPresenter(DeliveryOrderPreviewFormContract.Presenter):

    def __init__(self, _mView, _review_order_usecase, _get_delvron_admin_usecase, _retrieve_all_active_users_usecase, _make_sale_usecase, _update_order_status_usecase, _update_delvron_sale_id_usecase):
        self._mView = _mView
        self._review_order_usecase = _review_order_usecase
        self._get_delvron_admin_usecase = _get_delvron_admin_usecase
        self._retrieve_all_active_users_usecase = _retrieve_all_active_users_usecase
        self._make_sale_usecase = _make_sale_usecase
        self._update_order_status_usecase = _update_order_status_usecase
        self._update_delvron_sale_id_usecase = _update_delvron_sale_id_usecase

    def on_review_order(self, _order_id):
        self._review_order_usecase(_order_id).subscribe(self._mView.show_order_reviewed)

    def on_load_admin(self, _admin_id):
        self._get_delvron_admin_usecase(_admin_id).subscribe(self._mView.show_admin)

    def on_load_all_active_users(self):
        self._retrieve_all_active_users_usecase().subscribe(self._mView.show_all_active_users)

    def on_make_sale_print(self, _expected_sale_id, _delivered_date, _order_id, _sell_by_id, _approved_by_id):
        self._make_sale_usecase(_expected_sale_id, _delivered_date, _order_id, _sell_by_id, _approved_by_id).subscribe(on_next=self._mView.show_make_sale_completed)

    def on_update_order_status_finished(self, _order_id):
        self._update_order_status_usecase(OrderStatus.FINISHED.value, _order_id)

    def on_update_next_sale_id_delvron_finished(self, _next_sale_id):
        self._update_delvron_sale_id_usecase(_next_sale_id).subscribe()


