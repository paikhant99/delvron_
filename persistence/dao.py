from abc import ABC, abstractmethod
import dataclasses

from persistence.database import (GET_ALL_USERS, GET_ALL_ACTIVE_USERS, GET_ALL_ACTIVE_SPECIFIC_USERS_BY_POSITION,
                                  POST_ONE_USER, PUT_USER_QUIT_DATE, PUT_ADMIN_PASSWORD, GET_ALL_ADMINS,
                                  PUT_ADMIN_COMPANY_ACCESS, PUT_ADMIN_ORDER_ID, GET_ALL_ITEMS,
                                  GET_SPECIFIC_ITEMS_WRT_PRODUCTS, GET_ALL_AVAILABLE_ITEMS, POST_ONE_ITEM,
                                  POST_ONE_CUSTOMER, PUT_ONE_CUSTOMER, GET_ALL_SPECIFIC_CUSTOMERS, POST_ONE_PRODUCT,
                                  GET_ALL_PRODUCTS, GET_SPECIFIC_PRODUCT_WRT_ITEM, DELETE_ONE_PRODUCT,
                                  POST_ONE_SALES_ORDER, POST_ORDER_PRODUCTS, DELETE_ORDER_PRODUCTS,
                                  GET_SPECIFIC_SALES_ORDERS, PUT_SALES_ORDER_STATUS, POST_ONE_SALE, GET_LAST_SALE_ID,
                                  GET_ALL_SALES, GET_ALL_RECEIPTS_BY_DATE, GET_ALL_UNPAID_OFF_SALE_ID_BY_CUSTOMER,
                                  GET_ONE_SALE, GET_ALL_RECEIPTS_BY_SALE_ID, POST_ONE_RECEIPT, PUT_RECEIPTS_BALANCE)

from business.models import User, UserAdmin, Item, Customer, Product, SalesOrder, OrderProduct, Sale, Receipt


class UsersDao(ABC):

    @abstractmethod
    def select_all_users(self): pass

    @abstractmethod
    def select_all_active_users(self, _quit_date): pass

    @abstractmethod
    def select_all_active_specific_users_by_position(self, _quit_date, _position): pass

    @abstractmethod
    def insert_user(self, _id, _name, _position, _start_date, _quit_date): pass

    @abstractmethod
    def update_quit_date(self, _user_id, _quit_date): pass


class UserAdminDao(ABC):

    @abstractmethod
    def update_admin_password(self, _admin_id, _password): pass

    @abstractmethod
    def select_all_user_admin(self, _admin_id): pass

    @abstractmethod
    def update_delvron_order_id(self, _order_id): pass

    @abstractmethod
    def update_delvron_company_access(self, _company_access): pass


class ItemsDao(ABC):

    @abstractmethod
    def select_items(self): pass

    @abstractmethod
    def select_items_wrt_products(self): pass

    @abstractmethod
    def select_available_items(self): pass

    @abstractmethod
    def insert_item(self, _item_code, _name, _measure): pass


class CustomersDao(ABC):

    @abstractmethod
    def insert_one_customer(self, _customer_id, _name, _address, _phno, _serial_no, _installed_date, _customer_type, _deactivated): pass

    @abstractmethod
    def update_one_customer(self, _customer_id, _name, _address, _phno, _serial_no, _installed_date, _customer_type, _deactivated, _index_id): pass

    @abstractmethod
    def select_all_relevant_customers(self, _customer_id, _customer_name): pass


class ProductsDao(ABC):

    @abstractmethod
    def update_product(self, _id, _item_id, _local_price, _distributor_price, _defined_qty): pass

    @abstractmethod
    def select_products(self): pass

    @abstractmethod
    def select_specific_product(self, _item_id): pass

    @abstractmethod
    def delete_one_product(self, _product_id): pass


class SalesOrdersDao(ABC):

    @abstractmethod
    def update_sales_order(self, _sales_order_id, _customer_id, _order_date, _status, _order_products, _deleted_order_products): pass

    @abstractmethod
    def select_all_sales_orders(self): pass

    @abstractmethod
    def select_one_sales_order(self, _order_id): pass

    @abstractmethod
    def update_sale_status(self, _status, _order_id): pass


class SalesDao(ABC):

    @abstractmethod
    def insert_one_sale(self, _sale_id, _created_at, _order_id, _sell_by, _approved_by): pass

    @abstractmethod
    def select_last_sale_id(self): pass

    @abstractmethod
    def select_all_sales(self, _start_date, _end_date, _customer_id, _item_id, _salesman_id): pass


