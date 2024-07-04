from dataclasses import dataclass
from datetime import datetime


@dataclass
class Product:
    Product_number:int
    Date: datetime
    Quantity: int
    Unit_sale_price: float
    Retailer_code: int

    def __hash__(self):
        return hash(self.Product_number)
