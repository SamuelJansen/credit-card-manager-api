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
    def getCurrentClosingDateTime(self, invoiceDateTime, creditCardResponseDto):
        invoiceDateTimeAsStringList = self.getDateTimeAsStringList(invoiceDateTime)
        return DateTimeHelper.plusMonths(
            DateTimeHelper.of(dateTime=f'{invoiceDateTimeAsStringList[0]}{c.DASH}{invoiceDateTimeAsStringList[1]}{c.DASH}{creditCardResponseDto.closingDay:02} {InstallmentConstant.DEFAULT_CLOSING_TIME}'),
            months = self.getPlusMonsthsByDueDayComparrison(invoiceDateTimeAsStringList, creditCardResponseDto)
        )

    @HelperMethod(requestClass=[datetime.datetime, CreditCardDto.CreditCardResponseDto])
    def getNextClosingDateTime(self, invoiceDateTime, creditCardResponseDto):
        return DateTimeHelper.plusMonths(
            self.getCurrentClosingDateTime(invoiceDateTime, creditCardResponseDto),
            months = 1
        )

    @HelperMethod(requestClass=[datetime.datetime, CreditCardDto.CreditCardResponseDto])
    def getCurrentDueDateTime(self, invoiceDateTime, creditCardResponseDto):
        invoiceDateTimeAsStringList = self.getDateTimeAsStringList(invoiceDateTime)
        return DateTimeHelper.plusMonths(
            DateTimeHelper.of(dateTime=f'{invoiceDateTimeAsStringList[0]}{c.DASH}{invoiceDateTimeAsStringList[1]}{c.DASH}{creditCardResponseDto.dueDay:02} {InstallmentConstant.DEFAULT_DUE_TIME}'),
            months = self.getPlusMonsthsByDueDayComparrison(invoiceDateTimeAsStringList, creditCardResponseDto)
        )

    @HelperMethod(requestClass=[datetime.datetime, CreditCardDto.CreditCardResponseDto])
    def getNextDueDateTime(self, invoiceDateTime, creditCardResponseDto):
        return DateTimeHelper.plusMonths(
            self.getCurrentDueDateTime(invoiceDateTime, creditCardResponseDto),
            months = 1
        )

    @HelperMethod(requestClass=[datetime.datetime])
    def getDateTimeAsStringList(self, invoiceDateTime):
        return str(str(invoiceDateTime).split()[0]).split(c.DASH)

    @HelperMethod(requestClass=[[str], CreditCardDto.CreditCardResponseDto])
    def getPlusMonsthsByDueDayComparrison(self, invoiceDateTimeAsStringList, creditCardResponseDto):
        return 0 if creditCardResponseDto.dueDay > int(invoiceDateTimeAsStringList[-1]) else 1
