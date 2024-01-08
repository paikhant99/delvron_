from views.pin_login.pin_login_form_contract import PinLoginFormContract


class PinLoginFormPresenter(PinLoginFormContract.Presenter):

    def __init__(self, _mView, _get_delvron_admin_usecase):
        self._mView = _mView
        self._get_delvron_admin_usecase = _get_delvron_admin_usecase

    def on_load_admin(self, _admin_id):
        self._get_delvron_admin_usecase(_admin_id).subscribe(on_next=self._mView.show_admin)