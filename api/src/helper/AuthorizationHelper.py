from python_helper import ObjectHelper, StringHelper, log
from python_framework import Helper, HelperMethod

from domain import AuthorizationAccount, AuthorizationAccess, AuthorizationOperation, RequestedAuthorization, AuthorizedRequest
from helper.static import AuthorizationStaticHelper


@Helper()
class AuthorizationHelper:

    @HelperMethod(requestClass=[RequestedAuthorization.RequestedAuthorization, str, [str]])
    def getForbiddenMessage(self, requestedAuthorization, requestedResourceKey, authorizedResourceKeys):
        forbiddenMessage = 'Forbidden'
        try:
            errorMessageDomain = StringHelper.toText(StringHelper.toTitle(requestedAuthorization.domain))
            errorMessageOperation = StringHelper.toText(requestedAuthorization.operation)
            forbiddenMessage = f'''Forbidden to {errorMessageOperation.lower()} the {StringHelper.toTitle(errorMessageDomain)}: {requestedResourceKey}'''
        except Exception as exception:
            log.failure(self.getForbiddenMessage, f'Not possible to compose error message. Domain: {requestedAuthorization.domain}, operation: {requestedAuthorization.operation}', exception=exception)
        return forbiddenMessage


    @HelperMethod(requestClass=[RequestedAuthorization.RequestedAuthorization, AuthorizationAccount.AuthorizationAccount, [AuthorizationAccess], str])
    def getLogForbiddenMessage(self, requestedAuthorization, authorizationAccount, authorizedAccesses, forbiddenMessage):
        logForbiddenMessage = 'Forbidden'
        try:
            logForbiddenMessage = f'{forbiddenMessage}. {self.getLogForbiddenMessageDetails(requestedAuthorization, authorizationAccount, authorizedAccesses)}'
        except Exception as exception:
            log.failure(self.getLogForbiddenMessage, f'Not possible to compose error message. Domain: {requestedAuthorization.domain}, operation: {requestedAuthorization.operation}', exception=exception)
        return logForbiddenMessage


    @HelperMethod(requestClass=[RequestedAuthorization.RequestedAuthorization, AuthorizationAccount.AuthorizationAccount, [AuthorizationAccess]])
    def getLogForbiddenMessageDetails(self, requestedAuthorization, authorizationAccount, authorizedAccesses):
        accountErrorLogMessage = f'Account requesting: {authorizationAccount.key}'
        domainErrorLogMessage = f'Requested domain: {requestedAuthorization.domain}'
        resourceErrorLogMessage = f'Requested resources: {requestedAuthorization.resourceKeys}'
        operationErrorLogMessage = f'Requested operation: {requestedAuthorization.operation}'
        accessesErrorLogMessage = f'Allowed accesses len: {len(authorizedAccesses)}' if 5 <= len(authorizedAccesses) else f'Allowed accesses: {authorizedAccesses}'
        return f'{accountErrorLogMessage}. {domainErrorLogMessage}. {resourceErrorLogMessage}. {operationErrorLogMessage}. {accessesErrorLogMessage}'