class ReceiptsDao(ABC):

    @abstractmethod
    def insert_one_receipt(self, _sale_id, _customer_id, _sale_amount, _received_amount, _balance, received_date, _remark): pass

    @abstractmethod
    def update_balance_on_sale_id(self, _balance, _sale_id): pass

    @abstractmethod
    def select_all_unpaid_off_sale_id_on_customers(self, _customer_id, _sale_id): pass

    @abstractmethod
    def select_all_receipts_on_customers_and_date(self, _customer_id, _date): pass

    @abstractmethod
    def select_one_sale_and_receipts(self, _sale_id): pass


class UsersDaoImpl(UsersDao):

    def __init__(self, _db):
        self._db = _db

    def select_all_users(self):
        self._db.connect()
        users = [User(*user) for user in self._db.cursor.execute(GET_ALL_USERS).fetchall()]
        self._db.close()
        return users

    def select_all_active_users(self, _quit_date):
        self._db.connect()
        _users = [User(*user) for user in self._db.cursor.execute(GET_ALL_ACTIVE_USERS, [_quit_date]).fetchall()]
        self._db.close()
        return _users

    def select_all_active_specific_users_by_position(self, _quit_date, _position):
        self._db.connect()
        _users = [User(*user) for user in self._db.cursor.execute(GET_ALL_ACTIVE_SPECIFIC_USERS_BY_POSITION, [_quit_date, _position]).fetchall()]
        self._db.close()
        return _users

    def insert_user(self, _id, _name, _position, _start_date, _quit_date):
        self._db.connect()
        user_id = self._db.cursor.execute(POST_ONE_USER, [_id, _name, _position, _start_date, _quit_date]).lastrowid
        self._db.conn.commit()
        self._db.close()
        return user_id

    def update_quit_date(self, _user_id, _quit_date):
        self._db.connect()
        _user_count = self._db.cursor.execute(PUT_USER_QUIT_DATE, [_quit_date, _user_id]).rowcount
        self._db.conn.commit()
        self._db.close()
        return _user_count


class UserAdminDaoImpl(UserAdminDao):

    def __init__(self, db):
        self._db = db

    def update_admin_password(self, _admin_id, _password):
        self._db.connect()
        _admin_id = self._db.cursor.execute(PUT_ADMIN_PASSWORD, [_password, _admin_id]).lastrowid
        self._db.conn.commit()
        self._db.close()
        return _admin_id

    def select_all_user_admin(self, _admin_id):
        self._db.connect()
        admins = [UserAdmin(*admin) for admin in self._db.cursor.execute(GET_ALL_ADMINS, [_admin_id])]
        self._db.close()
        return admins

    def update_delvron_order_id(self, _order_id):
        self._db.connect()
        row_count = self._db.cursor.execute(PUT_ADMIN_ORDER_ID, [_order_id]).rowcount
        self._db.conn.commit()
        self._db.close()
        return row_count

    def update_delvron_company_access(self, _company_access):
        self._db.connect()
        row_count = self._db.cursor.execute(PUT_ADMIN_COMPANY_ACCESS, [_company_access]).rowcount
        self._db.conn.commit()
        self._db.close()
        return row_count


class ItemsDaoImpl(ItemsDao):

    def __init__(self, _db):
        self._db = _db

    def select_items(self):
        self._db.connect()
        _items = [Item(*_item) for _item in self._db.cursor.execute(GET_ALL_ITEMS).fetchall()]
        self._db.close()
        return _items

    def select_items_wrt_products(self):
        self._db.connect()
        _items = [Item(*_item) for _item in self._db.cursor.execute(GET_SPECIFIC_ITEMS_WRT_PRODUCTS).fetchall()]
        self._db.close()
        return _items

    def select_available_items(self):
        self._db.connect()
        _items = [Item(*_item) for _item in self._db.cursor.execute(GET_ALL_AVAILABLE_ITEMS).fetchall()]
        self._db.close()
        return _items

    def insert_item(self, _item_code, _name, _measure):
        self._db.connect()
        item_id = self._db.cursor.execute(POST_ONE_ITEM, [_item_code, _name, _measure]).lastrowid
        self._db.conn.commit()
        self._db.close()
        return item_id


class CustomersDaoImpl(CustomersDao):

    def __init__(self, _db):
        self._db = _db

    def insert_one_customer(self, _customer_id, _name, _address, _phno, _serial_no, _installed_date, _customer_type, _deactivated):
        self._db.connect()
        _customer_id = self._db.cursor.execute(POST_ONE_CUSTOMER, [_customer_id, _name, _address, _phno, _serial_no, _installed_date, _customer_type, _deactivated]).lastrowid
        self._db.conn.commit()
        self._db.close()
        return _customer_id

    def update_one_customer(self, _customer_id, _name, _address, _phno, _serial_no, _installed_date, _customer_type, _deactivated, _index_id):
        self._db.connect()
        _customer_updated_count = self._db.cursor.execute(PUT_ONE_CUSTOMER, [_customer_id, _name, _address, _phno, _serial_no, _installed_date, _customer_type, _deactivated, _index_id]).rowcount
        self._db.conn.commit()
        self._db.close()
        print(_customer_updated_count)
        return _customer_updated_count

    def select_all_relevant_customers(self, _customer_id, _customer_name):
        self._db.connect()
        _customers = [Customer(*_customer) for _customer in
                      self._db.cursor.execute(GET_ALL_SPECIFIC_CUSTOMERS, [_customer_id+'%', _customer_name+'%']).fetchall()]
        self._db.close()
        return _customers


