import datetime
from python_helper import Constant as c
from python_helper import DateTimeHelper
from python_framework import Helper, HelperMethod

from constant import IntervalConstant
from helper.static import MathStaticHelper, IntervalStaticHelper
from dto import CreditCardDto, PurchaseDto


FIRST_MONTH_DAY = 1


@Helper()
class InvoiceHelper:

    @HelperMethod(requestClass=[datetime.datetime, CreditCardDto.CreditCardResponseDto])
    def getCurrentClosingDateTime(self, invoiceDateTime, creditCardResponseDto):
        # invoiceDateTimeAsStringList = self.getDateTimeAsStringList(invoiceDateTime)
        # return DateTimeHelper.plusMonths(
        #     DateTimeHelper.of(
        #         dateTime = f'''{invoiceDateTimeAsStringList[0]}{
        #             c.DASH
        #         }{invoiceDateTimeAsStringList[1]}{
        #             c.DASH
        #         }{creditCardResponseDto.closingDay:02}{
        #             c.SPACE
        #         }{IntervalConstant.DEFAULT_CLOSING_TIME}''' if creditCardResponseDto.closingDay > 0 else DateTimeHelper.minusDays(
        #             f'''{invoiceDateTimeAsStringList[0]}{
        #                 c.DASH
        #             }{invoiceDateTimeAsStringList[1]}{
        #                 c.DASH
        #             }{FIRST_MONTH_DAY:02}{
        #                 c.SPACE
        #             }{IntervalConstant.DEFAULT_CLOSING_TIME}''',
        #             days = 1
        #         )
        #     ),
        #     months = self.getPlusMonsthsByDueDayComparrison(invoiceDateTimeAsStringList, creditCardResponseDto.dueDay)
        # )
        return IntervalStaticHelper.getCurrentClosingDateTime(invoiceDateTime, creditCardResponseDto.closingDay, creditCardResponseDto.dueDay)


    @HelperMethod(requestClass=[datetime.datetime, CreditCardDto.CreditCardResponseDto])
    def getNextClosingDateTime(self, invoiceDateTime, creditCardResponseDto):
        # return DateTimeHelper.plusMonths(
        #     self.getCurrentClosingDateTime(invoiceDateTime, creditCardResponseDto),
        #     months = 1
        # )
        return IntervalStaticHelper.getNextClosingDateTime(invoiceDateTime, creditCardResponseDto.closingDay, creditCardResponseDto.dueDay)


    @HelperMethod(requestClass=[datetime.datetime, CreditCardDto.CreditCardResponseDto])
    def getCurrentDueDateTime(self, invoiceDateTime, creditCardResponseDto):
        # invoiceDateTimeAsStringList = self.getDateTimeAsStringList(invoiceDateTime)
        # return DateTimeHelper.plusMonths(
        #     DateTimeHelper.of(
        #         dateTime = f'''{invoiceDateTimeAsStringList[0]}{
        #             c.DASH
        #         }{invoiceDateTimeAsStringList[1]}{
        #             c.DASH
        #         }{creditCardResponseDto.dueDay:02}{
        #             c.SPACE
        #         }{IntervalConstant.DEFAULT_DUE_TIME}''' if creditCardResponseDto.dueDay > 0 else DateTimeHelper.minusDays(
        #             f'''{invoiceDateTimeAsStringList[0]}{
        #                 c.DASH
        #             }{invoiceDateTimeAsStringList[1]}{
        #                 c.DASH
        #             }{FIRST_MONTH_DAY:02}{
        #                 c.SPACE
        #             }{IntervalConstant.DEFAULT_DUE_TIME}''',
        #             days = 1
        #         )
        #     ),
        #     months = self.getPlusMonsthsByDueDayComparrison(invoiceDateTimeAsStringList, creditCardResponseDto.dueDay)
        # )
        return IntervalStaticHelper.getCurrentDueDateTime(invoiceDateTime, creditCardResponseDto.dueDay, creditCardResponseDto.dueDay)
    

    @HelperMethod(requestClass=[datetime.datetime, CreditCardDto.CreditCardResponseDto])
    def getNextDueDateTime(self, invoiceDateTime, creditCardResponseDto):
        # return DateTimeHelper.plusMonths(
        #     self.getCurrentDueDateTime(invoiceDateTime, creditCardResponseDto),
        #     months = 1
        # )
        return IntervalStaticHelper.getNextDueDateTime(invoiceDateTime, creditCardResponseDto.dueDay, creditCardResponseDto.dueDay)
