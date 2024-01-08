from abc import ABC, abstractmethod
import sqlite3
import os
import ctypes

from business.models import Access

DBPATH = os.getcwd() + '/Documents/work/delvron/persistence/main'
DEBUG_DBPATH = os.getcwd() + '/delvron_debug'
MAIN_DBPATH = os.getcwd() + '/delvron_main'

# Customer - HR's
INIT_CUSTOMERS = ("create table if not exists customers (id TEXT, name TEXT, address TEXT, phno TEXT, serial_no TEXT, "
                  "installed_date TEXT, customer_type TEXT, deactivated BOOLEAN,  PRIMARY KEY(id))")
GET_ALL_SPECIFIC_CUSTOMERS = "select * from customers where id like ? or name like ?"
POST_ONE_CUSTOMER = (
    "insert or replace into customers (id, name, address, phno, serial_no, installed_date, customer_type,"
    "deactivated) values (?, ?, ?, ?, ?, ?, ?, ?)")
PUT_ONE_CUSTOMER = (
    "update customers set id=?, name=?, address=?, phno=?, serial_no=?, installed_date=?, "
    "customer_type=?, deactivated=? where id=?")

# Item - INVENTORY's
INIT_ITEMS = "create table if not exists items (id INTEGER, name TEXT, measurement TEXT, PRIMARY KEY(id))"

GET_ALL_ITEMS = "select * from items"

GET_SPECIFIC_ITEMS_WRT_PRODUCTS = "select * from items where id in (select item_id from 'products')"

GET_ALL_AVAILABLE_ITEMS = "select * from items where id in (select distinct item_id from order_products union select item_id from products)"

POST_ONE_ITEM = "insert or replace into items (id, name, measurement) values (?, ?, ?)"

# Product - Accountant's

INIT_PRODUCTS = ("create table if not exists 'products' (id INTEGER, item_id TEXT, local_price INTEGER, "
                 "distributor_price INTEGER, defined_qty INTEGER, PRIMARY KEY(id), FOREIGN KEY(item_id) REFERENCES "
                 "items(id))")
POST_ONE_PRODUCT = ("insert or replace into 'products' (id, item_id, local_price, distributor_price, defined_qty) "
                    "values(?, ?, ?, ?, ?)")
GET_ALL_PRODUCTS = ("select 'products'.id, 'products'.local_price, 'products'.distributor_price, "
                    "'products'.defined_qty, items.id, items.name, items.measurement from 'products' inner join items "
                    "where 'products'.item_id == items.id")
GET_SPECIFIC_PRODUCT_WRT_ITEM = ("select 'products'.id, 'products'.local_price, 'products'.distributor_price, "
                                 "'products'.defined_qty, items.id, items.name, items.measurement from 'products' "
                                 "inner join items where 'products'.item_id == items.id and items.id LIKE ?")
DELETE_ONE_PRODUCT = "delete from 'products' where id = ?"

# Receipt - ACCOUNTANT's

INIT_RECEIPTS = ("create table if not exists receipts (id INTEGER, sale_id INTEGER, customer_id INTEGER, sale_amount "
                 "INTEGER, received_amount INTEGER, balance INTEGER, received_date date(6), remark TEXT, PRIMARY KEY("
                 "id), FOREIGN KEY(sale_id) REFERENCES sales(id), FOREIGN KEY(customer_id) REFERENCES customers(id))")

POST_ONE_RECEIPT = ("insert into receipts (sale_id, customer_id, sale_amount, received_amount, balance, "
                    "received_date, remark) VALUES(?, ?, ?, ?, ?, ?, ?)")

PUT_RECEIPTS_BALANCE = "update receipts set balance=? where sale_id like ?"

GET_ALL_UNPAID_OFF_SALE_ID_BY_CUSTOMER = ("select * from (select sales.id from sales join sales_orders on "
                                          "sales.order_id == sales_orders.id where customer_id like ? except select "
                                          "distinct sale_id from receipts where customer_id like ? and balance == 0) "
                                          "where id like ?")

