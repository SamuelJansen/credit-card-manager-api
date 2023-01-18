from python_helper import Constant as c
from python_helper import ObjectHelper, ReflectionHelper
from python_framework import StaticConverter, Serializer, GlobalException, StaticConverter

from domain import RequestedAuthorization
from helper.static import AuthorizationStaticHelper


def overrideDefaultValues(instance):
    instance.domain = AuthorizationStaticHelper.resolveDomain(instance, instance.domain)


def toRequestedAuthorization(thing, domain, operation):
    if ObjectHelper.isNone(thing):
        return None
    if ObjectHelper.isCollection(thing):
        return _toRequestedAuthorizationFromList(thing, operation, domain)
    domain = AuthorizationStaticHelper.resolveDomain(thing, domain)
    if AuthorizationStaticHelper.isKey(thing):
        return RequestedAuthorization.RequestedAuthorization(
            resourceKeys = [thing],
            domain = domain,
            operation = operation
        )
    if ReflectionHelper.hasAttributeOrMethod(thing, 'key'):
        return RequestedAuthorization.RequestedAuthorization(
            resourceKeys = [] if ObjectHelper.isNone(thing.key) else [thing.key],
            domain = domain,
            operation = operation
        )
    return RequestedAuthorization.RequestedAuthorization(
        resourceKeys = [
            key
            for key in StaticConverter.getValueOrDefault(thing.keyList, [])
            if ObjectHelper.isNotNone(key)
        ],
        domain = domain,
        operation = operation
    )


def _toRequestedAuthorizationFromList(instanceList, operation, domain):
    domain = AuthorizationStaticHelper.resolveDomain(instanceList, domain)
    return RequestedAuthorization.RequestedAuthorization(
        resourceKeys = list(set(
            ObjectHelper.flatMap(
                [
                    requestedAuthorization.resourceKeys
                    for requestedAuthorization in [
                        toRequestedAuthorization(instance, domain, operation)
                        for instance in instanceList
                        if ObjectHelper.isNotNone(instance)
                    ]
                ]
            )
        )),
        domain = domain,
        operation = operation
    )
