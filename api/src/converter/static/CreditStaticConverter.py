from python_helper import DateTimeHelper, ObjectHelper, ReflectionHelper
from python_framework import StaticConverter

from constant import CreditConstant
from converter.static import DefaultStaticConverter


def overrideDefaultValues(instance, objectKeys=None):
    # instance.id = instance.id if ObjectHelper.isNone(instance.id) else int(instance.id)
    instance.limit = StaticConverter.getValueOrDefault(instance.limit if ObjectHelper.isNone(instance.limit) else float(instance.limit), CreditConstant.DEFAULT_LIMIT)
    instance.customLimit = StaticConverter.getValueOrDefault(instance.customLimit if ObjectHelper.isNone(instance.customLimit) else float(instance.customLimit), CreditConstant.DEFAULT_CUSTOM_LIMIT)
    instance.value = StaticConverter.getValueOrDefault(instance.value if ObjectHelper.isNone(instance.value) else float(instance.value), CreditConstant.DEFAULT_VALUE)
    return instance


def overrideDefaultQueryValues(instance, objectKeys=None):
    return DefaultStaticConverter.overrideDefaultQueryValues(instance, objectKeys=objectKeys)
