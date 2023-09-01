import datetime
from python_helper import Constant as c
from python_helper import DateTimeHelper
from python_framework import Helper, HelperMethod

from constant import IntervalConstant
from helper.static import IntervalStaticHelper
from dto import CreditCardDto, PurchaseDto


@Helper()
class InstallmentHelper:

    @HelperMethod(requestClass=[PurchaseDto.PurchaseResponseDto, CreditCardDto.CreditCardResponseDto, int])
    def getInstallmentAt(self, responseDto, creditCardResponseDto, nthInstallment):
        closingDateTime = self.getCurrentClosingDateTime(responseDto.purchaseAt, creditCardResponseDto)
        dueDateTime = self.getCurrentDueDateTime(responseDto.purchaseAt, creditCardResponseDto)
        if responseDto.purchaseAt >= closingDateTime:
            nextPurchaseDateTime = DateTimeHelper.of(dateTime = DateTimeHelper.plusMonths(responseDto.purchaseAt, months=1))
            return DateTimeHelper.of(
                date=DateTimeHelper.dateOf(dateTime=DateTimeHelper.plusMonths(nextPurchaseDateTime, months=nthInstallment)),
                time=DateTimeHelper.timeOf(dateTime=nextPurchaseDateTime)
            )
        currentPurchaseDateTime = DateTimeHelper.of(dateTime=responseDto.purchaseAt)
        return DateTimeHelper.of(
            date=DateTimeHelper.dateOf(dateTime=DateTimeHelper.plusMonths(currentPurchaseDateTime, months=nthInstallment)),
            time=DateTimeHelper.timeOf(dateTime=currentPurchaseDateTime)
        )
    

    @HelperMethod(requestClass=[datetime.datetime, CreditCardDto.CreditCardResponseDto])
    def getCurrentClosingDateTime(self, purchaseAt, creditCardResponseDto):
        return IntervalStaticHelper.getCurrentClosingDateTime(purchaseAt, creditCardResponseDto.closingDay, creditCardResponseDto.dueDay, IntervalConstant.CLOSING_DAY_REFERENCE)


    @HelperMethod(requestClass=[datetime.datetime, CreditCardDto.CreditCardResponseDto])
    def getNextClosingDateTime(self, purchaseAt, creditCardResponseDto):
        return IntervalStaticHelper.getNextClosingDateTime(purchaseAt, creditCardResponseDto.closingDay, creditCardResponseDto.dueDay, IntervalConstant.CLOSING_DAY_REFERENCE)


    @HelperMethod(requestClass=[datetime.datetime, CreditCardDto.CreditCardResponseDto])
    def getCurrentDueDateTime(self, purchaseAt, creditCardResponseDto):
        return IntervalStaticHelper.getCurrentDueDateTime(purchaseAt, creditCardResponseDto.closingDay, creditCardResponseDto.dueDay, IntervalConstant.CLOSING_DAY_REFERENCE)


    @HelperMethod(requestClass=[datetime.datetime, CreditCardDto.CreditCardResponseDto])
    def getNextDueDateTime(self, purchaseAt, creditCardResponseDto):
        return IntervalStaticHelper.getNextDueDateTime(purchaseAt, creditCardResponseDto.closingDay, creditCardResponseDto.dueDay, IntervalConstant.CLOSING_DAY_REFERENCE)
