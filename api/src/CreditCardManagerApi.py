from python_framework import ResourceManager

from model import ModelAssociation


app = ResourceManager.initialize(__name__, ModelAssociation.MODEL, managerList=[])


import io, csv, requests, zipfile
from flask import make_response, request, send_file

from python_helper import ObjectHelper, log, DateTimeHelper
from python_helper import Constant as c
from python_framework import Serializer, OpenApiManager, StaticConverter

from config import SimpleAccountsConfig
from dto import CreditCardDto, InvoiceDto, InstallmentDto


def getApiUrl(apiInstance):
    globalsInstance = apiInstance.globals
    sheme = StaticConverter.getValueOrDefault(StaticConverter.getValueOrDefault(globalsInstance.getSetting(f'{OpenApiManager.KW_OPEN_API}.{OpenApiManager.KW_SCHEMES}'), [apiInstance.scheme]), [apiInstance.scheme])[0]
    host = StaticConverter.getValueOrDefault(globalsInstance.getSetting(f'{OpenApiManager.KW_OPEN_API}.{OpenApiManager.KW_HOST}'), apiInstance.host).replace(OpenApiManager.ZERO_DOT_ZERO_DOT_ZERO_DOT_ZERO_HOST, OpenApiManager.LOCALHOST_HOST)
    colonPortIfAny = StaticConverter.getValueOrDefault(f"{c.COLON}{globalsInstance.getSetting(f'{OpenApiManager.KW_OPEN_API}.{OpenApiManager.KW_PORT}')}", c.BLANK).replace(f'{c.COLON}None', c.BLANK)
    exposedHostApiUrl = f'{sheme}{OpenApiManager.SCHEME_HOST_SEPARATOR}{host}{colonPortIfAny}{apiInstance.baseUrl}'
    return f'{exposedHostApiUrl}'.replace(OpenApiManager.PORT_80_IN_URL, OpenApiManager.PORT_80_EXCLUDED_FROM_URL).replace(OpenApiManager.ZERO_DOT_ZERO_DOT_ZERO_DOT_ZERO_HOST, OpenApiManager.LOCALHOST_HOST)


OpenApiManager.getApiUrl = getApiUrl


API_URL = OpenApiManager.getApiUrl(app.api)
log.debugIt(API_URL)



@app.route(f'{app.api.baseUrl}/credit-card/download', methods=['GET'])
def downloadCreditCards():
    output = make_response(toCreditCardsCsvContent(getCreditCards()))
    output.headers['Content-Disposition'] = f'''attachment; filename={parseFileName('credit-card.csv')}'''
    output.headers['Content-type'] = 'text/csv'
    return output


def getCreditCards() -> [CreditCardDto.CreditCardResponseDto]:
    return app.api.resource.repository.creditCard.findAllByQuery(
        Serializer.getObjectAsDictionary(CreditCardDto.CreditCardQueryDto())
    )


def toCreditCardsCsvContent(creditCardResponseDtoList):
    print(creditCardResponseDtoList)
    return toCsv([
        [
            f'{creditCardResponseDto.label}', 
            toValue(creditCardResponseDto.value)
        ]
        for creditCardResponseDto in creditCardResponseDtoList
    ])


@app.route(f'{app.api.baseUrl}/invoice/download/<string:date>', methods=['GET'])
def downloadInvoices(date):
    output = make_response(toInvoicesCsvContent(getInvoices(
        DateTimeHelper.of(date=DateTimeHelper.dateOf(DateTimeHelper.of(date=date)))
    )))
    output.headers['Content-Disposition'] = f'''attachment; filename={parseFileName(f'{date}-invoices.csv')}'''
    output.headers['Content-type'] = 'text/csv'
    return output


def getInvoices(date, userKey=None) -> [InvoiceDto.InvoiceResponseDto]:
    return ObjectHelper.flatMap([
        getInvoicesByAuthorization(authenticatedUser.authentication, date)
        for authenticatedUser in SimpleAccountsConfig.AUTHENTICATED_USERS
        if (
            ObjectHelper.isEmpty(userKey) or
            ObjectHelper.equals(authenticatedUser.userKey, userKey)
        )
    ])


