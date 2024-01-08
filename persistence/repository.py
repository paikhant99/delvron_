from abc import ABC, abstractmethod
import reactivex


class UsersRepository(ABC):

    @abstractmethod
    def get_all_users(self): pass

    @abstractmethod
    def get_all_active_users(self): pass

    @abstractmethod
    def get_all_active_specific_users_by_position(self, _position): pass

    @abstractmethod
    def update_user(self, _id, _name, _position, _start_date, _quit_date): pass

    @abstractmethod
    def update_user_quit_date(self, _user_id, _quit_date): pass


class UserAdminsRepository(ABC):

    @abstractmethod
    def update_admin_password(self, _admin_id, _password): pass

    @abstractmethod
    def get_admins(self, _admin_id): pass

    @abstractmethod
    def update_delvron_order_id(self, _order_id): pass

    @abstractmethod
    def update_delvron_company_access(self, _company_access): pass


class ItemsRepository(ABC):

    @abstractmethod
    def get_items(self): pass

    @abstractmethod
    def get_only_items_wrt_products(self): pass

    @abstractmethod
    def get_available_items(self): pass

    @abstractmethod
    def create_item(self, _item_code, _name, _measure): pass


class CustomersRepository(ABC):

    @abstractmethod
    def create_customer(self, _customer_id, _name, _address, _phno, _serial_no, _installed_date, _customer_type, _deactivated): pass

    @abstractmethod
    def update_customer(self, _customer_id, _name, _address, _phno, _serial_no, _installed_date, _customer_type, _deactivated, _index_id): pass

    @abstractmethod
    def get_customers(self, _customer_id, _customer_name): pass


class ProductsRepository(ABC):

    @abstractmethod
    def create_product(self, _product_id, _item_id, _local_price, _distributor_price, _defined_qty): pass

    @abstractmethod
    def get_products(self): pass

    @abstractmethod
    def get_product(self, _item_id): pass

    @abstractmethod
    def delete_product(self, _product_id): pass


class SalesOrderRepository(ABC):

    @abstractmethod
    def update_sales_order(self, _sales_order_id, _customer_id, _order_date, _status, _order_products,
                           _deleted_order_products): pass

    @abstractmethod
    def get_sales_orders(self): pass

    @abstractmethod
    def get_order(self, order_id): pass

    @abstractmethod
    def update_order_status(self, _status, _order_id): pass


class SalesRepository(ABC):

    @abstractmethod
    def get_last_sale_id(self): pass

    @abstractmethod
    def create_sale(self, _sale_id, _created_at, _order_id, _sell_by, _approved_by): pass

    @abstractmethod
    def get_sales(self, _start_date, _end_date, _customer_id, _item_id, _salesman_id): pass


class ReceiptsRepository(ABC):

    @abstractmethod
    def get_all_receipts_by_customer(self, _customer_id, _date): pass

    @abstractmethod
    def get_all_sales_id_by_customer(self, _customer_id, _sale_id): pass

    @abstractmethod
    def get_one_sale_and_receipts(self, _sale_id): pass

    @abstractmethod
    def insert_one_receipt(self, _sale_id, _customer_id, _sale_amount, _received_amount, _balance, _received_date, _remark): pass

    @abstractmethod
    def update_balance_on_sale_id(self, _balance, _sale_id): pass


class UsersRepositoryImpl(UsersRepository):

    def __init__(self, _users_dao):
        self._users_dao = _users_dao

    def get_all_users(self):
        return reactivex.from_callable(lambda: self._users_dao.select_all_users())

    def get_all_active_users(self):
        return reactivex.from_callable(lambda: self._users_dao.select_all_active_users(''))

    def get_all_active_specific_users_by_position(self, _position):
        return reactivex.from_callable(
            lambda: self._users_dao.select_all_active_specific_users_by_position('', _position))

    def update_user(self, _id, _name, _position, _start_date, _quit_date):
        return reactivex.from_callable(lambda: self._users_dao.insert_user(_id, _name, _position, _start_date, _quit_date))

    def update_user_quit_date(self, _user_id, _quit_date):
        return reactivex.from_callable(lambda: self._users_dao.update_quit_date(_user_id, _quit_date))


class UserAdminRepositoryImpl(UserAdminsRepository):

    def __init__(self, _user_admins_dao):
        self._user_admins_dao = _user_admins_dao

    def update_admin_password(self, _admin_id, _password):
        return reactivex.from_callable(lambda: self._user_admins_dao.update_admin_password(_admin_id, _password))

    def get_admins(self, admin_id):
        return reactivex.from_callable(lambda: self._user_admins_dao.select_all_user_admin(admin_id))

    def update_delvron_order_id(self, order_id):
        return self._user_admins_dao.update_delvron_order_id(order_id)

    def update_delvron_company_access(self, _company_access):
        return reactivex.from_callable(lambda: self._user_admins_dao.update_delvron_company_access(_company_access))


