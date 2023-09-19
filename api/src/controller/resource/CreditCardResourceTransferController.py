from python_framework import Controller, ControllerMethod, HttpStatus

from domain.SecurityContext import SecurityContext
from dto import AuthorizationAccessDto

@Controller(
    url = '/resource/transfer/credit-card',
    tag = 'Resource',
    description = 'Resource controller'
    # , logRequest = True
    # , logResponse = True
)
class CreditCardResourceTransferController:

    @ControllerMethod(url = '/all',
        roleRequired=[SecurityContext.ADMIN, SecurityContext.RESOURCE_ADMIN, SecurityContext.USER, SecurityContext.RESOURCE_USER],
        requestClass=[[AuthorizationAccessDto.AuthorizationAccessAllRequestDto]],
        responseClass=[[AuthorizationAccessDto.AuthorizationAccessAllResponseDto]]
        # , logRequest = True
        # , logResponse = True
    )
    def post(self, dtoList):
        self.service.resource.transferAllCreditCard(dtoList)
        return [], HttpStatus.CREATED

    @ControllerMethod(url = '/all',
        roleRequired=[SecurityContext.ADMIN, SecurityContext.RESOURCE_ADMIN, SecurityContext.USER, SecurityContext.RESOURCE_USER],
        requestClass=[[AuthorizationAccessDto.AuthorizationAccessAllRequestDto]],
        responseClass=[[AuthorizationAccessDto.AuthorizationAccessAllResponseDto]]
        # , logRequest = True
        # , logResponse = True
    )
    def put(self, dtoList):
        self.service.resource.transferAllCreditCard(dtoList)
        return [], HttpStatus.CREATED

    @ControllerMethod(url = '/all',
        roleRequired=[SecurityContext.ADMIN, SecurityContext.RESOURCE_ADMIN, SecurityContext.USER, SecurityContext.RESOURCE_USER],
        requestClass=[[AuthorizationAccessDto.AuthorizationAccessAllRequestDto]],
        responseClass=[[AuthorizationAccessDto.AuthorizationAccessAllResponseDto]]
        # , logRequest = True
        # , logResponse = True
    )
    def delete(self, dtoList):
        # self.service.resource.revokeAllCreditCard(dtoList)
        return [], HttpStatus.ACCEPTED
