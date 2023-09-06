from python_framework import Controller, ControllerMethod, HttpStatus

from domain.SecurityContext import SecurityContext
from dto import CreditCardDto

@Controller(
    url = '/credit-card',
    tag = 'Credit Card',
    description = 'Credit Card controller'
    # , logRequest = True
    # , logResponse = True
)
class CreditCardController:

    @ControllerMethod(url = '/<string:key>',
        roleRequired=[SecurityContext.ADMIN, SecurityContext.CREDIT_CARD_ADMIN, SecurityContext.USER, SecurityContext.CREDIT_CARD_USER],
        responseClass=[]
    )
    def delete(self, key=None):
        return self.service.creditCard.deleteByKey(key), HttpStatus.ACCEPTED


@Controller(
    url = '/credit-card',
    tag = 'Credit Card',
    description = 'Credit Card controller'
    # , logRequest = True
    # , logResponse = True
)
class CreditCardAllController:

    @ControllerMethod(url = '/all',
        roleRequired=[SecurityContext.ADMIN, SecurityContext.CREDIT_CARD_ADMIN, SecurityContext.USER, SecurityContext.CREDIT_CARD_USER],
        requestParamClass=[CreditCardDto.CreditCardQueryAllDto],
        responseClass=[[CreditCardDto.CreditCardResponseDto]]
    )
    def get(self, params=None):
        return self.service.creditCard.findAllByQuery(params), HttpStatus.OK


    @ControllerMethod(url = '/all',
        roleRequired=[SecurityContext.ADMIN, SecurityContext.CREDIT_CARD_ADMIN, SecurityContext.USER, SecurityContext.CREDIT_CARD_USER],
        requestClass=[[CreditCardDto.CreditCardRequestDto]],
        responseClass=[[CreditCardDto.CreditCardResponseDto]]
    )
    def post(self, dtoList):
        return self.service.creditCard.createAll(dtoList), HttpStatus.CREATED


    @ControllerMethod(url = '/all',
        roleRequired=[SecurityContext.ADMIN, SecurityContext.CREDIT_CARD_ADMIN, SecurityContext.USER, SecurityContext.CREDIT_CARD_USER],
        requestClass=[[CreditCardDto.CreditCardRequestDto]],
        responseClass=[[CreditCardDto.CreditCardResponseDto]]
    )
    def delete(self, dtoList):
        return self.service.creditCard.revertAll(dtoList), HttpStatus.CREATED
