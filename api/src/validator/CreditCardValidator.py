from python_helper import ObjectHelper
from python_framework import Validator, ValidatorMethod, GlobalException, HttpStatus

from domain import AuthorizationOperation
from dto import CreditCardDto
from model import CreditCard
from converter.static import AuthorizationStaticConverter


@Validator()
class CreditCardValidator:

    @ValidatorMethod(requestClass=[CreditCard.CreditCard, float])
    def validateTransaction(self, model, limit):
        if ObjectHelper.isNone(model) or ObjectHelper.isNone(limit):
            raise GlobalException(logMessage=f'Invalid operation. Credit card: {model}, limit: {limit}', status=HttpStatus.INTERNAL_SERVER_ERROR)
        if 0 > model.limit + limit:
            raise GlobalException(message=f'Not enought funds', status=HttpStatus.BAD_REQUEST)


    @ValidatorMethod(requestClass=[str])
    def validateExistsByKey(self, key):
        if not self.service.creditCard.existsByKey(key):
            raise GlobalException(message=f'''Credit card does not exists''', status=HttpStatus.BAD_REQUEST)


    @ValidatorMethod(requestClass=[[str]])
    def validateAllExistsByKeyIn(self, keyList):
        for key in keyList:
            self.validateExistsByKey(key)


    @ValidatorMethod(requestClass=[[CreditCardDto.CreditCardRequestDto], [str]])
    def validateCreateAll(self, dtoList, existingKeyList):
        if self.service.creditCard.existsByKeyInAndLabelIn(existingKeyList, [dto.label for dto in dtoList]):
            raise GlobalException(message=f'''At least one credit card already exists''', status=HttpStatus.BAD_REQUEST)


    @ValidatorMethod(requestClass=[CreditCardDto.CreditCardRequestDto, [str]])
    def validateCreate(self, dto, existingKeyList):
        if self.service.creditCard.existsByNameInKeyIn(existingKeyList, [dto.label]):
            raise GlobalException(message=f'''The {dto.label} credit card already exists''', status=HttpStatus.BAD_REQUEST)


    @ValidatorMethod(requestClass=[[CreditCardDto.CreditCardRequestDto]])
    def validateUpdateAll(self, dtoList):
        self.validateAllExistsByKeyIn([dto.key for dto in dtoList])


    @ValidatorMethod(requestClass=[CreditCardDto.CreditCardRequestDto])
    def validateUpdate(self, dto):
        self.validateExistsByKey(dto.key)


    @ValidatorMethod(requestClass=[[str]])
    def validateDeleteAll(self, keyList):
        self.validateAllExistsByKeyIn(keyList)


    @ValidatorMethod(requestClass=[str])
    def validateDelete(self, key):
        self.validateExistsByKey(key)
