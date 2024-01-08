from views.customers.customers_form_contract import CustomersFormContract


class CustomersFormPresenter(CustomersFormContract.Presenter):

    def __init__(self, _mView, _get_delvron_admin_usecase, _display_customers_usecase, _update_customer_usecase, _create_customer_usecase):
        self._mView = _mView
        self._get_delvron_admin_usecase = _get_delvron_admin_usecase
        self._display_customers_usecase = _display_customers_usecase
        self._update_customer_usecase = _update_customer_usecase
        self._create_customer_usecase = _create_customer_usecase

    def on_load_customers(self, _customer_id, _customer_name):
        self._display_customers_usecase(_customer_id, _customer_name).subscribe(self._mView.show_customers)

    def on_load_admin(self, _admin_id):
        self._get_delvron_admin_usecase(_admin_id).subscribe(self._mView.show_admin)

    def on_update_customer(self, _customer_code, _customer_name, _customer_address, _customer_phno, _customer_serialno, _customer_installed_date, _customer_deactivated, _customer_type, _customer_id):
        self._update_customer_usecase(_customer_code, _customer_name, _customer_address, _customer_phno, _customer_serialno, _customer_installed_date, _customer_deactivated, _customer_type, _customer_id).subscribe(on_next=self._mView.show_customer_update_completed, on_error=self._mView.show_customer_update_error)

    def on_create_customer(self, _customer_code, _customer_name, _customer_address, _customer_phno, _customer_serialno, _customer_installed_date, _customer_deactivated, _customer_type):
        self._create_customer_usecase(_customer_code, _customer_name, _customer_address, _customer_phno, _customer_serialno, _customer_installed_date, _customer_deactivated, _customer_type).subscribe(on_next=self._mView.show_customer_add_completed, on_error=self._mView.show_customer_add_error)