GET_ALL_RECEIPTS_BY_DATE = ("select receipts.id, receipts.sale_id, receipts.sale_amount, receipts.received_amount, "
                            "receipts.balance, receipts.received_date, receipts.remark, customers.* from receipts "
                            "join customers on customers.id=receipts.customer_id where receipts.received_date=? and "
                            "receipts.customer_id like ?")

GET_ALL_RECEIPTS_BY_SALE_ID = ("select receipts.id, receipts.sale_id, receipts.sale_amount, receipts.received_amount, "
                               "receipts.balance, receipts.received_date, receipts.remark, customers.* from receipts "
                               "join customers on receipts.customer_id==customers.id where sale_id=?")

# Sales Order - SALESMEN's
INIT_SALES_ORDERS = ("create table if not exists sales_orders (id INTEGER, customer_id INTEGER, order_date date(6), "
                     "status TEXT, PRIMARY KEY(id), FOREIGN KEY(customer_id) REFERENCES customers(id))")

# GET_ALL_SALES_ORDERS = "select sales_orders.id, customers.id, customers.code, "
POST_ONE_SALES_ORDER = "insert or replace into sales_orders (id, customer_id, order_date, status) values (?, ?, ?, ?)"

PUT_SALES_ORDER_STATUS = "update sales_orders set status = ? where id=?"

# GET_SPECIFIC_SALES_ORDERS = ("select sales_orders.id, count(order_products.id) as order_qty, "
#                              "sales_orders.status, sales_orders.order_date, customers.* from sales_orders"
#                              " join customers on sales_orders.customer_id==customers.id join order_products "
#                              "on order_products.salesorder_id == sales_orders.id where sales_orders.id like ? group by order_products.salesorder_id")

GET_SPECIFIC_SALES_ORDERS = ("select sales_orders.id, sales_orders.status, sales_orders.order_date, customers.*, "
                             "order_products.id, order_products.unit_price, order_products.quantity, "
                             "order_products.defined_distributor_qty, order_products.remark, items.* from sales_orders join "
                             "customers on sales_orders.customer_id == customers.id join order_products on sales_orders.id == "
                             "order_products.salesorder_id join items on order_products.item_id == items.id where "
                             "sales_orders.id like ?")

order_wrt_customer_query = ("select 'order'.id, 'order'.delivered_date, 'order'.printed_time, 'order'.approved_by, "
                            "'order'.sell_by, customer.id, customer.name, customer.address, customer.serial_no, "
                            "customer.phno, customer.deactivated, customer.installed_date, customer.market_type "
                            "from customer join 'order' on customer.id = 'order'.company_id where 'order'.id = ?")

# Order Products - SALESMEN's
INIT_ORDER_PRODUCTS = ("create table if not exists order_products (id INTEGER, salesorder_id INTEGER, item_id INTEGER, "
                       "unit_price INTEGER, quantity INTEGER, defined_distributor_qty INTEGER, remark TEXT, "
                       "PRIMARY KEY(id), FOREIGN KEY(salesorder_id) REFERENCES sales_orders(id), "
                       "FOREIGN KEY(item_id) REFERENCES items(id))")

POST_ORDER_PRODUCTS = ("insert or replace into order_products (id, salesorder_id, item_id, unit_price, quantity, "
                       "defined_distributor_qty, remark) values (?, ?, ?, ?, ?, ?, ?)")

GET_SPECIFIC_ORDER_PRODUCTS = ("select order_products.id, order_products.unit_price, order_products.quantity, "
                               "order_products.defined_distributor_qty, order_products.remark, items.id, items.name, "
                               "items.measurement from order_products join items on order_products.item_id == "
                               "items.id where salesorder_id==?")

DELETE_ORDER_PRODUCTS = "delete from order_products where id = ?"

