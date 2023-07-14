from python_framework import Controller, ControllerMethod, HttpStatus

from domain.SecurityContext import SecurityContext
from dto import AuthorizationAccessShareDto

@Controller(
    url = '/resource/share/credit-card',
    tag = 'Resource',
    description = 'Resource controller'
    # , logRequest = True
    # , logResponse = True
)
class CreditCardResourceShareController:

    @ControllerMethod(url = '/all',
        roleRequired=[SecurityContext.ADMIN, SecurityContext.RESOURCE_ADMIN, SecurityContext.USER, SecurityContext.RESOURCE_USER],
        requestClass=[[AuthorizationAccessShareDto.AuthorizationAccessShareRequestDto]],
        responseClass=[[AuthorizationAccessShareDto.AuthorizationAccessShareResponseDto]]
    )
    def post(self, dtoList):
        self.service.resource.shareAllCreditCard(dtoList)
        return [], HttpStatus.CREATED

    @ControllerMethod(url = '/all',
        roleRequired=[SecurityContext.ADMIN, SecurityContext.RESOURCE_ADMIN, SecurityContext.USER, SecurityContext.RESOURCE_USER],
        requestClass=[[AuthorizationAccessShareDto.AuthorizationAccessShareRequestDto]],
        responseClass=[[AuthorizationAccessShareDto.AuthorizationAccessShareResponseDto]]
    )
    def delete(self, dtoList):
        # self.service.resource.revokeAllCreditCard(dtoList)
        return [], HttpStatus.ACCEPTED