class ProductsDaoImpl(ProductsDao):

    def __init__(self, _db):
        self._db = _db

    def update_product(self, _id, _item_id, _local_price, _distributor_price, _defined_qty):
        self._db.connect()
        _product_id = self._db.cursor.execute(POST_ONE_PRODUCT,
                                              [_id, _item_id, _local_price, _distributor_price, _defined_qty]).lastrowid
        self._db.conn.commit()
        self._db.close()
        return _product_id

    def select_products(self):
        self._db.connect()
        products = [Product(*_raw_product[:4], item=Item(*_raw_product[4:])) for _raw_product in
                    self._db.cursor.execute(GET_ALL_PRODUCTS).fetchall()]
        self._db.close()
        return products

    def select_specific_product(self, _item_id):
        self._db.connect()
        _raw_product = self._db.cursor.execute(GET_SPECIFIC_PRODUCT_WRT_ITEM, [_item_id]).fetchone()
        self._db.close()
        return Product(*_raw_product[:4], item=Item(*_raw_product[4:]))

    def delete_one_product(self, _product_id):
        self._db.connect()
        _product_id = self._db.cursor.execute(DELETE_ONE_PRODUCT, [_product_id]).lastrowid
        self._db.conn.commit()
        self._db.close()
        return _product_id


class SalesOrdersDaoImpl(SalesOrdersDao):

    def __init__(self, db):
        self.db = db

    def update_sales_order(self, _sales_order_id, _customer_id, _order_date, _status, _order_products, _deleted_order_products):
        self.db.connect()
        _salesorder_id = self.db.cursor.execute(POST_ONE_SALES_ORDER, [_sales_order_id, _customer_id, _order_date, _status]).lastrowid
        self.db.conn.commit()
        _orderproducts = [(_orderproduct.id, _salesorder_id, _orderproduct.item.item_code, _orderproduct.unit_price,
                           _orderproduct.qty, _orderproduct.defined_distributor_qty, _orderproduct.remark)
                          for _orderproduct in _order_products]
        self.db.cursor.executemany(POST_ORDER_PRODUCTS, _orderproducts)
        self.db.conn.commit()
        for product_id in _deleted_order_products:
            self.db.cursor.execute(DELETE_ORDER_PRODUCTS, [product_id])
        self.db.conn.commit()

        self.db.close()
        return _salesorder_id

    def select_all_sales_orders(self):
        self.db.connect()
        # _sales_orders = [SalesOrder(*sales_order[:4], company=Customer(*sales_order[4:])) for sales_order in
        #                  self.persistence.cursor.execute(GET_SPECIFIC_SALES_ORDERS, ['%%']).fetchall()]
        sales_orders_dict = {}
        for sales_order in self.db.cursor.execute(GET_SPECIFIC_SALES_ORDERS, ['%%']).fetchall():

            if sales_order[0] not in sales_orders_dict:
                sales_orders_dict[sales_order[0]] = SalesOrder(*sales_order[:3], company=Customer(*sales_order[3:11]))

            order_product = OrderProduct(*sales_order[11:16], item=Item(*sales_order[16:]))
            sales_orders_dict[sales_order[0]].order_products.append(order_product)
        print(list(sorted(sales_orders_dict.items())))
        self.db.close()
        return list(dict(sorted(sales_orders_dict.items())).values())

    def select_one_sales_order(self, _order_id):
        self.db.connect()
        _order = None
        # _order_products = []
        for order_product in self.db.cursor.execute(GET_SPECIFIC_SALES_ORDERS, [_order_id]).fetchall():
            if _order is None:
                _order = SalesOrder(*order_product[:3], company=Customer(*order_product[3:11]))
            _order.order_products.append(OrderProduct(*order_product[11:16], item=Item(*order_product[16:])))
        # if raw_order:
        #     _order = SalesOrder(*raw_order[:4], company=Customer(*raw_order[4:]))
        #     _order_products = [OrderProduct(*order_product[:5], item=Item(*order_product[5:])) for order_product in self.persistence.cursor.execute(GET_SPECIFIC_ORDER_PRODUCTS, [_order_id]).fetchall()]
        # self.persistence.close()
        return _order

    def update_sale_status(self, _status, _order_id):
        self.db.connect()
        _order_id = self.db.cursor.execute(PUT_SALES_ORDER_STATUS, [_status, _order_id]).lastrowid
        self.db.conn.commit()
        self.db.close()
        return _order_id