# Sales - SALESMEN's

INIT_SALES = ("create table if not exists sales (id INTEGER, created_at date(6), order_id INTEGER, sell_by INTEGER, "
              "approve_by INTEGER, PRIMARY KEY(id), FOREIGN KEY(order_id) REFERENCES sales_orders(id), FOREIGN KEY("
              "sell_by) REFERENCES 'users'(id), FOREIGN KEY(approve_by) REFERENCES 'users'(id))")

POST_ONE_SALE = "insert into sales (id, created_at, order_id, sell_by, approve_by) values (?, ?, ?, ?, ?)"

GET_LAST_SALE_ID = "select id from sales order by id desc limit 1;"

GET_ALL_SALES = ("select sales.id, sales.created_at, sales_orders.id, sales_orders.status, sales_orders.order_date, "
                 "customers.*, order_products.id, order_products.unit_price, order_products.quantity, "
                 "order_products.defined_distributor_qty, order_products.remark, items.*, u1.*, u2.*  from (select * "
                 "from sales where sales.created_at between ? and ? order by sales.id desc) as sales join "
                 "sales_orders on sales.order_id == sales_orders.id join customers on sales_orders.customer_id == "
                 "customers.id join order_products on sales_orders.id == order_products.salesorder_id join items on "
                 "order_products.item_id == items.id join users u1 on sales.sell_by == u1.id join users u2 on "
                 "sales.approve_by == u2.id where customers.id like ? and items.id like ? and u1.id like ?")

GET_ONE_SALE = ("select sales.id, sales.created_at, sales_orders.id, sales_orders.status, sales_orders.order_date, "
                "customers.*, order_products.id, order_products.unit_price, order_products.quantity, "
                "order_products.defined_distributor_qty, order_products.remark, items.*, u1.*, u2.*  from (select * "
                "from sales where sales.id= ?) as sales join "
                "sales_orders on sales.order_id == sales_orders.id join customers on sales_orders.customer_id == "
                "customers.id join order_products on sales_orders.id == order_products.salesorder_id join items on "
                "order_products.item_id == items.id join users u1 on sales.sell_by == u1.id join users u2 on "
                "sales.approve_by == u2.id")

# GET_ALL_SALES = "select sales.id, sales.created_at, sum(order_products.unit_price*quantity) as total_amount, sales_orders.id, count(order_products.id) as order_qty, sales_orders.status, sales_orders.order_date, customers.*, u1.*, u2.* from sales join sales_orders on sales.order_id==sales_orders.id join order_products on order_products.salesorder_id == sales_orders.id join customers on sales_orders.customer_id == customers.id join users u1 on sales.sell_by == u1.id join users u2 on sales.approve_by == u2.id group by sales.id;"

# Admin
INIT_ADMINS = ("create table if not exists 'user_admin' (id INTEGER, name TEXT, password TEXT, order_id "
               "INTEGER, company_access TEXT, PRIMARY KEY(id))")
GET_ALL_ADMINS = "select * from 'user_admin' where id LIKE ?"
POST_ADMINS = "insert or ignore into 'user_admin' (id, name, password, order_id, company_access) values (?, ?, ?, ?, ?)"
PUT_ADMIN_PASSWORD = "update 'user_admin' set password=? where id=?"
PUT_ADMIN_ORDER_ID = "update 'user_admin' set order_id=? where id=1"
PUT_ADMIN_COMPANY_ACCESS = "update 'user_admin' set company_access=? where id=1"

# User
INIT_USERS = ("create table if not exists 'users' (id INTEGER, name TEXT, position TEXT, start_date TEXT, quit_date "
              "TEXT, PRIMARY KEY(id))")
