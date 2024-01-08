from business.models import Role
import reactivex

from constants import NO_DATA_INPUT_ERROR, PHONE_NUMBER_ERROR, PASSWORD_INVALID_ERROR, REPEATED_ERROR, RESTRICTION_CHAR_ERROR, NUMBER_ERROR, EXCEEDED_ERROR


class UpdateOrderUsecase:

    def __init__(self, _sales_orders_repo):
        self._sales_orders_repo = _sales_orders_repo

    def __call__(self, _sales_order_id, customer, _order_date, _status, _order_products, _deleted_order_products):
        if customer and len(_order_products) >= 1:
            return self._sales_orders_repo.update_sales_order(_sales_order_id, customer.id, _order_date, _status, _order_products, _deleted_order_products)
        return reactivex.throw(Exception(NO_DATA_INPUT_ERROR))


class DisplayOrdersUsecase:

    def __init__(self, _sales_orders_repo):
        self.sales_orders_repo = _sales_orders_repo

    def __call__(self):
        return self.sales_orders_repo.get_sales_orders()


class ReviewOrderUsecase:

    def __init__(self, _sales_orders_repo):
        self._sales_orders_repo = _sales_orders_repo

    def __call__(self, order_id):
        return self._sales_orders_repo.get_order(order_id)


class UpdateOrderStatusUsecase:

    def __init__(self, _sales_orders_repo):
        self._sales_orders_repo = _sales_orders_repo

    def __call__(self, _status, _order_id):
        return self._sales_orders_repo.update_order_status(_status, _order_id)


class RetrieveLastSaleId:

    def __call__(self, _sale_repo):
        return _sale_repo.get_last_sale_id()


class MakeSaleUsecase:

    def __init__(self, _sale_repo):
        self._sale_repo = _sale_repo

    def __call__(self, _sale_id, _created_at, _order_id, _sell_by, _approved_by):
        return self._sale_repo.create_sale(_sale_id, _created_at, _order_id, _sell_by, _approved_by)


class DisplaySalesUsecase:

    def __init__(self, _sale_repo):
        self._sale_repo = _sale_repo

    def __call__(self, _start_date, _end_date, _customer, _item, _salesman):
        _customer_id = '%%' if _customer.id == 0 else _customer.id
        _item_id = '%%' if _item is None else _item.item_code
        _salesman_id = '%%' if _salesman is None else _salesman.id
        return self._sale_repo.get_sales(_start_date, _end_date, _customer_id, _item_id, _salesman_id)


class DisplayCustomersUsecase:

    def __init__(self, _customer_repo):
        self._customer_repo = _customer_repo

    def __call__(self, _customer_id, _customer_name):
        _customer_id, _customer_name = '%' if _customer_id is None or _customer_id == '' else _customer_id, '%' if _customer_id is None or _customer_id == '' else _customer_name
        return self._customer_repo.get_customers(_customer_id, _customer_name)


class CreateCustomerUsecase:

    def __init__(self, _customer_repo):
        self._customer_repo = _customer_repo

    def __call__(self, _customer_id, _name, _address, _phno, _serial_no, _installed_date, _deactivated,
                            _customer_type):
        _error = validate_customer_entry_form(_customer_id, _name, _address, _phno, _serial_no, _installed_date,
                                              _deactivated, _customer_type)
        return _error if _error else self._customer_repo.create_customer(_customer_id, _name, _address, _phno, _serial_no,
                                                                    _installed_date, _customer_type, _deactivated)


class UpdateCustomerUsecase:

    def __init__(self, _customer_repo):
        self._customer_repo = _customer_repo

    def __call__(self, _customer_id, _name, _address, _phno, _serial_no, _installed_date, _deactivated,
                            _customer_type, _index_id):
        _error = validate_customer_entry_form(_customer_id, _name, _address, _phno, _serial_no, _installed_date,
                                              _deactivated, _customer_type)
        return _error if _error else self._customer_repo.update_customer(_customer_id, _name, _address, _phno, _serial_no,
                                                                    _installed_date, _customer_type, _deactivated,
                                                                    _index_id)


def validate_customer_entry_form(_customer_id, _name, _address, _phno, _serial_no, _installed_date, _deactivated,
                            _customer_type):

    if _customer_id is None or _customer_id == '' or _customer_id == '' or _name == '' or _phno == '':
        return reactivex.throw(Exception(NO_DATA_INPUT_ERROR))
    elif not _phno.isnumeric() or not ((len(_phno) <= 11) and (len(_phno) >= 9)):
        return reactivex.throw(Exception(PHONE_NUMBER_ERROR))
    elif _name.find('\\') != -1:
        return reactivex.throw(Exception(RESTRICTION_CHAR_ERROR))
    else:
        return None


#todo need to reconsider whether it should be deleted
def remove_customer_usecase(_customers_repo, company_id):
    return _customers_repo.delete_customer(company_id)


class DisplayItemsUsecase:

    def __init__(self, _items_repo):
        self._items_repo = _items_repo

    def __call__(self):
        return self._items_repo.get_items()


class DisplayItemsWrtProductsUsecase:

    def __init__(self, _items_repo):
        self._items_repo = _items_repo

    def __call__(self):
        return self._items_repo.get_only_items_wrt_products()


class RetrieveAllAvailableItemsUsecase:

    def __init__(self, _items_repo):
        self._items_repo = _items_repo

    def __call__(self):
        return self._items_repo.get_available_items()


class SaveItemUsecase:

    def __init__(self, _items_repo):
        self._items_repo = _items_repo

    def __call__(self, _item, _name, _measure):
        if _name != '' and _measure != '':
            return self._items_repo.create_item(_item.item_code if _item else _item, _name, _measure)
        return reactivex.throw(Exception(NO_DATA_INPUT_ERROR))