def getInvoicesByAuthorization(authentication, date) -> [InvoiceDto.InvoiceResponseDto]:
    try:
        return Serializer.convertFromJsonToObject(
            requests.get(
                f'{API_URL}/invoice/all?date={date}',
                headers={
                    'Authorization': f'Bearer {authentication}'
                }
            ).json(),
            [[InvoiceDto.InvoiceResponseDto]]
        )
    except Exception as exception:
        log.error(getInvoicesByAuthorization, 'Error', exception=exception)
        return []


def toInvoicesCsvContent(invoiceResponseDtoList: [InvoiceDto.InvoiceResponseDto]):
    return toCsv([
        [
            f'{invoiceResponseDto.creditCard.label}', 
            toValue(invoiceResponseDto.value)
        ]
        for invoiceResponseDto in invoiceResponseDtoList
    ])


@app.route(f'{app.api.baseUrl}/invoice/user/download/<string:date>/<string:userKey>', methods=['GET'])
def downloadUserInvoices(date, userKey):
    output = make_response(toInvoicesCsvContent(getInvoices(
        DateTimeHelper.of(date=DateTimeHelper.dateOf(DateTimeHelper.of(date=date))),
        userKey = userKey
    )))
    output.headers['Content-Disposition'] = f'''attachment; filename={parseFileName(f'{userKey}-{date}-invoices.csv')}'''
    output.headers['Content-type'] = 'text/csv'
    return output


@app.route(f'{app.api.baseUrl}/invoice/user/detailed/download/<string:date>/<string:userKey>', methods=['GET'])
def downloadUserDetailedInvoices(date, userKey):
    return send_file(
        toUserDetailedInvoicesZipContentStream(date, userKey),
        as_attachment = True,
        download_name = parseFileName(f'{userKey}-{date}-detailed-invoices.zip')
    )


def toInvoicesCsvContentDictionary(date, userKey):
    return {
        invoiceResponseDto.creditCard.label: toCsv([
            [
                toUserFriendlyDate(installmentResponseDto.installmentAt), 
                f'{installmentResponseDto.label}', 
                f'{invoiceResponseDto.creditCard.label}', 
                toUserrFriendlyValueDate(installmentResponseDto.value), 
                toUserFriendlyInstalmmentOrder(installmentResponseDto)
            ]
            for installmentResponseDto in invoiceResponseDto.installmentList
        ])
        for invoiceResponseDto in getInvoices(
            DateTimeHelper.of(date=DateTimeHelper.dateOf(DateTimeHelper.of(date=date))),
            userKey = userKey
        )
    }


def toUserDetailedInvoicesZipContentStream(date, userKey):
    stream = io.BytesIO()
    with zipfile.ZipFile(stream, 'w') as zf:
        for creditCardLabel, content in toInvoicesCsvContentDictionary(date, userKey).items():
            zf.writestr(parseFileName(f'{userKey}-{creditCardLabel}-{date}-invoices.csv'), content)
    stream.seek(0)
    return stream


def toCsv(contentRows):
    osBuffer = io.StringIO()
    csv.writer(osBuffer, delimiter=c.SEMI_COLON).writerows(contentRows)
    return osBuffer.getvalue()


def parseFileName(originalFileName):
    return originalFileName.replace(c.SPACE, c.BLANK)


def toUserFriendlyDate(date):
    userFriendlyDateTimeSplited = f'{date}'.split()
    userFriendlyDate = userFriendlyDateTimeSplited[0].split(c.DASH)
    return f'''{userFriendlyDate[-1]}/{userFriendlyDate[1]}/{userFriendlyDate[0]} {userFriendlyDateTimeSplited[-1] if 2 == len(userFriendlyDateTimeSplited) else '10:10:10.000'}'''


def toValue(value):
    return float(value) if ObjectHelper.equals(0.0, value) else f'{-1 * float(value)}'


def toUserrFriendlyValueDate(value):
    return f'R$ {toValue(value)}'.replace(c.COMA, c.BLANK).replace(c.DOT, c.COMA)


def toUserFriendlyInstalmmentOrder(installmentResponseDto: InstallmentDto.InstallmentResponseDto):
    return c.DASH if ObjectHelper.equals(1, installmentResponseDto.installments) else f'{installmentResponseDto.order + 1} de {int(installmentResponseDto.installments)}'

