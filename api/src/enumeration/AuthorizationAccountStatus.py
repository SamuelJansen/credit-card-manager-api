from python_framework import Enum, EnumItem


@Enum()
class AuthorizationAccountStatusEnumeration:
    ACTIVE = EnumItem()
    ACTIVE_WITH_PENDENCIES = EnumItem()
    INACTIVE = EnumItem()
    NONE = EnumItem()


AuthorizationAccountStatus = AuthorizationAccountStatusEnumeration()
