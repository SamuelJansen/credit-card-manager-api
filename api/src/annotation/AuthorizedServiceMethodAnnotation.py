from python_helper import Constant as c
from python_helper import ReflectionHelper, ObjectHelper, log, Function
from python_framework import FlaskManager, Serializer

from domain import AuthorizationOperation
from converter.static import AuthorizationStaticConverter
from helper.static import AuthorizationStaticHelper


# @Function
# def Service() :
#     def Wrapper(OuterClass, *args, **kwargs):
#         log.wrapper(Service,f'''wrapping {OuterClass.__name__}''')
#         class InnerClass(OuterClass):
#             def __init__(self,*args,**kwargs):
#                 log.wrapper(OuterClass,f'in {InnerClass.__name__}.__init__(*{args},**{kwargs})')
#                 apiInstance = FlaskManager.getApi()
#                 OuterClass.__init__(self,*args,**kwargs)
#                 self.service = apiInstance.resource.service
#                 self.client = apiInstance.resource.client
#                 self.emitter = apiInstance.resource.emitter
#                 self.repository = apiInstance.resource.repository
#                 self.validator = apiInstance.resource.validator
#                 self.mapper = apiInstance.resource.mapper
#                 self.helper = apiInstance.resource.helper
#                 self.converter = apiInstance.resource.converter
#                 self.globals = apiInstance.globals
#         ReflectionHelper.overrideSignatures(InnerClass, OuterClass)
#         return InnerClass
#     return Wrapper


@Function
def AuthorizedServiceMethod(requestClass=None, operations=None):
    serviceMethodClass = requestClass
    serviceMethodOperations = getAuthorizedOperations(operations)
    def innerMethodWrapper(resourceInstanceMethod,*args,**kwargs) :
        log.wrapper(AuthorizedServiceMethod,f'''wrapping {resourceInstanceMethod.__name__}''')
        def innerResourceInstanceMethod(*args,**kwargs) :
            resourceInstance = args[0]
            lockKey = resourceInstance.service.security.lockTransaction()
            try :
                serviceMethodDomain = getAuthorizedDomain(args[0], serviceMethodClass)
                args = handleAuthorizationAndUpdateArgsBeforeExecuteTheServiceMethod(args, serviceMethodDomain, serviceMethodOperations)
                FlaskManager.validateArgs(args,requestClass,innerResourceInstanceMethod)
                methodReturn = resourceInstanceMethod(*args,**kwargs)
                createOrUpdateAccessesAfterExceutedServiceMethod(args, serviceMethodDomain, serviceMethodOperations, methodReturn)
            except Exception as exception :
                FlaskManager.raiseAndHandleGlobalException(exception, resourceInstance, resourceInstanceMethod)
            resourceInstance.service.security.unlockTransaction(lockKey)
            return methodReturn
        ReflectionHelper.overrideSignatures(innerResourceInstanceMethod, resourceInstanceMethod)
        return innerResourceInstanceMethod
    return innerMethodWrapper


def handleAuthorizationAndUpdateArgsBeforeExecuteTheServiceMethod(args, serviceMethodDomain, serviceMethodOperations):
    if 1 >= len(args):
        raise Exception('Bad implementation of @AuthorizedServiceMethod. The resource cannot be None')
    resourceInstance = args[0]
    requestedResource = args[1]
    authorizedRequest = resourceInstance.validator.security.validateAuthorization(
        AuthorizationStaticConverter.toRequestedAuthorization(
            requestedResource,
            serviceMethodDomain,
            serviceMethodOperations
        )
    )
    evaluateAutenticationIntegrity(requestedResource, authorizedRequest)
    return [
        *args,
        authorizedRequest
    ]


def createOrUpdateAccessesAfterExceutedServiceMethod(args, serviceMethodDomain, serviceMethodOperations, methodReturn):
    resourceInstance = args[0]
    requestedResource = args[1]
    resourceInstance.service.security.createOrUpdateOrDeleteAccesses(
        getResourceKeys(args, serviceMethodDomain, serviceMethodOperations, methodReturn),
        serviceMethodDomain,
        serviceMethodOperations
    )


def getResourceKeys(args, serviceMethodDomain, serviceMethodOperations, methodReturn):
    if ObjectHelper.isNotNone(methodReturn):
        if ObjectHelper.isNotTuple(methodReturn):
            return AuthorizationStaticConverter.toRequestedAuthorization(methodReturn, serviceMethodDomain, serviceMethodOperations).resourceKeys
        return AuthorizationStaticConverter.toRequestedAuthorization(methodReturn[0], serviceMethodDomain, serviceMethodOperations).resourceKeys
    return AuthorizationStaticConverter.toRequestedAuthorization(args[1], serviceMethodDomain, serviceMethodOperations).resourceKeys


def getAuthorizedOperations(operations):
    if ObjectHelper.isEmpty(operations):
        raise Exception('Bad implementation of @AuthorizedServiceMethod. The operations=[] parameter cannot be empty')
    if ObjectHelper.isEmpty(operations):
        raise Exception('Missing implementation of @AuthorizedServiceMethod. The operations=[] parameter can only have one argument for the moment')
    return operations[0]


def getAuthorizedDomain(service, requestClass):
    serviceName = ReflectionHelper.getClassName(service)
    return AuthorizationStaticHelper.resolveDomain(None, serviceName.replace('Service', ''))
    if ObjectHelper.isEmpty(requestClass):
        raise Exception('Bad implementation of @AuthorizedServiceMethod. The requestClass=[] parameter cannot be empty')
    if ObjectHelper.isEmpty(requestClass[0]):
        raise Exception('Bad implementation of @AuthorizedServiceMethod. The requestClass=[[]] parameter cannot be empty')
    if ObjectHelper.isCollection(requestClass[0]):
        return requestClass[0][0]
    return requestClass[0]


def evaluateAutenticationIntegrity(requestedResource, authorizedRequest):
    # log.prettyPython(evaluateAutenticationIntegrity, 'requestedResource', Serializer.getObjectAsDictionary(requestedResource), logLevel=log.DEBUG)
    # log.prettyPython(evaluateAutenticationIntegrity, 'authorizedRequest', Serializer.getObjectAsDictionary(authorizedRequest), logLevel=log.DEBUG)
    ...
