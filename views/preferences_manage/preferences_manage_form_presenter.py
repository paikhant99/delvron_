from views.preferences_manage.preferences_manage_form_contract import PreferencesManageFormContract


class PreferencesManageFormPresenter(PreferencesManageFormContract.Presenter):

    def __init__(self, _mView, _get_delvron_admin_usecase, _update_delvron_company_access_usecase, _update_delvron_sale_id_usecase, _update_delvron_admin_password_usecase):
        self._mView = _mView
        self._get_delvron_admin_usecase = _get_delvron_admin_usecase
        self._update_delvron_company_access_usecase = _update_delvron_company_access_usecase
        self._update_delvron_sale_id_usecase = _update_delvron_sale_id_usecase
        self._update_delvron_admin_password_usecase = _update_delvron_admin_password_usecase

    def on_load_admin(self, _admin_id):
        self._get_delvron_admin_usecase(_admin_id).subscribe(on_next=self._mView.show_admin)

    def on_update_company_access(self, _company_access):
        self._update_delvron_company_access_usecase(_company_access).subscribe(on_next=self._mView.show_company_access)

    def on_update_last_sale_id_btn_click(self, _last_sale_id):
        self._update_delvron_sale_id_usecase(_last_sale_id).subscribe(on_next=self._mView.show_sale_id_update_completed)

    def on_update_admin_password_btn_click(self, _admin_id, _password):
        self._update_delvron_admin_password_usecase(_password).subscribe(on_next=self._mView.show_password_update_completed)
