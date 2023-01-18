from python_framework import Controller, ControllerMethod, HttpStatus

from domain.SecurityContext import SecurityContext
from dto import InstallmentDto

@Controller(
    url = '/installment',
    tag = 'Installment',
    description = 'Installment controller'
    , logRequest = True
    , logResponse = True
)
class InstallmentController:

    @ControllerMethod(
        roleRequired=[SecurityContext.ADMIN, SecurityContext.INSTALLMENT_ADMIN, SecurityContext.USER, SecurityContext.INSTALLMENT_USER],
        requestParamClass=[InstallmentDto.InstallmentQueryAllDto],
        responseClass=[InstallmentDto.InstallmentResponseDto]
    )
    def get(self, params=None):
        return self.service.installment.findByQuery(params), HttpStatus.OK

    @ControllerMethod(
        roleRequired=[SecurityContext.ADMIN, SecurityContext.INSTALLMENT_ADMIN, SecurityContext.USER, SecurityContext.INSTALLMENT_USER],
        requestClass=[InstallmentDto.InstallmentRequestDto],
        responseClass=[InstallmentDto.InstallmentResponseDto]
    )
    def post(self, dto):
        return self.service.installment.create(dto), HttpStatus.CREATED

    @ControllerMethod(url = '/<string:key>',
        roleRequired=[SecurityContext.ADMIN, SecurityContext.INSTALLMENT_ADMIN, SecurityContext.USER, SecurityContext.INSTALLMENT_USER],
        responseClass=[]
    )
    def delete(self, key=None):
        return self.service.installment.deleteByKey(key), HttpStatus.OK


@Controller(
    url = '/installment',
    tag = 'Installment',
    description = 'Installment controller'
    , logRequest = True
    , logResponse = True
)
class InstallmentAllController:

    @ControllerMethod(url = '/all',
        roleRequired=[SecurityContext.ADMIN, SecurityContext.INSTALLMENT_ADMIN, SecurityContext.USER, SecurityContext.INSTALLMENT_USER],
        requestParamClass=[InstallmentDto.InstallmentQueryAllDto],
        responseClass=[[InstallmentDto.InstallmentResponseDto]]
    )
    def get(self, params=None):
        return self.service.installment.findAllByQuery(params), HttpStatus.OK


    @ControllerMethod(url = '/all',
        roleRequired=[SecurityContext.ADMIN, SecurityContext.INSTALLMENT_ADMIN, SecurityContext.USER, SecurityContext.INSTALLMENT_USER],
        requestClass=[[InstallmentDto.InstallmentRequestDto]],
        responseClass=[[InstallmentDto.InstallmentResponseDto]]
    )
    def post(self, dtoList):
        return self.service.installment.createAll(dtoList), HttpStatus.CREATED

    @ControllerMethod(url = '/all',
        roleRequired=[SecurityContext.ADMIN, SecurityContext.INSTALLMENT_ADMIN, SecurityContext.USER, SecurityContext.INSTALLMENT_USER],
        requestParamClass=[InstallmentDto.InstallmentQueryAllDto],
        responseClass=[[InstallmentDto.InstallmentResponseDto]]
    )
    def patch(self, params=None):
        return self.service.installment.proccessAll(params), HttpStatus.OK
