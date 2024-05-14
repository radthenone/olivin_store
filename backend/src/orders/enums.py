import enum


class OrderStatus(enum.Enum):
    CREATED = "CREATED"
    ORDERED = "ORDERED"
    PREPARED = "PREPARED"
    SHIPPED = "SHIPPED"
    CANCELED = "CANCELED"
    DELIVERED = "DELIVERED"
    RETURNED = "RETURNED"
    DELETED = "DELETED"


class PaymentMethod(enum.Enum):
    CREDIT_CARD = "CREDIT_CARD"
    PAYPAL = "PAYPAL"
    INPOST = "INPOST"
    DHL = "DHL"
    POCZTEX = "POCZTEX"
    UPS = "UPS"
    GLS = "GLS"
