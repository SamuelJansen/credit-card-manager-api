from python_helper import Constant as c
from python_helper import ReflectionHelper, ObjectHelper, StringHelper
from python_framework import StaticConverter, Serializer, GlobalException

from domain import AuthorizationOperation


KW_ALL = 'All'
KW_QUERY = 'All'
KW_PARAM = 'Param'
KW_HEADER = 'Header'
SPECIAL_TERM_LIST = [
    Serializer.MODEL_SUFIX,
    Serializer.DTO_SUFIX,
    Serializer.LIST_SUFIX,
    KW_ALL,
    KW_QUERY,
    KW_PARAM,
    KW_HEADER,
    *Serializer.MESO_SUFIX_LIST
]


def getDomain(thing):
    if ObjectHelper.isNone(thing):
        _raiseDomainNotFoundException()
    if ReflectionHelper.isClass(thing):
        return _getDomainFromClass(thing)
    if ObjectHelper.isCollection(thing):
        return _getDomainFromInstanceList(thing)
    return _getDomainFromInstance(thing)


def resolveDomain(thing, domain):
    if ObjectHelper.isNone(domain):
        return getDomain(thing)
    elif isKey(thing) or isinstance(domain, str):
        return _getDomainFromName(domain)
    elif ReflectionHelper.isClass(domain):
        return _getDomainFromClass(domain)
    return getDomain(thing)


def isKey(thing):
    return isinstance(thing, str) and StringHelper.isNotBlank(thing)


def isForbiddenCondition(operation, requestedResourceKey, authorizedResourceKeys):
    if operation in AuthorizationOperation.WRITTING_OPERATIONS:
        if operation in AuthorizationOperation.CREATE_OPERATIONS:
            return (
                requestedResourceKey in authorizedResourceKeys
            )
        if operation in AuthorizationOperation.UPDATE_OPERATIONS:
            return (
                ObjectHelper.isNone(requestedResourceKey) or
                requestedResourceKey not in authorizedResourceKeys
            )
    elif operation in AuthorizationOperation.READDING_OPERATIONS:
        return (
            requestedResourceKey not in authorizedResourceKeys
        )
    return False


def _getDomainFromClass(instance):
    return _getDomainFromName(ReflectionHelper.getName(instance))


def _getDomainFromInstance(instance):
    return _getDomainFromName(ReflectionHelper.getClassName(instance))


def _getDomainFromInstanceList(instanceList):
    _getDomainFromInstance(_getFirstDomainInstance(instanceList))


def _getFirstDomainInstance(instanceList):
    for instance in instanceList:
        return instance
    _raiseDomainNotFoundException()


def _getDomainFromName(name):
    if ObjectHelper.isNotNone(name):
        nameAsTitleList = StringHelper.toTitle(name).split()
        for specialTerm in SPECIAL_TERM_LIST:
            if specialTerm in nameAsTitleList:
                nameAsTitleList.remove(specialTerm)
        name = StringHelper.join(nameAsTitleList, character=c.BLANK)
        return name if ObjectHelper.isNeitherNoneNorBlank(name) else _raiseDomainNotFoundException()
    else:
        _raiseDomainNotFoundException()


def _raiseDomainNotFoundException():
    raise GlobalException(logMessage='Not possible to evaluate domain')