GET_ALL_USERS = "select * from 'users'"
GET_ALL_ACTIVE_USERS = "select * from 'users' where quit_date <> ? or quit_date is not null"
GET_ALL_ACTIVE_SPECIFIC_USERS_BY_POSITION = "select * from 'users' where (quit_date <> ? or quit_date is not null) and position = ?"
POST_ONE_USER = "insert or replace into 'users' (id, name, position, start_date, quit_date) values (?, ?, ?, ?, ?)"
PUT_USER_QUIT_DATE = "update 'users' set quit_date=? where id = ?"


# Version Alpha 0.01
# item_alter_add_market_type_query = "alter table item add column market_type TEXT"
# customer_alter_add_market_type_query = "alter table company add column market_type TEXT"
# customer_alter_table_name_query = "alter table company rename to customer"
# customer_alter_id_data_type_query = "alter table company alter column id TEXT"


# order_alter_add_printed_query = "alter table 'order' add printed BLOB"
# order_alter_add_printed_time_query = "alter table 'order' add printed_time TEXT"

class DBInterface(ABC):

    @abstractmethod
    def connect(self): pass

    @abstractmethod
    def close(self): pass


class SQLiteDatabase(DBInterface):

    def __init__(self, db_path=MAIN_DBPATH):
        self.db_path = f"{db_path}.db"

        self.connect()
        # self.update_database_schema_version(ALPHA_0_01)
        print(f"This is the version of {sqlite3.version}")
        print(f"this is sqlite version {sqlite3.sqlite_version}")

        self.cursor.execute(INIT_CUSTOMERS)
        self.cursor.execute(INIT_ITEMS)
        self.cursor.execute(INIT_PRODUCTS)
        self.cursor.execute(INIT_SALES_ORDERS)
        self.cursor.execute(INIT_ORDER_PRODUCTS)
        self.cursor.execute(INIT_USERS)
        self.cursor.execute(INIT_SALES)
        self.cursor.execute(INIT_ADMINS)
        self.cursor.execute(INIT_RECEIPTS)
        _admins = self.cursor.execute(GET_ALL_ADMINS, ['%']).fetchall()
        if _admins:
            self.cursor.executemany(POST_ADMINS, [(1, "Salesman", _admins[0][2], 0, Access.READPUSH.value)])
        else:
            self.cursor.executemany(POST_ADMINS, [(1, "Salesman", 'delvron', 0, Access.READPUSH.value)])
        self.conn.commit()
        # self.cursor.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name=item")

        # order_schema = self.cursor.fetchone()[0]
        # if 'printed' not in order_schema and 'printed_time' not in order_schema:
        #     self.cursor.execute(order_alter_add_printed_query)
        #     self.cursor.execute(order_alter_add_printed_time_query)
        self._hide_file(f"{db_path}.db")
        self.close()

    def connect(self):
        self.conn = sqlite3.connect(self.db_path, uri=True)
        self.cursor = self.conn.cursor()

    def close(self):
        self.cursor.close()
        self.conn.close()

    @staticmethod
    def _hide_file(file_path):
        try:
            # Set the hidden attribute for the file (Windows only)
            file_path = os.path.abspath(file_path)
            FILE_ATTRIBUTE_HIDDEN = 0x02
            ctypes.windll.kernel32.SetFileAttributesW(file_path, FILE_ATTRIBUTE_HIDDEN)
            print("Something")
        except Exception as e:
            print(f"Failed to hide the file: {e}")

    # def update_database_schema_version(self, _version):
    #
    #     match _version:
    #         case ALPHA_0_01 :
    #             item_schema = self.cursor.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name='item'").fetchone()[0]
    #             if 'market_type' not in item_schema:
    #                 self.cursor.execute(item_alter_add_market_type_query)
    #
    #             company_schema = self.cursor.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name='company'").fetchone()[0]
    #             print(company_schema)
    #             if 'market_type' not in company_schema:
    #                 self.cursor.execute(customer_alter_add_market_type_query)
    #                 self.cursor.execute(customer_alter_table_name_query)
    #             self.cursor.execute(customer_alter_id_data_type_query)
