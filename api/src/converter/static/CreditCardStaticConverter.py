from python_helper import DateTimeHelper, ObjectHelper, ReflectionHelper
from python_framework import StaticConverter

from constant import CreditCardConstant


def overrideDefaultValues(instance, objectKeys=None):
    if ObjectHelper.isNone(instance):
        return instance
    # instance.id = instance.id if ObjectHelper.isNone(instance.id) else int(instance.id)
    instance.customLimit = StaticConverter.getValueOrDefault(instance.customLimit if ObjectHelper.isNone(instance.customLimit) else float(instance.customLimit), CreditCardConstant.DEFAULT_CUSTOM_LIMIT)
    instance.value = StaticConverter.getValueOrDefault(instance.value if ObjectHelper.isNone(instance.value) else float(instance.value), CreditCardConstant.DEFAULT_VALUE)
    instance.expirationDate = None if ObjectHelper.isNone(instance.expirationDate) else DateTimeHelper.dateOf(dateTime=addTimePotiomToDateAsStringIfNeeded(instance.expirationDate))
    instance.dueDay = StaticConverter.getValueOrDefault(instance.dueDay if ObjectHelper.isNone(instance.dueDay) else int(instance.dueDay), CreditCardConstant.DEFAULT_DUE_DAY)
    instance.closingDay = StaticConverter.getValueOrDefault(instance.closingDay if ObjectHelper.isNone(instance.closingDay) else int(instance.closingDay), CreditCardConstant.DEFAULT_CLOSING_DAY)
    return instance


def overrideDefaultQueryValues(instance, objectKeys=None):
    if ObjectHelper.isNone(instance):
        return instance
    objectKeys = StaticConverter.getValueOrDefault(objectKeys, ReflectionHelper.getAttributeNameListFromInstance(instance))
    # overrideDefaultValues(instance, objectKeys=objectKeys)
    if 'keyList' in objectKeys:
        instance.keyList = StaticConverter.getValueOrDefault(instance.keyList, [])
    return instance


def addTimePotiomToDateAsStringIfNeeded(date):
    return None if ObjectHelper.isNone(date) else f'{str(date).strip()} {DateTimeHelper.DEFAULT_TIME_BEGIN}' if ObjectHelper.equals(1, len(str(date).strip().split())) else date
