from python_helper import ObjectHelper, log
from python_framework import Service, ServiceMethod, Serializer, GlobalException, HttpStatus

from AuthorizedServiceMethodAnnotation import AuthorizedServiceMethod

from domain import AuthorizationOperation
from enumeration.InstallmentStatus import InstallmentStatus
from dto import CreditDto
from model import Credit


@Service()
class CreditService:

    @ServiceMethod(requestClass=[[str]])
    def findAllForCreditCardCreation(self, keyList):
        if 0 == len(keyList):
            raise Exception(f'Credit key list cannot be empty')
        dtoList = self.findAllByKeyIn(keyList)
        if not len(keyList) == len(dtoList) :
            raise Exception(f'Missing Credi: requested: {keyList}, found: {[dto.key for dto in dtoList]}')
        return dtoList


    @ServiceMethod(requestClass=[[str]])
    def findAllByKeyIn(self, keyList):
        return self.findAllByQuery(
            CreditDto.CreditQueryAllDto(
                keyList = keyList
            )
        )


    @ServiceMethod(requestClass=[CreditDto.CreditQueryAllDto])
    def findAllByQuery(self, queryDto):
        return self.mapper.credit.fromModelListToResponseDtoList(self.findAllModelByQuery(queryDto))


    @AuthorizedServiceMethod(requestClass=[str], operations=[AuthorizationOperation.GET])
    def findByKey(self, key, authorizedRequest):
        return self.mapper.credit.fromModelToResponseDto(self.repository.credit.findByKey(key))


    @AuthorizedServiceMethod(requestClass=[CreditDto.CreditQueryAllDto], operations=[AuthorizationOperation.GET])
    def findAllModelByQuery(self, queryDto, authorizedRequest):
        if ObjectHelper.isEmpty(queryDto.keyList):
            for resourceKey in authorizedRequest.resourceKeys:
                if resourceKey not in queryDto.keyList:
                    queryDto.keyList.append(resourceKey)
        query = Serializer.getObjectAsDictionary(queryDto)
        return self.repository.credit.findAllByQuery(query)


    @AuthorizedServiceMethod(requestClass=[[CreditDto.CreditRequestDto]], operations=[AuthorizationOperation.POST])
    def createAll(self, dtoList, authorizedRequest):
        return [
            self.create(dto)
            for dto in dtoList
        ]


    @AuthorizedServiceMethod(requestClass=[CreditDto.CreditRequestDto], operations=[AuthorizationOperation.POST])
    def create(self, dto, authorizedRequest):
        model = self.mapper.credit.fromRequestDtoToModel(dto)
        self.saveAllModel([model])
        return self.mapper.credit.fromModelToResponseDto(model)


    @AuthorizedServiceMethod(requestClass=[str, str], operations=[AuthorizationOperation.PATCH])
    def proccessInstalment(self, key, installmentKey, authorizedRequest):
        log.debug(self.proccessInstalment, f'Proccesing {installmentKey} installment')
        model = self.findAllModelByQuery(
            CreditDto.CreditQueryAllDto(
                keyList = [key]
            )
        )[0]
        installmentResponseDto = self.service.installment.findByKey(installmentKey)
        self.validator.credit.validateTransaction(model, (float(model.value) + installmentResponseDto.value))
        log.debug(self.proccessInstalment, f'Updating {key} credit value')
        model.value = float(model.value) + installmentResponseDto.value
        self.saveModel(model)
        log.debug(self.proccessInstalment, f'Credit {key} value updated')
        log.debug(self.proccessInstalment, f'Installment {installmentKey} proccessed')
        return self.mapper.credit.fromModelToResponseDto(model)


    @ServiceMethod(requestClass=[Credit.Credit])
    def saveModel(self, model):
        return self.repository.credit.saveAll([model])


    @ServiceMethod(requestClass=[[Credit.Credit]])
    def saveAllModel(self, modelList):
        return self.repository.credit.saveAll(modelList)


    @AuthorizedServiceMethod(requestClass=[str], operations=[AuthorizationOperation.DELETE])
    def deleteByKey(self, key, authorizedRequest):
        self.repository.credit.deleteByKey(key)
