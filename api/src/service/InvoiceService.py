from python_framework import Service, ServiceMethod, Serializer, StaticConverter
from python_helper import ObjectHelper, DateTimeHelper, log

from constant import InvoiceConstant
from helper.static import MathStaticHelper, IntervalStaticHelper
from dto import InvoiceDto, InstallmentDto, CreditCardDto


def getDay(givenDate):
    return 


@Service()
class InvoiceService:

    @ServiceMethod(requestClass=[InvoiceDto.InvoiceQueryDto])
    def findAllByQuery(self, queryDto):
        transactionKey = self.service.security.lockTransaction()
        creditCardResponseDtoList = self.service.creditCard.findAllByQuery(CreditCardDto.CreditCardQueryAllDto(keyList=[] if ObjectHelper.isEmpty(queryDto.creditCardKeyList) else queryDto.creditCardKeyList))
        invoiceResponseDtoList = []
        for creditCardResponseDto in creditCardResponseDtoList:
            dueDateTime = self.helper.invoice.getCurrentDueDateTime(DateTimeHelper.of(date=queryDto.date), creditCardResponseDto)
            dueDate = DateTimeHelper.dateOf(dateTime=dueDateTime)
            closingDateTime = self.helper.invoice.getCurrentClosingDateTime(DateTimeHelper.of(date=queryDto.date), creditCardResponseDto)
            closingDate = DateTimeHelper.dateOf(dateTime=closingDateTime)
            fromDateTimeRefference = closingDateTime if queryDto.date > dueDate else IntervalStaticHelper.previousMonth(closingDateTime)
            toDateTimeRefference = IntervalStaticHelper.nextMonth(fromDateTimeRefference)
            installmentResponseDtoList = self.service.installment.findAllByQuery(
                InstallmentDto.InstallmentQueryAllDto(
                    creditCardKeyList = [
                        creditCardResponseDto.key
                    ],
                    fromDateTime = f'{DateTimeHelper.dateOf(dateTime=DateTimeHelper.plusDays(fromDateTimeRefference, days=1))} {DateTimeHelper.DEFAULT_TIME_BEGIN}',
                    toDateTime = f'{DateTimeHelper.dateOf(dateTime=toDateTimeRefference)} {DateTimeHelper.DEFAULT_TIME_END}'
                )
            )
            invoiceResponseDtoList.append(
                InvoiceDto.InvoiceResponseDto(
                    key = creditCardResponseDto.key,
                    value = MathStaticHelper.sumIt(
                        [
                            installmentResponseDto.value
                            for installmentResponseDto in installmentResponseDtoList
                            if (
                                installmentResponseDto.value < 0  and
                                installmentResponseDto.status in InvoiceConstant.INSTALLMENT_COUNTABLE_TYPES
                            )
                        ]
                    ),
                    installmentList = sorted(installmentResponseDtoList, key=lambda x: x.installmentAt, reverse=True),
                    creditCard = creditCardResponseDto,
                    closeAt = closingDate, ###- closeAt
                    dueAt =  dueDate ###- dueAt
                )
            )
        self.service.security.unlockTransaction(transactionKey)
        return invoiceResponseDtoList
