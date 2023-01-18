from python_helper import DateTimeHelper, ObjectHelper, ReflectionHelper
from python_framework import StaticConverter

from constant import PurchaseConstant


def overrideDefaultValues(instance, objectKeys=None):
    # instance.id = instance.id if ObjectHelper.isNone(instance.id) else int(instance.id)
    instance.value = StaticConverter.getValueOrDefault(instance.value if ObjectHelper.isNone(instance.value) else float(instance.value), PurchaseConstant.DEFAULT_VALUE)
    instance.installments = StaticConverter.getValueOrDefault(instance.installments if ObjectHelper.isNone(instance.installments) else int(instance.installments), PurchaseConstant.DEFAULT_INSTALLMENTS)
    instance.purchaseAt = StaticConverter.getValueOrDefault(DateTimeHelper.of(dateTime=instance.purchaseAt), DateTimeHelper.now())
    return instance


def overrideDefaultQueryValues(instance, objectKeys=None):
    if ObjectHelper.isNone(instance):
        return instance
    objectKeys = StaticConverter.getValueOrDefault(objectKeys, ReflectionHelper.getAttributeNameListFromInstance(instance))
    # overrideDefaultValues(instance, objectKeys=objectKeys)
    if 'keyList' in objectKeys:
        instance.keyList = StaticConverter.getValueOrDefault(instance.keyList, [])
    return instance
