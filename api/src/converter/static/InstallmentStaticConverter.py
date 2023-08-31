from python_helper import DateTimeHelper, ObjectHelper, ReflectionHelper
from python_framework import StaticConverter

from constant import InstallmentConstant
from enumeration.InstallmentStatus import InstallmentStatus


def overrideDefaultValues(instance, objectKeys=None):
    # instance.id = instance.id if ObjectHelper.isNone(instance.id) else int(instance.id)
    instance.value = StaticConverter.getValueOrDefault(instance.value if ObjectHelper.isNone(instance.value) else float(instance.value), InstallmentConstant.DEFAULT_VALUE)
    instance.installmentAt = StaticConverter.getValueOrDefault(DateTimeHelper.of(dateTime=instance.installmentAt), DateTimeHelper.now())
    instance.order = StaticConverter.getValueOrDefault(instance.order if ObjectHelper.isNone(instance.order) else int(instance.order), InstallmentConstant.DEFAULT_ORDER)
    instance.installments = StaticConverter.getValueOrDefault(instance.installments if ObjectHelper.isNone(instance.installments) else float(instance.installments), InstallmentConstant.DEFAULT_INSTALLMENTS)
    instance.status = StaticConverter.getValueOrDefault(InstallmentStatus.map(instance.status), InstallmentConstant.DEFAULT_STATUS)
    return instance


def overrideDefaultQueryValues(instance, objectKeys=None):
    if ObjectHelper.isNone(instance):
        return instance
    instanceKeys = StaticConverter.getValueOrDefault(objectKeys, ReflectionHelper.getAttributeNameListFromInstance(instance))
    if 'keyList' in instanceKeys:
        instance.keyList = StaticConverter.getValueOrDefault(instance.keyList, [])
    if 'statusList' in instanceKeys:
        instance.statusList = StaticConverter.getValueOrDefault(instance.statusList, [])
    return instance
