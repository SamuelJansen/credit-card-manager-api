import datetime
from python_helper import Constant as c
from python_helper import DateTimeHelper
from python_framework import Helper, HelperMethod

from constant import IntervalConstant
from helper.static import IntervalStaticHelper
from dto import CreditCardDto


FIRST_MONTH_DAY = 1


@Helper()
class InvoiceHelper:

    @HelperMethod(requestClass=[datetime.datetime, CreditCardDto.CreditCardResponseDto])
    def getCurrentClosingDateTime(self, invoiceDateTime, creditCardResponseDto):
        return IntervalStaticHelper.getCurrentClosingDateTime(invoiceDateTime, creditCardResponseDto.closingDay, creditCardResponseDto.dueDay, IntervalConstant.DUE_DAY_REFERENCE)


    @HelperMethod(requestClass=[datetime.datetime, CreditCardDto.CreditCardResponseDto])
    def getNextClosingDateTime(self, invoiceDateTime, creditCardResponseDto):
        return IntervalStaticHelper.getNextClosingDateTime(invoiceDateTime, creditCardResponseDto.closingDay, creditCardResponseDto.dueDay, IntervalConstant.DUE_DAY_REFERENCE)


    @HelperMethod(requestClass=[datetime.datetime, CreditCardDto.CreditCardResponseDto])
    def getCurrentDueDateTime(self, invoiceDateTime, creditCardResponseDto):
        return IntervalStaticHelper.getCurrentDueDateTime(invoiceDateTime, creditCardResponseDto.closingDay, creditCardResponseDto.dueDay, IntervalConstant.DUE_DAY_REFERENCE)
    

    @HelperMethod(requestClass=[datetime.datetime, CreditCardDto.CreditCardResponseDto])
    def getNextDueDateTime(self, invoiceDateTime, creditCardResponseDto):
        return IntervalStaticHelper.getNextDueDateTime(invoiceDateTime, creditCardResponseDto.closingDay, creditCardResponseDto.dueDay, IntervalConstant.DUE_DAY_REFERENCE)
