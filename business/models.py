import datetime
from dataclasses import dataclass, field
from enum import Enum


@dataclass
class CustomerType(Enum):
    NORMAL = "Normal"
    SPECIAL = "Special"

    @staticmethod
    def values():
        return [item.value for item in CustomerType]

    @staticmethod
    def names():
        return [item.name for item in CustomerType]


class OrderStatus(Enum):
    PENDING = 'Pending'
    FINISHED = 'Finished'
    CANCELLED = 'Cancelled'

    @staticmethod
    def values():
        return [item.value for item in OrderStatus]

    @staticmethod
    def names():
        return [item.name for item in OrderStatus]


@dataclass
class Access(Enum):
    ALL = "All"
    READ = "Read"
    READPUSH = "Read-Add"
    READPUT = "Read-Update"
    DELETE = "Delete"

    @staticmethod
    def values():
        return [item.value for item in Access]

    @staticmethod
    def names():
        return [item.name for item in Access]


@dataclass
class Role(Enum):
    OFFICE = "Office"
    SALES = "Sales"

    @staticmethod
    def values():
        return [item.value for item in Role]

    @staticmethod
    def names():
        return [item.name for item in Role]


@dataclass
class User:
    id: int
    name: str
    position: Role
    start_date: str
    quit_date: str


@dataclass
class Customer:
    id: int
    name: str
    address: str
    phno: str
    serial_no: str
    installed_date: str
    customer_type: CustomerType
    deactivated: bool


@dataclass
class Item:
    item_code: int
    name: str
    measurement: str


@dataclass
class Product:
    id: int
    local_price: int
    distributor_price: int
    defined_qty: int
    item: Item


@dataclass
class OrderProduct:
    id: int
    unit_price: int
    qty: int
    defined_distributor_qty: int
    remark: str
    item: Item


@dataclass
class SalesOrder:
    id: int
    status: OrderStatus
    order_date: str
    company: Customer
    order_products: list[OrderProduct] = field(default_factory=list)

    def __post_init__(self):
        self.order_date = datetime.datetime.strptime(self.order_date, '%Y-%m-%d').strftime('%d-%m-%Y')


@dataclass
class Receipt:
    id: int
    sale_id: int
    sale_amount: int
    received_amount: int
    balance: int
    received_date: str
    remark: str
    customer: Customer

    def __post_init__(self):
        self.received_date = datetime.datetime.strptime(self.received_date, '%Y-%m-%d').strftime('%d-%m-%Y')


@dataclass
class Sale:
    id: int
    created_at: str
    sales_order: SalesOrder
    sell_by: User
    approve_by: User
    receipts: list[Receipt] = field(default_factory=list)

    def __post_init__(self):
        self.created_at = datetime.datetime.strptime(self.created_at, '%Y-%m-%d').strftime('%d-%m-%Y')




@dataclass
class UserAdmin:
    id: int
    name: str
    pwd: str
    order_id: int
    company_access: Access
