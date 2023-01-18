from python_helper import ObjectHelper, StringHelper
from python_framework import Helper, HelperMethod

from domain import AuthorizationAccount, AuthorizationAccess, AuthorizationOperation, RequestedAuthorization, AuthorizedRequest
from helper.static import AuthorizationStaticHelper


StringHelper.toText = StringHelper.toParagraphCase


@Helper()
class AuthorizationHelper:

    @HelperMethod(requestClass=[RequestedAuthorization.RequestedAuthorization, str, [str]])
    def getForbiddenMessage(self, requestedAuthorization, requestedResourceKey, authorizedResourceKeys):
        errorMessageDomain = StringHelper.toText(StringHelper.toTitle(requestedAuthorization.domain))
        errorMessageOperation = StringHelper.toText(requestedAuthorization.operation)
        return f'''Forbidden to {errorMessageOperation.lower()} the {StringHelper.toTitle(errorMessageDomain)}: {requestedResourceKey}'''


    @HelperMethod(requestClass=[RequestedAuthorization.RequestedAuthorization, AuthorizationAccount.AuthorizationAccount, [AuthorizationAccess], str])
    def getLogForbiddenMessage(self, requestedAuthorization, authorizationAccount, authorizedAccesses, forbiddenMessage):
        return f'{forbiddenMessage}. {self.getLogForbiddenMessageDetails(requestedAuthorization, authorizationAccount, authorizedAccesses)}'


    @HelperMethod(requestClass=[RequestedAuthorization.RequestedAuthorization, AuthorizationAccount.AuthorizationAccount, [AuthorizationAccess]])
    def getLogForbiddenMessageDetails(self, requestedAuthorization, authorizationAccount, authorizedAccesses):
        accountErrorLogMessage = f'Account requesting: {authorizationAccount.key}'
        domainErrorLogMessage = f'Requested domain: {requestedAuthorization.domain}'
        resourceErrorLogMessage = f'Requested resources: {requestedAuthorization.resourceKeys}'
        operationErrorLogMessage = f'Requested operation: {requestedAuthorization.operation}'
        accessesErrorLogMessage = f'Allowed accesses: {authorizedAccesses}'
        return f'{accountErrorLogMessage}. {domainErrorLogMessage}. {resourceErrorLogMessage}. {operationErrorLogMessage}. {accessesErrorLogMessage}'
