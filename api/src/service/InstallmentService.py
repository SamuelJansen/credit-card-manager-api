from python_helper import ObjectHelper, log
from python_framework import Service, ServiceMethod, Serializer, StaticConverter, EnumItem, GlobalException, HttpStatus

from annotation.AuthorizedServiceAnnotation import AuthorizedServiceMethod

from constant import InstallmentConstant
from domain import AuthorizationOperation
from enumeration.InstallmentStatus import InstallmentStatus
from dto import InstallmentDto
from model import Installment


@Service()
class InstallmentService:

    @ServiceMethod(requestClass=[[str]])
    def findAllByKeyIn(self, keyList):
        return self.findAllByQuery(
            InstallmentDto.InstallmentQueryAllDto(
                keyList = keyList
            )
        )


    @ServiceMethod(requestClass=[[str]])
    def findAllByPurchaseKeyIn(self, purchaseKeyList):
        modelList = self.findAllModelByQuery(
            InstallmentDto.InstallmentQueryAllDto(
                purchaseKeyList = purchaseKeyList
            )
        )
        return self.mapper.installment.fromModelListToResponseDtoList(modelList)


    @ServiceMethod(requestClass=[InstallmentDto.InstallmentQueryAllDto])
    def findAllByQuery(self, queryDto):
        modelList = self.findAllModelByQuery(queryDto)
        purchaseResponseDtoList = self.service.purchase.findAllByKeyIn([
            model.purchaseKey
            for model in modelList
        ])
        return self.mapper.installment.toResponseDtoList(modelList, purchaseResponseDtoList)


    @ServiceMethod(requestClass=[InstallmentDto.InstallmentQueryAllDto])
    def findAllProccessableByQuery(self, queryDto):
        self.converter.installment.overrideProcessableQueryDto(queryDto)
        modelList = self.findAllModelByQuery(queryDto)
        if 0 == len(modelList):
            raise GlobalException(message=f'Installments {queryDto.keyList} already processed', status=HttpStatus.BAD_REQUEST)
        purchaseResponseDtoList = self.service.purchase.findAllByKeyIn([
            model.purchaseKey
            for model in modelList
        ])
        return self.mapper.installment.toResponseDtoList(modelList, purchaseResponseDtoList)


    @ServiceMethod(requestClass=[InstallmentDto.InstallmentQueryAllDto])
    def findAllRevertableByQuery(self, queryDto):
        self.converter.installment.overrideRevertableQueryDto(queryDto)
        modelList = self.findAllModelByQuery(queryDto)
        if 0 == len(modelList):
            raise GlobalException(message=f'Installments {queryDto.keyList} already reverted', status=HttpStatus.BAD_REQUEST)
        purchaseResponseDtoList = self.service.purchase.findAllByKeyIn([
            model.purchaseKey
            for model in modelList
        ])
        return self.mapper.installment.toResponseDtoList(modelList, purchaseResponseDtoList)


    @AuthorizedServiceMethod(requestClass=[InstallmentDto.InstallmentQueryAllDto], operations=[AuthorizationOperation.GET])
    def findAllModelByQuery(self, queryDto, authorizedRequest):
        if ObjectHelper.isEmpty(queryDto.keyList):
            for resourceKey in authorizedRequest.resourceKeys:
                if resourceKey not in queryDto.keyList:
                    queryDto.keyList.append(resourceKey)
        query = Serializer.getObjectAsDictionary(queryDto)
        filteredQuery = {
            k: v
            for k, v in query.items()
            if (
                k not in InstallmentConstant.DATE_TIME_QUERY_KEY_LIST and
                k not in InstallmentConstant.CREDIT_CARD_QUERY_KEY_LIST
            )
        }
        fromDateTime = StaticConverter.getValueOrDefault(query.get(InstallmentConstant.FROM_DATE_TIME_QUERY_KEY), InstallmentConstant.MIN_START_DATE_TIME)
        toDateTime = StaticConverter.getValueOrDefault(query.get(InstallmentConstant.TO_DATE_TIME_QUERY_KEY), InstallmentConstant.MAX_END_DATE_TIME)
        return self.repository.installment.findAllByQueryWithinInstallmentDatesAndCreditCardKeyIn(filteredQuery, fromDateTime, toDateTime, queryDto.creditCardKeyList)


    @AuthorizedServiceMethod(requestClass=[str], operations=[AuthorizationOperation.GET])
    def findByKey(self, key, authorizedRequest):
        return self.mapper.installment.fromModelToResponseDto(self.repository.installment.findByKey(key))


    @AuthorizedServiceMethod(requestClass=[InstallmentDto.InstallmentQueryAllDto], operations=[AuthorizationOperation.PATCH])
    def proccessAll(self, queryDto, authorizedRequest):
        log.status(self.proccessAll, f'Proccesing {len(queryDto.keyList)} installments')
        installmentResponseDtoList = self.findAllProccessableByQuery(queryDto)
        self.updateAllStatusByKeyList(
            [
                installmentResponseDto.key
                for installmentResponseDto in installmentResponseDtoList
            ],
            InstallmentStatus.PROCESSING
        )
        creditCardResponseDtoList = self.service.creditCard.findAllByKeyIn(
            list(set([
                installmentResponseDto.purchase.creditCardKey
                for installmentResponseDto in installmentResponseDtoList
            ]))
        )
        responseDtoList = []
        for creditCardResponseDto in creditCardResponseDtoList:
            toProccessInstallmentKeyList = [
                installmentResponseDto.key
                for installmentResponseDto in installmentResponseDtoList
                if creditCardResponseDto.key == installmentResponseDto.purchase.creditCardKey
            ]
            toProccessInstallmentDtoList = self.service.installment.findAllByKeyIn(toProccessInstallmentKeyList)
            try:
                creditCardInstallmentProcessedList = self.service.creditCard.proccessAllInstalments(
                    creditCardResponseDto.key,
                    toProccessInstallmentDtoList
                )
                processingInstallmentKeyList = [
                    creditCardInstallmentProcessedDto.key
                    for creditCardInstallmentProcessedDto in creditCardInstallmentProcessedList
                    if InstallmentStatus.PROCESSING == creditCardInstallmentProcessedDto.status
                ]
                if 0 < len(processingInstallmentKeyList):
                    responseDtoList += self.updateAllStatusByKeyList(
                        processingInstallmentKeyList,
                        InstallmentStatus.PROCESSED
                    )
                if len(toProccessInstallmentDtoList) > len(processingInstallmentKeyList):
                    responseDtoList += self.updateAllStatusByKeyList(
                        [
                            creditCardInstallmentProcessedDto.key
                            for creditCardInstallmentProcessedDto in creditCardInstallmentProcessedList
                            if creditCardInstallmentProcessedDto.key in toProccessInstallmentKeyList and not InstallmentStatus.PROCESSING == creditCardInstallmentProcessedDto.status
                        ],
                        InstallmentStatus.ERROR
                    )
            except Exception as exception:
                log.error(self.proccessAll, f'Not possible to proccess installments {queryDto.keyList}', exception=exception)
                responseDtoList += self.updateAllStatusByKeyList(
                    [
                        toProccessInstallmentDto.key
                        for toProccessInstallmentDto in toProccessInstallmentDtoList
                    ],
                    InstallmentStatus.ERROR
                )
        log.status(self.proccessAll, f'{len(responseDtoList)} installments processed')
        return responseDtoList


    @AuthorizedServiceMethod(requestClass=[InstallmentDto.InstallmentQueryAllDto], operations=[AuthorizationOperation.DELETE])
    def revertAll(self, queryDto, authorizedRequest):
        log.status(self.revertAll, f'Reverting {len(queryDto.keyList)} installments')
        installmentResponseDtoList = self.findAllRevertableByQuery(queryDto)
        self.updateAllStatusByKeyList(
            [
                installmentResponseDto.key
                for installmentResponseDto in installmentResponseDtoList
            ],
            InstallmentStatus.REVERTING
        )
        creditCardResponseDtoList = self.service.creditCard.findAllByKeyIn(
            list(set([
                installmentResponseDto.purchase.creditCardKey
                for installmentResponseDto in installmentResponseDtoList
            ]))
        )
        responseDtoList = []
        for creditCardResponseDto in creditCardResponseDtoList:
            toRevertInstallmentKeyList = [
                installmentResponseDto.key
                for installmentResponseDto in installmentResponseDtoList
                if creditCardResponseDto.key == installmentResponseDto.purchase.creditCardKey
            ]
            toRevertInstallmentDtoList = self.service.installment.findAllByKeyIn(toRevertInstallmentKeyList)
            try:
                creditCardInstallmentRevertedList = self.service.creditCard.revertAllInstalments(
                    creditCardResponseDto.key,
                    toRevertInstallmentDtoList
                )
                processingInstallmentKeyList = [
                    creditCardInstallmentRevertedDto.key
                    for creditCardInstallmentRevertedDto in creditCardInstallmentRevertedList
                    if InstallmentStatus.REVERTING == creditCardInstallmentRevertedDto.status
                ]
                if 0 < len(processingInstallmentKeyList):
                    responseDtoList += self.updateAllStatusByKeyList(
                        processingInstallmentKeyList,
                        InstallmentStatus.REVERTED
                    )
                if len(toRevertInstallmentDtoList) > len(processingInstallmentKeyList):
                    responseDtoList += self.updateAllStatusByKeyList(
                        [
                            creditCardInstallmentRevertedDto.key
                            for creditCardInstallmentRevertedDto in creditCardInstallmentRevertedList
                            if creditCardInstallmentRevertedDto.key in toRevertInstallmentKeyList and not InstallmentStatus.REVERTING == creditCardInstallmentRevertedDto.status
                        ],
                        InstallmentStatus.ERROR
                    )
            except Exception as exception:
                log.error(self.revertAll, f'Not possible to revert installments {queryDto.keyList}', exception=exception)
                responseDtoList += self.updateAllStatusByKeyList(
                    [
                        toRevertInstallmentDto.key
                        for toRevertInstallmentDto in toRevertInstallmentDtoList
                    ],
                    InstallmentStatus.ERROR
                )
        log.status(self.revertAll, f'{len(responseDtoList)} installments reverted')
        return responseDtoList


    @AuthorizedServiceMethod(requestClass=[[str], EnumItem], operations=[AuthorizationOperation.PATCH])
    def updateAllStatusByKeyList(self, keyList, status, authorizedRequest):
        if 0 == len(keyList):
            raise GlobalException(logMessage='Installment key list cannot be None', status=HttpStatus.INTERNAL_SERVER_ERROR)
        modelList = self.findAllModelByQuery(
            InstallmentDto.InstallmentQueryAllDto(
                keyList = keyList
            )
        )
        self.mapper.installment.overrideModelListStatus(modelList, status)
        self.saveAllModel(modelList)
        purchaseResponseDtoList = self.service.purchase.findAllByKeyIn([
            model.purchaseKey
            for model in modelList
        ])
        return self.mapper.installment.toResponseDtoList(modelList, purchaseResponseDtoList)


    @AuthorizedServiceMethod(requestClass=[[InstallmentDto.InstallmentRequestDto]], operations=[AuthorizationOperation.POST])
    def newCreatedAll(self, dtoList, authorizedRequest):
        modelList = self.mapper.installment.buildNewCreatedModelList(dtoList)
        self.saveAllModel(modelList)
        return self.mapper.installment.fromModelListToResponseDtoList(modelList)


    @AuthorizedServiceMethod(requestClass=[[InstallmentDto.InstallmentRequestDto]], operations=[AuthorizationOperation.POST])
    def createAll(self, dtoList, authorizedRequest):
        return [
            self.create(dto)
            for dto in dtoList
        ]


    @AuthorizedServiceMethod(requestClass=[InstallmentDto.InstallmentRequestDto], operations=[AuthorizationOperation.POST])
    def create(self, dto, authorizedRequest):
        model = self.mapper.installment.fromRequestDtoToModel(dto)
        self.saveAllModel([model])
        return self.mapper.installment.fromModelToResponseDto(model)


    @ServiceMethod(requestClass=[[Installment.Installment]])
    def saveAllModel(self, modelList):
        return self.repository.installment.saveAll(modelList)


    @AuthorizedServiceMethod(requestClass=[str], operations=[AuthorizationOperation.DELETE])
    def deleteByKey(self, key, authorizedRequest):
        log.info(self.deleteByKey, f'Deleting installment: {key}')
        self.repository.installment.deleteByKey(key)


    @AuthorizedServiceMethod(requestClass=[[str]], operations=[AuthorizationOperation.DELETE])
    def deleteAllByKeyIn(self, keyList, authorizedRequest):
        log.info(self.deleteAllByKeyIn, f'Deleting installments: {keyList}')
        self.repository.installment.deleteAllByKeyIn(keyList)
