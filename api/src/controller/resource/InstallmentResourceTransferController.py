from python_framework import Controller, ControllerMethod, HttpStatus

from domain.SecurityContext import SecurityContext
from dto import AuthorizationAccessDto

@Controller(
    url = '/resource/transfer/installment',
    tag = 'Resource',
    description = 'Resource controller'
    # , logRequest = True
    # , logResponse = True
)
class InstallmentResourceTransferController:

    @ControllerMethod(url = '/all',
        roleRequired=[SecurityContext.ADMIN, SecurityContext.RESOURCE_ADMIN, SecurityContext.USER, SecurityContext.RESOURCE_USER],
        requestClass=[[AuthorizationAccessDto.AuthorizationAccessAllRequestDto]],
        responseClass=[[AuthorizationAccessDto.AuthorizationAccessAllRequestDto]]
    )
    def post(self, dtoList):
        self.service.resource.transferAllInstallment(dtoList)
        return [], HttpStatus.CREATED
