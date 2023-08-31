from python_framework import Controller, ControllerMethod, HttpStatus

from domain.SecurityContext import SecurityContext
from dto import PurchaseDto

@Controller(
    url = '/purchase',
    tag = 'Purchase',
    description = 'Purchase controller'
    # , logRequest = True
    # , logResponse = True
)
class PurchaseController:

    @ControllerMethod(url = '/<string:key>',
        roleRequired=[SecurityContext.ADMIN, SecurityContext.PURCHASE_ADMIN, SecurityContext.USER, SecurityContext.PURCHASE_USER],
        responseClass=[]
    )
    def delete(self, key=None):
        return self.service.purchase.deleteByKey(key), HttpStatus.OK


@Controller(
    url = '/purchase',
    tag = 'Purchase',
    description = 'Purchase controller'
    # , logRequest = True
    # , logResponse = True
)
class PurchaseAllController:

    @ControllerMethod(url = '/all',
        roleRequired=[SecurityContext.ADMIN, SecurityContext.PURCHASE_ADMIN, SecurityContext.USER, SecurityContext.PURCHASE_USER],
        requestParamClass=[PurchaseDto.PurchaseQueryAllDto],
        responseClass=[[PurchaseDto.PurchaseResponseDto]]
    )
    def get(self, params=None):
        return self.service.purchase.findAllByQuery(params), HttpStatus.OK


    @ControllerMethod(url = '/all',
        roleRequired=[SecurityContext.ADMIN, SecurityContext.PURCHASE_ADMIN, SecurityContext.USER, SecurityContext.PURCHASE_USER],
        requestClass=[[PurchaseDto.PurchaseRequestDto]],
        responseClass=[[PurchaseDto.PurchaseResponseDto]]
    )
    def post(self, dtoList):
        return self.service.purchase.createAll(dtoList), HttpStatus.CREATED


    @ControllerMethod(url = '/all',
        roleRequired=[SecurityContext.ADMIN, SecurityContext.PURCHASE_ADMIN, SecurityContext.USER, SecurityContext.PURCHASE_USER],
        requestClass=[[PurchaseDto.PurchaseRequestDto]],
        responseClass=[[PurchaseDto.PurchaseResponseDto]]
    )
    def delete(self, dtoList):
        return self.service.purchase.revertAll(dtoList), HttpStatus.ACCEPTED
