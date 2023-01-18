from python_framework import Enum, EnumItem


@Enum()
class SecurityContextEnumeration:
    ADMIN = EnumItem()
    CREDIT_ADMIN = EnumItem()
    CREDIT_CARD_ADMIN = EnumItem()
    PURCHASE_ADMIN = EnumItem()
    INSTALLMENT_ADMIN = EnumItem()
    INVOICE_ADMIN = EnumItem()
    RESOURCE_ADMIN = EnumItem()

    USER = EnumItem()
    CREDIT_USER = EnumItem()
    CREDIT_CARD_USER = EnumItem()
    PURCHASE_USER = EnumItem()
    INSTALLMENT_USER = EnumItem()
    INVOICE_USER = EnumItem()
    RESOURCE_USER = EnumItem()


SecurityContext = SecurityContextEnumeration()
