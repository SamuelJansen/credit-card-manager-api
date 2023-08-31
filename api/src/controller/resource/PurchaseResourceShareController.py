from python_framework import Controller, ControllerMethod, HttpStatus

from domain.SecurityContext import SecurityContext
from dto import AuthorizationAccessShareDto

@Controller(
    url = '/resource/share/purchase',
    tag = 'Resource',
    description = 'Resource controller'
    # , logRequest = True
    # , logResponse = True
)
class PurchaseResourceShareController:

    @ControllerMethod(url = '/all',
        roleRequired=[SecurityContext.ADMIN, SecurityContext.RESOURCE_ADMIN, SecurityContext.USER, SecurityContext.RESOURCE_USER],
        requestClass=[[AuthorizationAccessShareDto.AuthorizationAccessShareAllRequestDto]],
        responseClass=[[AuthorizationAccessShareDto.AuthorizationAccessShareAllRequestDto]]
    )
    def post(self, dtoList):
        self.service.resource.shareAllPurchase(dtoList)
        return [], HttpStatus.CREATED

    @ControllerMethod(url = '/all',
        roleRequired=[SecurityContext.ADMIN, SecurityContext.RESOURCE_ADMIN, SecurityContext.USER, SecurityContext.RESOURCE_USER],
        requestClass=[[AuthorizationAccessShareDto.AuthorizationAccessShareAllRequestDto]],
        responseClass=[[AuthorizationAccessShareDto.AuthorizationAccessShareAllResponseDto]]
    )
    def delete(self, dtoList):
        # self.service.resource.revokeAllPurchase(dtoList)
        return [], HttpStatus.ACCEPTED
