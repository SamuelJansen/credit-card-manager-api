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
        purchaseAtAsStringList = self.getDateTimeAsStringList(purchaseAt)
        return DateTimeHelper.plusMonths(
            DateTimeHelper.of(dateTime=f'{purchaseAtAsStringList[0]}{c.DASH}{purchaseAtAsStringList[1]}{c.DASH}{creditCardResponseDto.closingDay:02} {InstallmentConstant.DEFAULT_CLOSING_TIME}'),
            months = self.getPlusMonsthsByClosingDayComparrison(purchaseAtAsStringList, creditCardResponseDto)
        )

    @HelperMethod(requestClass=[datetime.datetime, CreditCardDto.CreditCardResponseDto])
    def getNextClosingDateTime(self, purchaseAt, creditCardResponseDto):
        return DateTimeHelper.plusMonths(
            self.getCurrentClosingDateTime(purchaseAt, creditCardResponseDto),
            months = 1
        )

    @HelperMethod(requestClass=[datetime.datetime, CreditCardDto.CreditCardResponseDto])
    def getCurrentDueDateTime(self, purchaseAt, creditCardResponseDto):
        purchaseAtAsStringList = self.getDateTimeAsStringList(purchaseAt)
        return DateTimeHelper.plusMonths(
            DateTimeHelper.of(dateTime=f'{purchaseAtAsStringList[0]}{c.DASH}{purchaseAtAsStringList[1]}{c.DASH}{creditCardResponseDto.dueDay:02} {InstallmentConstant.DEFAULT_DUE_TIME}'),
            months = self.getPlusMonsthsByClosingDayComparrison(purchaseAtAsStringList, creditCardResponseDto)
        )

    @HelperMethod(requestClass=[datetime.datetime, CreditCardDto.CreditCardResponseDto])
    def getNextDueDateTime(self, purchaseAt, creditCardResponseDto):
        return DateTimeHelper.plusMonths(
            self.getCurrentDueDateTime(purchaseAt, creditCardResponseDto),
            months = 1
        )

    @HelperMethod(requestClass=[datetime.datetime])
    def getDateTimeAsStringList(self, purchaseAt):
        return str(str(purchaseAt).split()[0]).split(c.DASH)

    @HelperMethod(requestClass=[[str], CreditCardDto.CreditCardResponseDto])
    def getPlusMonsthsByClosingDayComparrison(self, purchaseAtAsStringList, creditCardResponseDto):
        return 0 if creditCardResponseDto.closingDay > int(purchaseAtAsStringList[-1]) else 1
