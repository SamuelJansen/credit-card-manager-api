from python_helper import ObjectHelper
from python_framework import Validator, ValidatorMethod, GlobalException, HttpStatus

from domain import AuthorizationAccount, AuthorizationAccess, AuthorizationOperation, RequestedAuthorization, AuthorizedRequest
from helper.static import AuthorizationStaticHelper


INVALID_WRITTING_OPERATION_FORBIDDEN_MESSAGE = 'Invalid writting operation'
INVALID_READDING_OPERATION_FORBIDDEN_MESSAGE = 'Invalid readding operation'


@Validator()
class SecurityValidator:

    @ValidatorMethod(requestClass=[RequestedAuthorization.RequestedAuthorization])
    def validateAuthorization(self, requestedAuthorization):
        authorizationAccount = self.service.security.getAuthorizationAccount()
        authorizedAccesses = authorizationAccount.getAccessesByDomainAndOperation(
            requestedAuthorization.domain,
            requestedAuthorization.operation
        )
        self._validateWrittingOperation(requestedAuthorization, authorizationAccount, authorizedAccesses)
        self._validateReaddingOperation(requestedAuthorization, authorizationAccount, authorizedAccesses)
        authorizedResourceKeys = [
            access.resourceKey
            for access in authorizedAccesses
        ]
        ###- if ObjectHelper.isEmpty(authorizedResourceKeys) and requestedAuthorization.operation in [AuthorizationOperation.GET, AuthorizationOperation.PUT, AuthorizationOperation.PATCH, AuthorizationOperation.DELETE]:
        if ObjectHelper.isEmpty(authorizedResourceKeys) and requestedAuthorization.operation in [AuthorizationOperation.PUT, AuthorizationOperation.PATCH, AuthorizationOperation.DELETE]:
            ###- if ObjectHelper.isEmpty(authorizedResourceKeys) and requestedAuthorization.operation in [AuthorizationOperation.PUT, AuthorizationOperation.PATCH, AuthorizationOperation.DELETE]:
            raise GlobalException(message=f'The account {authorizationAccount.key} has no access to the {requestedAuthorization.domain} resource', logMessage='Authorized resource key cannot be empty', status=HttpStatus.FORBIDDEN)
        return AuthorizedRequest.AuthorizedRequest(
            account = authorizationAccount,
            domain = requestedAuthorization.domain,
            operation = requestedAuthorization.operation,
            resourceKeys = authorizedResourceKeys
        )


    @ValidatorMethod(requestClass=[RequestedAuthorization.RequestedAuthorization, AuthorizationAccount.AuthorizationAccount, [AuthorizationAccess]])
    def _validateWrittingOperation(self, requestedAuthorization, authorizationAccount, authorizedAccesses):
        if (
            ObjectHelper.isNotNone(requestedAuthorization.resourceKeys) and
            requestedAuthorization.operation in AuthorizationOperation.WRITTING_OPERATIONS
        ):
            self._validateForbiddenResourceKey(requestedAuthorization, authorizationAccount, authorizedAccesses, INVALID_WRITTING_OPERATION_FORBIDDEN_MESSAGE)


    @ValidatorMethod(requestClass=[RequestedAuthorization.RequestedAuthorization, AuthorizationAccount.AuthorizationAccount, [AuthorizationAccess]])
    def _validateReaddingOperation(self, requestedAuthorization, authorizationAccount, authorizedAccesses):
        if (
            ObjectHelper.isNotNone(requestedAuthorization.resourceKeys) and
            requestedAuthorization.operation in AuthorizationOperation.READDING_OPERATIONS
        ):
            self._validateForbiddenResourceKey(requestedAuthorization, authorizationAccount, authorizedAccesses, INVALID_READDING_OPERATION_FORBIDDEN_MESSAGE)


    @ValidatorMethod(requestClass=[RequestedAuthorization.RequestedAuthorization, AuthorizationAccount.AuthorizationAccount, [AuthorizationAccess], str])
    def _validateForbiddenResourceKey(self, requestedAuthorization, authorizationAccount, authorizedAccesses, forbiddenMessage):
        authorizedResourceKeys = [
            access.resourceKey
            for access in authorizedAccesses
        ]
        for resourceKey in requestedAuthorization.resourceKeys:
            if AuthorizationStaticHelper.isForbiddenCondition(requestedAuthorization.operation, resourceKey, authorizedResourceKeys):
                raise GlobalException(
                    message = self.helper.authorization.getForbiddenMessage(requestedAuthorization, resourceKey, authorizedResourceKeys),
                    logMessage = self.helper.authorization.getLogForbiddenMessage(requestedAuthorization, authorizationAccount, authorizedAccesses, forbiddenMessage),
                    status = HttpStatus.FORBIDDEN
                )
