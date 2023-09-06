from python_helper import ObjectHelper, ReflectionHelper, log
from python_framework import StaticConverter


def overrideDefaultQueryValues(instance, objectKeys=None):
    if ObjectHelper.isNone(instance):
        return instance
    instanceKeys = StaticConverter.getValueOrDefault(objectKeys, ReflectionHelper.getAttributeNameListFromInstance(instance))
    if ObjectHelper.isEmpty(instanceKeys):
        raise Exception('outch')
    if ObjectHelper.isNotEmpty(instanceKeys):
        for objectKey in [
            objectKey
            for objectKey in instanceKeys
            if objectKey.endswith('List')
        ]:
            ReflectionHelper.setAttributeOrMethod(instance, objectKey, StaticConverter.getValueOrDefault(ReflectionHelper.getAttributeOrMethod(instance, objectKey), []))
    return instance