from views.employee_administration.employee_administration_form_contract import  EmployeeAdministrationFormContract


class EmployeeAdministrationFormPresenter(EmployeeAdministrationFormContract.Presenter):

    def __init__(self, _mView, _retrieve_all_users_usecase, _get_delvron_admin_usecase, _quit_user_usecase, _save_new_user_usecase):
        self._mView = _mView
        self._retrieve_all_users_usecase = _retrieve_all_users_usecase
        self._get_delvron_admin_usecase = _get_delvron_admin_usecase
        self._quit_user_usecase = _quit_user_usecase
        self._save_new_user_usecase = _save_new_user_usecase

    def on_load_users(self):
        self._retrieve_all_users_usecase().subscribe(on_next=self._mView.show_users)

    def on_load_admin(self, _admin_id):
        self._get_delvron_admin_usecase(_admin_id).subscribe(on_next=self._mView.show_admin)

    def on_quit_user_click(self, _user_id, _quit_date):
        self._quit_user_usecase(_user_id, _quit_date).subscribe(on_next=self._mView.show_quit_user_completed)

    def on_save_new_user_click(self, _user_id, _user_name, _user_position, _start_date, _quit_date):
        self._save_new_user_usecase(_user_id, _user_name, _user_position, _start_date, _quit_date).subscribe(on_next=self._mView.show_save_user_completed, on_error=self._mView.show_save_user_error)