from python_framework import Controller, ControllerMethod, HttpStatus

from domain.SecurityContext import SecurityContext
from dto import AuthorizationAccessDto

@Controller(
    url = '/resource/transfer/purchase',
    tag = 'Resource',
    description = 'Resource controller'
    # , logRequest = True
    # , logResponse = True
)
class PurchaseResourceTransferController:

    @ControllerMethod(url = '/all',
        roleRequired=[SecurityContext.ADMIN, SecurityContext.RESOURCE_ADMIN, SecurityContext.USER, SecurityContext.RESOURCE_USER],
        requestClass=[[AuthorizationAccessDto.AuthorizationAccessAllRequestDto]],
        responseClass=[[AuthorizationAccessDto.AuthorizationAccessAllRequestDto]]
        # , logRequest = True
        # , logResponse = True
    )
    def post(self, dtoList):
        self.service.resource.transferAllPurchase(dtoList)
        return [], HttpStatus.CREATED

    @ControllerMethod(url = '/all',
        roleRequired=[SecurityContext.ADMIN, SecurityContext.RESOURCE_ADMIN, SecurityContext.USER, SecurityContext.RESOURCE_USER],
        requestClass=[[AuthorizationAccessDto.AuthorizationAccessAllRequestDto]],
        responseClass=[[AuthorizationAccessDto.AuthorizationAccessAllRequestDto]]
        # , logRequest = True
        # , logResponse = True
    )
    def put(self, dtoList):
        self.service.resource.transferAllPurchase(dtoList)
        return [], HttpStatus.CREATED