class ItemsRepositoryImpl(ItemsRepository):

    def __init__(self, _items_dao):
        self._items_dao = _items_dao
        # self._api_service = ApiService()

    def get_items(self):
        # return self._api_service.get_items_response()
        return reactivex.from_callable(lambda: self._items_dao.select_items())

    def get_only_items_wrt_products(self):
        return reactivex.from_callable(lambda: self._items_dao.select_items_wrt_products())

    def get_available_items(self):
        return reactivex.from_callable(lambda: self._items_dao.select_available_items())

    def create_item(self, _item_code, _name, _measure):
        return reactivex.from_callable(lambda: self._items_dao.insert_item(_item_code, _name, _measure))


class CustomersRepositoryImpl(CustomersRepository):

    def __init__(self, _customers_dao):
        self._customers_dao = _customers_dao

    def create_customer(self, _customer_id, _name, _address, _phno, _serial_no, _installed_date, _customer_type, _deactivated):
        return reactivex.from_callable(lambda: self._customers_dao.insert_one_customer(_customer_id, _name, _address, _phno, _serial_no,
                                                       _installed_date, _customer_type, _deactivated))

    def update_customer(self, _customer_id, _name, _address, _phno, _serial_no, _installed_date, _customer_type, _deactivated, _index_id):
        return reactivex.from_callable(lambda: self._customers_dao.update_one_customer(_customer_id, _name, _address, _phno, _serial_no, _installed_date, _customer_type, _deactivated, _index_id))

    def get_customers(self, _customer_id, _customer_name):
        return reactivex.from_callable(
            lambda: self._customers_dao.select_all_relevant_customers(_customer_id, _customer_name))


class ProductsRepositoryImpl(ProductsRepository):

    def __init__(self, _products_dao):
        self._products_dao = _products_dao
        # self._api_service = ApiService()

    def create_product(self, _id, _item_id, _local_price, _distributor_price, _defined_qty):
        return reactivex.from_callable(
            lambda: self._products_dao.update_product(_id, _item_id, _local_price, _distributor_price, _defined_qty))

    def get_products(self):
        # return reactivex.from_callable(lambda: self._api_service.get_products_response())
        return reactivex.from_callable(lambda: self._products_dao.select_products())

    def get_product(self, _item_id):
        return reactivex.from_callable(lambda: self._products_dao.select_specific_product(_item_id))

    def delete_product(self, _product_id):
        return self._products_dao.delete_one_product(_product_id)


class SalesOrdersRepositoryImpl(SalesOrderRepository):

    def __init__(self, _sales_orders_dao):
        self._sales_orders_dao = _sales_orders_dao

    def update_sales_order(self, _sales_order_id, _customer_id, _order_date, _status, _order_products,
                           _deleted_order_products):
        return reactivex.from_callable(lambda: self._sales_orders_dao.update_sales_order(_sales_order_id, _customer_id,
                                                                                      _order_date, _status,
                                                                                      _order_products,
                                                                                      _deleted_order_products))

    def get_sales_orders(self):
        return reactivex.from_callable(lambda: self._sales_orders_dao.select_all_sales_orders())

    def get_order(self, order_id):
        return reactivex.from_callable(lambda: self._sales_orders_dao.select_one_sales_order(order_id))

    def update_order_status(self, _status, _order_id):
        return self._sales_orders_dao.update_sale_status(_status, _order_id)


class SalesRepositoryImpl(SalesRepository):

    def __init__(self, _sales_dao):
        self._sales_dao = _sales_dao

    def get_last_sale_id(self):
        return self._sales_dao.select_last_sale_id()

    def create_sale(self, _sale_id, _created_at, _order_id, _sell_by, _approved_by):
        return reactivex.from_callable(
            lambda: self._sales_dao.insert_one_sale(_sale_id, _created_at, _order_id, _sell_by, _approved_by))

    def get_sales(self, _start_date, _end_date, _customer_id, _item_id, _salesman_id):
        return reactivex.from_callable(
            lambda: self._sales_dao.select_all_sales(_start_date, _end_date, _customer_id, _item_id, _salesman_id))


class ReceiptsRepositoryImpl(ReceiptsRepository):

    def __init__(self, _receipts_dao):
        self._receipts_dao = _receipts_dao

    def insert_one_receipt(self, _sale_id, _customer_id, _sale_amount, _received_amount, _balance, _received_date, _remark):
        return reactivex.from_callable(lambda: self._receipts_dao.insert_one_receipt(_sale_id, _customer_id, _sale_amount, _received_amount, _balance, _received_date, _remark))

    def get_one_sale_and_receipts(self, _sale_id):
        return reactivex.from_callable(lambda: self._receipts_dao.select_one_sale_and_receipts(_sale_id))

    def get_all_sales_id_by_customer(self, _customer_id, _sale_id):
        return reactivex.from_callable(
            lambda: self._receipts_dao.select_all_unpaid_off_sale_id_on_customers(_customer_id, _sale_id))

    def get_all_receipts_by_customer(self, _customer_id, _date):
        return reactivex.from_callable(
            lambda: self._receipts_dao.select_all_receipts_on_customers_and_date(_customer_id, _date))

    def update_balance_on_sale_id(self, _balance, _sale_id):
        return reactivex.from_callable(
            lambda: self._receipts_dao.update_balance_on_sale_id(_balance, _sale_id))