class SalesDaoImpl(SalesDao):

    def __init__(self, _db):
        self._db = _db

    def insert_one_sale(self, _sale_id, _created_at, _order_id, _sell_by, _approved_by):
        self._db.connect()
        _sale_id = self._db.cursor.execute(POST_ONE_SALE,
                                           [_sale_id, _created_at, _order_id, _sell_by, _approved_by]).lastrowid
        self._db.conn.commit()
        self._db.close()
        return _sale_id

    def select_last_sale_id(self):
        self._db.connect()
        _last_sale_id = self._db.cursor.execute(GET_LAST_SALE_ID).fetchone()
        self._db.close()
        return list(_last_sale_id)[0] if _last_sale_id else '-1'

    def select_all_sales(self, _start_date, _end_date, _customer_id, _item_id, _salesman_id):
        print(f'Start Date {_start_date}, End Date {_end_date}')
        self._db.connect()
        # _sales = self._db.cursor.execute(GET_ALL_SALES).fetchall()
        sales_dict = {}
        for sale in self._db.cursor.execute(GET_ALL_SALES, [_start_date, _end_date, _customer_id, _item_id, _salesman_id]).fetchall():

            if sale[0] not in sales_dict:
                sales_dict[sale[0]] = Sale(*sale[:2], sales_order=SalesOrder(*sale[2:5], company=Customer(*sale[5:13])), sell_by=User(*sale[21:26]), approve_by=User(*sale[26:]))

            order_product = OrderProduct(*sale[13:18], item=Item(*sale[18:21]))
            sales_dict[sale[0]].sales_order.order_products.append(order_product)
        print(sales_dict)
        # _sales = [Sale(*sale[:3], sales_order=SalesOrder(*sale[3:7], company=Customer(*sale[7:15])), sell_by=User(*sale[15:20]), approve_by=User(*sale[20:]), order_product=None) for sale in self._db.cursor.execute(GET_ALL_SALES).fetchall()]
        self._db.close()
        return list(dict(sorted(sales_dict.items(), reverse=True)).values())


class ReceiptsDaoImpl(ReceiptsDao):

    def __init__(self, _db):
        self._db = _db

    def insert_one_receipt(self, _sale_id, _customer_id, _sale_amount, _received_amount, _balance, received_date, _remark):
        self._db.connect()
        _receipt_id = self._db.cursor.execute(POST_ONE_RECEIPT, [_sale_id, _customer_id, _sale_amount, _received_amount, _balance, received_date, _remark]).lastrowid
        self._db.conn.commit()
        self._db.close()
        return _sale_id, _balance

    def update_balance_on_sale_id(self, _balance, _sale_id):
        print(_balance)
        print(_sale_id)
        self._db.connect()
        _receipt_id = self._db.cursor.execute(PUT_RECEIPTS_BALANCE, [_balance, _sale_id]).rowcount
        self._db.conn.commit()
        self._db.close()
        return _receipt_id

    def select_all_unpaid_off_sale_id_on_customers(self, _customer_id, _sale_id):
        self._db.connect()
        _all_sale_id = self._db.cursor.execute(GET_ALL_UNPAID_OFF_SALE_ID_BY_CUSTOMER, [_customer_id, _customer_id, _sale_id]).fetchall()
        self._db.close()
        return _all_sale_id

    def select_all_receipts_on_customers_and_date(self, _customer_id, _date):
        self._db.connect()
        _receipts = [Receipt(*receipt[:7], customer=Customer(*receipt[7:])) for receipt in self._db.cursor.execute(GET_ALL_RECEIPTS_BY_DATE, [_date, _customer_id]).fetchall()]
        self._db.close()
        return _receipts

    def select_one_sale_and_receipts(self, _sale_id):
        self._db.connect()
        sales_dict = {}
        print(list(_sale_id))
        for sale in self._db.cursor.execute(GET_ONE_SALE,
                                            [list(_sale_id)[0]]).fetchall():

            if sale[0] not in sales_dict:
                sales_dict[sale[0]] = Sale(*sale[:2], sales_order=SalesOrder(*sale[2:5], company=Customer(*sale[5:13])),
                                           sell_by=User(*sale[21:26]), approve_by=User(*sale[26:]))

            order_product = OrderProduct(*sale[13:18], item=Item(*sale[18:21]))
            sales_dict[sale[0]].sales_order.order_products.append(order_product)

        for receipt in self._db.cursor.execute(GET_ALL_RECEIPTS_BY_SALE_ID, [list(_sale_id)[0]]).fetchall():
            sales_dict[list(_sale_id)[0]].receipts.append(Receipt(*receipt[:7], customer=Customer(*receipt[7:])))
        self._db.close()
        return sales_dict.get(list(_sale_id)[0])
