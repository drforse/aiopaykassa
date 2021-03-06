import decimal
from typing import Literal

from pydantic import Field

import aiopaykassa
from ..base import PayKassaEndpoint, Request
from ...enums import Currency, System, ShopClient
from ...exceptions import AioPayKassaError
from ...types import NewOrder


class CreateOrderEndpoint(PayKassaEndpoint):
    __returning__ = NewOrder

    order_id: int = Field(api_mutation=str)
    amount: decimal.Decimal
    currency: Currency
    system: System
    comment: str
    # check if it can be not False (Field(False, const=True))
    phone: Literal[False] = Field(False, api_mutation=lambda v: str(v).lower())
    paid_commission: ShopClient = ShopClient.SHOP

    def url(self) -> str:
        return f"https://paykassa.app/sci/{aiopaykassa.__sci_version__}/index.php"

    def build_request(self, credentials: dict[str, str | int] = None, test_mode: bool = False) -> Request:
        if credentials is None:
            raise AioPayKassaError("Credentials are required")
        return Request(
            data=self.api_dict() | {"test": str(test_mode).lower(),
                                    "func": "sci_create_order_get_data"} | credentials
        )