# Products - Accountant's

class DisplayProductsUsecase:

    def __init__(self, _products_repo):
        self._products_repo = _products_repo

    def __call__(self):
        return self._products_repo.get_products()


class GetProductUsecase:

    def __init__(self, _products_repo):
        self._products_repo = _products_repo

    def __call__(self, _item_id):
        return self._products_repo.get_product(_item_id)


class SaveProductUsecase:

    def __init__(self, _products_repo):
        self._products_repo = _products_repo

    def __call__(self, _existed_products,  _item, _local_price, _distributor_price, _defined_qty=None, _id=None):
        if _local_price.isnumeric() and _item:
            if _id is None:
                if _item.item_code in _existed_products:
                    return reactivex.throw(Exception(REPEATED_ERROR))
            if _distributor_price.isnumeric() and _defined_qty:
                return self._products_repo.create_product(_id, _item.item_code, _local_price, _distributor_price, _defined_qty)
            return self._products_repo.create_product(_id, _item.item_code, _local_price, _distributor_price, _defined_qty)
        return reactivex.throw(Exception(NO_DATA_INPUT_ERROR))


class RemoveProductUsecase:

    def __init__(self, _products_repo):
        self._products_repo = _products_repo

    def __call__(self, _product_id):
        return self._products_repo.delete_product(_product_id)


class GetAllReceiptsByDateAndCustomerUsecase:

    def __init__(self, _receipts_repo):
        self._receipts_repo = _receipts_repo

    def __call__(self, _customer_id, _date):
        return self._receipts_repo.get_all_receipts_by_customer(_customer_id, _date)


class DisplayAllUnpaidOffSaleIdUsecase:

    def __init__(self, _receipt_repo):
        self._receipt_repo = _receipt_repo

    def __call__(self, _customer_id, _sale_id):
        return self._receipt_repo.get_all_sales_id_by_customer(_customer_id, _sale_id)


class DisplayOneSaleAndReceiptsUsecase:

    def __init__(self, _receipt_repo):
        self._receipt_repo = _receipt_repo

    def __call__(self, _sale_id):
        return self._receipt_repo.get_one_sale_and_receipts(_sale_id)


class InsertOneReceiptUsecase:

    def __init__(self, _receipt_repo):
        self._receipt_repo = _receipt_repo

    def __call__(self, _sale_id, _customer_id, _sale_amount, _received_amount, _balance, _received_date, _remark):
        if not _received_amount.isnumeric():
            return reactivex.throw(Exception(NUMBER_ERROR))
        elif int(_received_amount) > _balance:
            return reactivex.throw(Exception(EXCEEDED_ERROR))
        elif int(_received_amount) == 0:
            return reactivex.throw(Exception(NO_DATA_INPUT_ERROR))
        else:
            return self._receipt_repo.insert_one_receipt(_sale_id, _customer_id, _sale_amount, _received_amount,
                                                _balance - int(_received_amount), _received_date, _remark)


class UpdateBalanceOnSaleIdUsecase:

    def __init__(self, _receipt_repo):
        self._receipt_repo = _receipt_repo

    def __call__(self, _balance, _sale_id):
        return self._receipt_repo.update_balance_on_sale_id(_balance, _sale_id)


class RetrieveAllAdminsUsecase:

    def __call__(self, _user_admin_repo):
        return _user_admin_repo.get_admins('%')


class GetDelvronAdminUsecase:

    def __init__(self, _user_admins_repo):
        self._user_admins_repo = _user_admins_repo

    def __call__(self, _admin_id):
        return self._user_admins_repo.get_admins(_admin_id)


class UpdateDelvronSaleIdUsecase:

    def __init__(self, _user_admins_repo):
        self._user_admins_repo = _user_admins_repo

    def __call__(self, _order_id):
        return self._user_admins_repo.update_delvron_order_id(_order_id)


class UpdateDelvronAdminPasswordUsecase:

    def __init__(self, _user_admins_repo):
        self._user_admins_repo = _user_admins_repo

    def __call__(self, _admin_id, _password):
        if _password != "" and _password:
            return self._user_admins_repo.update_admin_password(_admin_id, _password)
        return reactivex.throw(Exception(PASSWORD_INVALID_ERROR))


class UpdateDelvronCompanyAccessUsecase:

    def __init__(self, _user_admins_repo):
        self._user_admins_repo = _user_admins_repo

    def __call__(self, _company_access):
        return self._user_admins_repo.update_delvron_company_access(_company_access)


class RetrieveAllUsersUsecase:

    def __init__(self, _users_repo):
        self._users_repo = _users_repo

    def __call__(self):
        return self._users_repo.get_all_users()


class RetrieveAllActiveUsersUsecase:

    def __init__(self, _users_repo):
        self._users_repo = _users_repo

    def __call__(self):
        return self._users_repo.get_all_active_users()


class RetrieveAllActiveSalesmenUsecase:

    def __init__(self, _users_repo):
        self._users_repo = _users_repo

    def __call__(self):
        return self._users_repo.get_all_active_specific_users_by_position(Role.SALES.value)


class SaveNewUserUsecase:

    def __init__(self, _users_repo):
        self._users_repo = _users_repo

    def __call__(self, _id, _name, _position, _start_date, _quit_date):
        if _name != "" and _position != "":
            return self._users_repo.update_user(_id, _name, _position, _start_date, _quit_date)
        return reactivex.throw(Exception(NO_DATA_INPUT_ERROR))


class QuitUserUsecase:

    def __init__(self, _users_repo):
        self._users_repo = _users_repo

    def __call__(self, _user_id, _quit_date):
        return self._users_repo.update_user_quit_date(_user_id, _quit_date)
