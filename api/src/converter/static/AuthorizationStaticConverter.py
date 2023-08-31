from python_helper import Constant as c
from python_helper import ObjectHelper, ReflectionHelper
from python_framework import StaticConverter, Serializer, GlobalException, StaticConverter

from domain import RequestedAuthorization
from helper.static import AuthorizationStaticHelper


def overrideDefaultValues(instance):
    instance.domain = AuthorizationStaticHelper.resolveDomain(instance, instance.domain)


def toRequestedAuthorization(requestedResourceOrRequestedResourcetList, domain, operation):
    requestedAuthorization = toUnfilteredRequestedAuthorization(requestedResourceOrRequestedResourcetList, domain, operation)
    requestedAuthorization.resourceKeys = [key for key in requestedAuthorization.resourceKeys if ObjectHelper.isNotNone(key)]
    return requestedAuthorization


def toRequestedAuthorizationFromList(requestedResourceList, domain, operation):
    requestedAuthorization = toUnfilteredRequestedAuthorizationFromList(requestedResourceList, domain, operation)
    requestedAuthorization.resourceKeys = [key for key in requestedAuthorization.resourceKeys if ObjectHelper.isNotNone(key)]
    return requestedAuthorization
    


def toUnfilteredRequestedAuthorization(requestedResourceOrRequestedResourcetList, domain, operation):
    if ObjectHelper.isNone(requestedResourceOrRequestedResourcetList):
        return None
    if ObjectHelper.isCollection(requestedResourceOrRequestedResourcetList):
        return toUnfilteredRequestedAuthorizationFromList(requestedResourceOrRequestedResourcetList, operation, domain)
    domain = AuthorizationStaticHelper.resolveDomain(requestedResourceOrRequestedResourcetList, domain)
    if AuthorizationStaticHelper.isKey(requestedResourceOrRequestedResourcetList):
        return RequestedAuthorization.RequestedAuthorization(
            resourceKeys = [requestedResourceOrRequestedResourcetList],
            domain = domain,
            operation = operation
        )
    if ReflectionHelper.hasAttributeOrMethod(requestedResourceOrRequestedResourcetList, 'key'):
        return RequestedAuthorization.RequestedAuthorization(
            resourceKeys = [requestedResourceOrRequestedResourcetList.key],
            domain = domain,
            operation = operation
        )
    return RequestedAuthorization.RequestedAuthorization(
        resourceKeys = [
            key
            for key in StaticConverter.getValueOrDefault(requestedResourceOrRequestedResourcetList.keyList, [])
        ],
        domain = domain,
        operation = operation
    )


def toUnfilteredRequestedAuthorizationFromList(requestedResourceList, operation, domain):
    domain = AuthorizationStaticHelper.resolveDomain(requestedResourceList, domain)
    return RequestedAuthorization.RequestedAuthorization(
        resourceKeys = list(set(
            ObjectHelper.flatMap(
                [
                    requestedAuthorization.resourceKeys
                    for requestedAuthorization in [
                        toUnfilteredRequestedAuthorization(instance, domain, operation)
                        for instance in requestedResourceList
                    ]
                ]
            )
        )),
        domain = domain,
        operation = operation
    )
