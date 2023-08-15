from python_helper import ObjectHelper
from python_framework import Validator, ValidatorMethod, GlobalException, HttpStatus

from domain import AuthorizationOperation
from dto import CreditDto
from model import Credit
from converter.static import AuthorizationStaticConverter


@Validator()
class CreditValidator:

    @ValidatorMethod(requestClass=[Credit.Credit, float])
    def validateTransaction(self, model, value):
        if model.customLimit > value:
            raise GlobalException(message='Not enought funds', status=HttpStatus.BAD_REQUEST)
