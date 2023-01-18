import datetime
from python_helper import Constant as c
from python_helper import DateTimeHelper
from python_framework import Helper, HelperMethod

from constant import InstallmentConstant
from helper.static import MathStaticHelper
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
        # dateNow = str(DateTimeHelper.dateNow())
        # return DateTimeHelper.of(dateTime=f'{dateNow.split(c.DASH)[0]}{c.DASH}{dateNow.split(c.DASH)[1]}{c.DASH}{creditCardResponseDto.closingDay:02} {InstallmentConstant.DEFAULT_CLOSING_TIME}')
        purchaseAtAsString = str(purchaseAt)
        return DateTimeHelper.plusMonths(
            DateTimeHelper.of(dateTime=f'{purchaseAtAsString.split(c.DASH)[0]}{c.DASH}{purchaseAtAsString.split(c.DASH)[1]}{c.DASH}{creditCardResponseDto.closingDay:02} {InstallmentConstant.DEFAULT_CLOSING_TIME}'),
            months = 1
        )

    @HelperMethod(requestClass=[datetime.datetime, CreditCardDto.CreditCardResponseDto])
    def getNextClosingDateTime(self, responseDto, creditCardResponseDto):
        # dateNow = str(DateTimeHelper.dateNow())
        # return DateTimeHelper.plusMonths(DateTimeHelper.of(dateTime=f'{dateNow.split(c.DASH)[0]}{c.DASH}{dateNow.split(c.DASH)[1]}{c.DASH}{creditCardResponseDto.closingDay:02} {InstallmentConstant.DEFAULT_CLOSING_TIME}'), months=1)
        purchaseAtAsString = str(purchaseAt)
        return DateTimeHelper.plusMonths(
            DateTimeHelper.plusMonths(DateTimeHelper.of(dateTime=f'{purchaseAtAsString.split(c.DASH)[0]}{c.DASH}{purchaseAtAsString.split(c.DASH)[1]}{c.DASH}{creditCardResponseDto.closingDay:02} {InstallmentConstant.DEFAULT_CLOSING_TIME}'), months=1),
            months = 1
        )

    @HelperMethod(requestClass=[datetime.datetime, CreditCardDto.CreditCardResponseDto])
    def getCurrentDueDateTime(self, purchaseAt, creditCardResponseDto):
        # dateNow = str(DateTimeHelper.dateNow())
        # return DateTimeHelper.of(dateTime=f'{dateNow.split(c.DASH)[0]}{c.DASH}{dateNow.split(c.DASH)[1]}{c.DASH}{creditCardResponseDto.dueDay:02} {InstallmentConstant.DEFAULT_DUE_TIME}')
        purchaseAtAsString = str(purchaseAt)
        return DateTimeHelper.plusMonths(
            DateTimeHelper.of(dateTime=f'{purchaseAtAsString.split(c.DASH)[0]}{c.DASH}{purchaseAtAsString.split(c.DASH)[1]}{c.DASH}{creditCardResponseDto.dueDay:02} {InstallmentConstant.DEFAULT_DUE_TIME}'),
            months = 1
        )

    @HelperMethod(requestClass=[datetime.datetime, CreditCardDto.CreditCardResponseDto])
    def getNextDueDateTime(self, purchaseAt, creditCardResponseDto):
        # dateNow = str(DateTimeHelper.dateNow())
        # return DateTimeHelper.plusMonths(DateTimeHelper.of(dateTime=f'{dateNow.split(c.DASH)[0]}{c.DASH}{dateNow.split(c.DASH)[1]}{c.DASH}{creditCardResponseDto.dueDay:02} {InstallmentConstant.DEFAULT_DUE_TIME}'), months=1)
        purchaseAtAsString = str(purchaseAt)
        return DateTimeHelper.plusMonths(
            DateTimeHelper.plusMonths(DateTimeHelper.of(dateTime=f'{purchaseAtAsString.split(c.DASH)[0]}{c.DASH}{purchaseAtAsString.split(c.DASH)[1]}{c.DASH}{creditCardResponseDto.dueDay:02} {InstallmentConstant.DEFAULT_DUE_TIME}'), months=1),
            months = 1
        )
