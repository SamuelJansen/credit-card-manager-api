import datetime
from python_helper import Constant as c
from python_helper import DateTimeHelper
from python_framework import Helper, HelperMethod

from constant import InstallmentConstant
from helper.static import MathStaticHelper
from dto import CreditCardDto, PurchaseDto


@Helper()
class InvoiceHelper:

    @HelperMethod(requestClass=[datetime.datetime, CreditCardDto.CreditCardResponseDto])
    def getCurrentClosingDateTime(self, givenDateTime, creditCardResponseDto):
        givenDateTimeAsStringList = self.getDateTimeAsStringList(givenDateTime)
        return DateTimeHelper.plusMonths(
            DateTimeHelper.of(dateTime=f'{givenDateTimeAsStringList[0]}{c.DASH}{givenDateTimeAsStringList[1]}{c.DASH}{creditCardResponseDto.closingDay:02} {InstallmentConstant.DEFAULT_CLOSING_TIME}'),
            months = self.getPlusMonsthsByDueDayComparrison(givenDateTimeAsStringList, creditCardResponseDto)
        )

    @HelperMethod(requestClass=[datetime.datetime, CreditCardDto.CreditCardResponseDto])
    def getNextClosingDateTime(self, givenDateTime, creditCardResponseDto):
        return DateTimeHelper.plusMonths(
            self.getCurrentClosingDateTime(givenDateTime, creditCardResponseDto),
            months = 1
        )

    @HelperMethod(requestClass=[datetime.datetime, CreditCardDto.CreditCardResponseDto])
    def getCurrentDueDateTime(self, givenDateTime, creditCardResponseDto):
        givenDateTimeAsStringList = self.getDateTimeAsStringList(givenDateTime)
        return DateTimeHelper.plusMonths(
            DateTimeHelper.of(dateTime=f'{givenDateTimeAsStringList[0]}{c.DASH}{givenDateTimeAsStringList[1]}{c.DASH}{creditCardResponseDto.dueDay:02} {InstallmentConstant.DEFAULT_DUE_TIME}'),
            months = self.getPlusMonsthsByDueDayComparrison(givenDateTimeAsStringList, creditCardResponseDto)
        )

    @HelperMethod(requestClass=[datetime.datetime, CreditCardDto.CreditCardResponseDto])
    def getNextDueDateTime(self, givenDateTime, creditCardResponseDto):
        return DateTimeHelper.plusMonths(
            self.getCurrentDueDateTime(givenDateTime, creditCardResponseDto),
            months = 1
        )

    @HelperMethod(requestClass=[datetime.datetime])
    def getDateTimeAsStringList(self, givenDateTime):
        return str(str(givenDateTime).split()[0]).split(c.DASH)

    @HelperMethod(requestClass=[[str], CreditCardDto.CreditCardResponseDto])
    def getPlusMonsthsByDueDayComparrison(self, givenDateTimeAsStringList, creditCardResponseDto):
        return 0 if creditCardResponseDto.dueDay > int(givenDateTimeAsStringList[-1]) else 1
