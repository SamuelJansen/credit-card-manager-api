from python_framework import Enum, EnumItem


@Enum()
class InstallmentStatusEnumeration:
    CREATED = EnumItem()
    SCHEADULED = EnumItem()
    PROCESSING = EnumItem()
    PROCESSED = EnumItem()
    REVERTING = EnumItem()
    REVERTED = EnumItem()
    ERROR = EnumItem()
    NONE = EnumItem()


InstallmentStatus = InstallmentStatusEnumeration()
