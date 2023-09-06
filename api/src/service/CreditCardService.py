from python_helper import ObjectHelper, log, StringHelper
from python_framework import Service, ServiceMethod, Serializer, GlobalException, HttpStatus

from annotation.AuthorizedServiceAnnotation import AuthorizedServiceMethod

from domain import AuthorizationOperation
from enumeration.InstallmentStatus import InstallmentStatus
from constant import InstallmentConstant
from dto import CreditCardDto, InstallmentDto, CreditDto, PurchaseDto
from model import CreditCard


@Service()
class CreditCardService:

    @AuthorizedServiceMethod(requestClass=[[CreditCardDto.CreditCardRequestDto]], operations=[AuthorizationOperation.POST])
    def createAll(self, dtoList, authorizedRequest):
        self.validator.creditCard.validateCreateAll(dtoList, authorizedRequest.resourceKeys)
        newCreditResponseDtoList = []
        for dto in [
            dto 
            for dto in dtoList 
            if ObjectHelper.isNoneOrBlank(dto.creditKey)
        ]:
            newCreditResponseDto = self.service.credit.createAll([
                CreditDto.CreditRequestDto(
                    limit = dto.customLimit,
                    customLimit = dto.customLimit,
                    value = 0
                )
            ])[0]
            dto.creditKey = newCreditResponseDto.key
            newCreditResponseDtoList.append(newCreditResponseDto)
        existingCreditResponseDtoList = self.service.credit.findAllForCreditCardCreation(list(set([
                dto.creditKey
                for dto in dtoList 
                if ObjectHelper.isNeitherNoneNorBlank(dto.creditKey)
            ]))) 
        modelList = self.mapper.creditCard.fromRequestDtoListToModelList(dtoList)
        self.saveAllModel(modelList)
        return self.mapper.creditCard.toResponseDtoList(modelList, [*newCreditResponseDtoList, *existingCreditResponseDtoList])
    

    @AuthorizedServiceMethod(requestClass=[[CreditCardDto.CreditCardRequestDto]], operations=[AuthorizationOperation.DELETE])
    def revertAll(self, dtoList, authorizedRequest):
        purchaseResponseDtoList = self.service.purchase.findAllByQuery(
            PurchaseDto.PurchaseQueryAllDto(
                creditCardKeyList=[dto.key for dto in dtoList]
            )
        )
        if ObjectHelper.isNotEmpty(purchaseResponseDtoList):
            self.service.purchase.revertAll(
                self.converter.purchase.fromResponseDtoListToRequestDtoList(purchaseResponseDtoList)
            )
        self.deleteAllByKeyIn([dto.key for dto in dtoList])
        return []



    @AuthorizedServiceMethod(requestClass=[str, [InstallmentDto.InstallmentResponseDto]], operations=[AuthorizationOperation.PATCH])
    def proccessAllInstalments(self, key, installmentRequestDtoList, authorizedRequest):
        log.status(self.proccessAllInstalments, f'Processing {len(installmentRequestDtoList)} {key} credit card installments')
        if 0 == len(installmentRequestDtoList):
            raise GlobalException(message=f'Installment already processed', status=HttpStatus.BAD_REQUEST)
        model = self.findAllModelByQuery(
            CreditCardDto.CreditCardQueryAllDto(
                keyList = [key]
            )
        )[0]
        installmentResponseDtoList = []
        for installmentRequestDto in ObjectHelper.sortIt(installmentRequestDtoList, byAttribute=InstallmentConstant.SORTTING_ATTRIBUTE):
            try:
                creditResponseDto = self.service.credit.proccessInstalment(model.creditKey, installmentRequestDto.key)
                model.value = float(model.value) + installmentRequestDto.value
                self.saveModel(model)
                installmentResponseDtoList.append(installmentRequestDto)
            except Exception as exception:
                log.error(self.proccessAllInstalments, f'Not possible to proccess installment {installmentRequestDto.key} of {key} credit card', exception=exception)
                installmentResponseDtoList += self.service.installment.updateAllStatusByKeyList([installmentRequestDto.key], InstallmentStatus.ERROR)
        log.status(self.proccessAllInstalments, f'{len(installmentResponseDtoList)} {key} credit card installments processed')
        return installmentResponseDtoList
    

    @AuthorizedServiceMethod(requestClass=[str, [InstallmentDto.InstallmentResponseDto]], operations=[AuthorizationOperation.PUT])
    def revertAllInstalments(self, key, installmentRequestDtoList, authorizedRequest):
        log.status(self.revertAllInstalments, f'Reverting {len(installmentRequestDtoList)} {key} credit card installments')
        if 0 == len(installmentRequestDtoList):
            raise GlobalException(message=f'Installment already reverted', status=HttpStatus.BAD_REQUEST)
        model = self.findAllModelByQuery(
            CreditCardDto.CreditCardQueryAllDto(
                keyList = [key]
            )
        )[0]
        installmentResponseDtoList = []
        for installmentRequestDto in installmentRequestDtoList:
            try:
                creditResponseDto = self.service.credit.revertInstalment(model.creditKey, installmentRequestDto.key)
                model.value = float(model.value) - installmentRequestDto.value
                self.saveModel(model)
                installmentResponseDtoList.append(installmentRequestDto)
            except Exception as exception:
                log.error(self.revertAllInstalments, f'Not possible to revert installment {installmentRequestDto.key} of {key} credit card', exception=exception)
                installmentResponseDtoList += self.service.installment.updateAllStatusByKeyList([installmentRequestDto.key], InstallmentStatus.ERROR)
        log.status(self.revertAllInstalments, f'{len(installmentResponseDtoList)} {key} credit card installments reverted')
        return installmentResponseDtoList
    
    
    @ServiceMethod()
    def findAll(self):
        return self.findAllByKeyIn([])


    @ServiceMethod(requestClass=[[str]])
    def findAllByKeyIn(self, keyList):
        return self.findAllByQuery(
            CreditCardDto.CreditCardQueryAllDto(
                keyList = keyList
            )
        )

    @ServiceMethod(requestClass=[CreditCardDto.CreditCardQueryAllDto])
    def findAllByQuery(self, queryDto):
        modelList = self.findAllModelByQuery(queryDto)
        creditResponseDtoList = self.service.credit.findAllByKeyIn(
            list(set([
                model.creditKey
                for model in modelList
                if ObjectHelper.isNotNone(model.creditKey)
            ]))
        )
        return self.mapper.creditCard.toResponseDtoList(modelList, creditResponseDtoList)


    @AuthorizedServiceMethod(requestClass=[CreditCardDto.CreditCardQueryAllDto], operations=[AuthorizationOperation.GET])
    def findAllModelByQuery(self, queryDto, authorizedRequest):
        if ObjectHelper.isEmpty(queryDto.keyList):
            for resourceKey in authorizedRequest.resourceKeys:
                if resourceKey not in queryDto.keyList:
                    queryDto.keyList.append(resourceKey)
        query = Serializer.getObjectAsDictionary(queryDto)
        return self.repository.creditCard.findAllByQuery(query)


    @AuthorizedServiceMethod(requestClass=[str], operations=[AuthorizationOperation.GET])
    def findByKey(self, key, authorizedRequest):
        model = self.findModelByKey(key)
        creditResponseDto = self.service.credit.findByKey(model.creditKey)
        return self.mapper.creditCard.toResponseDto(model, creditResponseDto)


    @ServiceMethod(requestClass=[str])
    def findModelByKey(self, key):
        return self.repository.creditCard.findByKey(key)


    @ServiceMethod(requestClass=[int])
    def findModelById(self, id):
        return self.repository.creditCard.findById(id)


    @ServiceMethod()
    def findAllModel(self):
        return self.repository.creditCard.findAll()


    @ServiceMethod(requestClass=[[str], [str]])
    def existsByKeyInAndLabelIn(self, keyList, labelList):
        return self.existsByQueryAll(
            CreditCardDto.CreditCardQueryAllDto(
                keyList = keyList,
                labelList = labelList
            )
        )


    @ServiceMethod(requestClass=[str])
    def existsByKey(self, key):
        return self.repository.creditCard.existsByKey(key)


    @ServiceMethod(requestClass=[CreditCardDto.CreditCardQueryDto])
    def existsByQuery(self, queryDto):
        query = Serializer.getObjectAsDictionary(queryDto)
        return self.repository.creditCard.existsByQuery(query)


    @ServiceMethod(requestClass=[CreditCardDto.CreditCardQueryAllDto])
    def existsByQueryAll(self, queryDto):
        query = Serializer.getObjectAsDictionary(queryDto)
        return self.repository.creditCard.existsByQuery(query)


    @ServiceMethod(requestClass=[CreditCard.CreditCard])
    def saveModel(self, model):
        return self.repository.creditCard.save(model)


    @ServiceMethod(requestClass=[[CreditCard.CreditCard]])
    def saveAllModel(self, modelList):
        return self.repository.creditCard.saveAll(modelList)


    @AuthorizedServiceMethod(requestClass=[str], operations=[AuthorizationOperation.DELETE])
    def deleteByKey(self, key, authorizedRequest):
        self.validator.creditCard.validateDelete(key)
        log.info(self.deleteByKey, f'Deleting credit card: {key}')
        self.repository.creditCard.deleteByKey(key)


    @AuthorizedServiceMethod(requestClass=[[str]], operations=[AuthorizationOperation.DELETE])
    def deleteAllByKeyIn(self, keyList, authorizedRequest):
        self.validator.creditCard.validateDeleteAll(keyList)
        log.info(self.deleteAllByKeyIn, f'Deleting credit cards: {keyList}')
        self.repository.creditCard.deleteAllByKeyIn(keyList)
