from python_framework import Controller, ControllerMethod, HttpStatus

from domain.SecurityContext import SecurityContext
from dto import CreditDto

@Controller(
    url = '/credit',
    tag = 'Credit',
    description = 'Credit controller'
    # , logRequest = True
    # , logResponse = True
)
class CreditController:

    @ControllerMethod(
        roleRequired=[SecurityContext.ADMIN, SecurityContext.CREDIT_ADMIN, SecurityContext.USER, SecurityContext.CREDIT_USER],
        requestParamClass=[CreditDto.CreditQueryAllDto],
        responseClass=[CreditDto.CreditResponseDto]
    )
    def get(self, params=None):
        return self.service.credit.findByQuery(params), HttpStatus.OK

    @ControllerMethod(
        roleRequired=[SecurityContext.ADMIN, SecurityContext.CREDIT_ADMIN, SecurityContext.USER, SecurityContext.CREDIT_USER],
        requestClass=[CreditDto.CreditRequestDto],
        responseClass=[CreditDto.CreditResponseDto]
    )
    def post(self, dto):
        return self.service.credit.create(dto), HttpStatus.CREATED

    @ControllerMethod(url = '/<string:key>',
        roleRequired=[SecurityContext.ADMIN, SecurityContext.CREDIT_ADMIN, SecurityContext.USER, SecurityContext.CREDIT_USER],
        responseClass=[]
    )
    def delete(self, key=None):
        return self.service.credit.deleteByKey(key), HttpStatus.OK


@Controller(
    url = '/credit',
    tag = 'Credit',
    description = 'Credit controller'
    # , logRequest = True
    # , logResponse = True
)
class CreditAllController:

    @ControllerMethod(url = '/all',
        roleRequired=[SecurityContext.ADMIN, SecurityContext.CREDIT_ADMIN, SecurityContext.USER, SecurityContext.CREDIT_USER],
        requestParamClass=[CreditDto.CreditQueryAllDto],
        responseClass=[[CreditDto.CreditResponseDto]]
    )
    def get(self, params=None):
        return self.service.credit.findAllByQuery(params), HttpStatus.OK


    @ControllerMethod(url = '/all',
        roleRequired=[SecurityContext.ADMIN, SecurityContext.CREDIT_ADMIN, SecurityContext.USER, SecurityContext.CREDIT_USER],
        requestClass=[[CreditDto.CreditRequestDto]],
        responseClass=[[CreditDto.CreditResponseDto]]
    )
    def post(self, dtoList):
        return self.service.credit.createAll(dtoList), HttpStatus.CREATED
