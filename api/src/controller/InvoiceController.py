from python_framework import Controller, ControllerMethod, HttpStatus

from domain.SecurityContext import SecurityContext
from dto import InvoiceDto

@Controller(
    url = '/invoice',
    tag = 'Invoice',
    description = 'Invoice controller'
    , logRequest = True
    , logResponse = True
)
class InvoiceController:

    @ControllerMethod(url = '/all',
        roleRequired=[SecurityContext.ADMIN, SecurityContext.INVOICE_ADMIN, SecurityContext.USER, SecurityContext.INVOICE_USER],
        requestParamClass=[InvoiceDto.InvoiceQueryDto],
        responseClass=[[InvoiceDto.InvoiceResponseDto]]
    )
    def get(self, params=None):
        return self.service.invoice.findAllByQuery(params), HttpStatus.OK
