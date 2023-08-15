import datetime
from python_helper import Constant as c
from python_helper import DateTimeHelper
from python_framework import Helper, HelperMethod

from constant import InstallmentConstant
from helper.static import MathStaticHelper, IntervalStaticHelper
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
        # purchaseAtAsStringList = self.getDateTimeAsStringList(purchaseAt)
        # return DateTimeHelper.plusMonths(
        #     DateTimeHelper.of(dateTime=f'{purchaseAtAsStringList[0]}{c.DASH}{purchaseAtAsStringList[1]}{c.DASH}{creditCardResponseDto.closingDay:02} {InstallmentConstant.DEFAULT_CLOSING_TIME}'),
        #     months = self.getPlusMonsthsByClosingDayComparrison(purchaseAtAsStringList, creditCardResponseDto)
        # )
        return IntervalStaticHelper.getCurrentClosingDateTime(purchaseAt, creditCardResponseDto.closingDay, creditCardResponseDto.closingDay)


    @HelperMethod(requestClass=[datetime.datetime, CreditCardDto.CreditCardResponseDto])
    def getNextClosingDateTime(self, purchaseAt, creditCardResponseDto):
        # return DateTimeHelper.plusMonths(
        #     self.getCurrentClosingDateTime(purchaseAt, creditCardResponseDto),
        #     months = 1
        # )
        return IntervalStaticHelper.getNextClosingDateTime(purchaseAt, creditCardResponseDto.closingDay, creditCardResponseDto.closingDay)


    @HelperMethod(requestClass=[datetime.datetime, CreditCardDto.CreditCardResponseDto])
    def getCurrentDueDateTime(self, purchaseAt, creditCardResponseDto):
        # purchaseAtAsStringList = self.getDateTimeAsStringList(purchaseAt)
        # return DateTimeHelper.plusMonths(
        #     DateTimeHelper.of(dateTime=f'{purchaseAtAsStringList[0]}{c.DASH}{purchaseAtAsStringList[1]}{c.DASH}{creditCardResponseDto.dueDay:02} {InstallmentConstant.DEFAULT_DUE_TIME}'),
        #     months = self.getPlusMonsthsByClosingDayComparrison(purchaseAtAsStringList, creditCardResponseDto)
        # )
        return IntervalStaticHelper.getCurrentDueDateTime(purchaseAt, creditCardResponseDto.dueDay, creditCardResponseDto.closingDay)


    @HelperMethod(requestClass=[datetime.datetime, CreditCardDto.CreditCardResponseDto])
    def getNextDueDateTime(self, purchaseAt, creditCardResponseDto):
        # return DateTimeHelper.plusMonths(
        #     self.getCurrentDueDateTime(purchaseAt, creditCardResponseDto),
        #     months = 1
        # )
        return IntervalStaticHelper.getNextDueDateTime(purchaseAt, creditCardResponseDto.dueDay, creditCardResponseDto.closingDay)
