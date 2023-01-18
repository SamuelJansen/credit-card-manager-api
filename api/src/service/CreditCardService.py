from python_helper import ObjectHelper, log
from python_framework import Service, ServiceMethod, Serializer, GlobalException, HttpStatus

from AuthorizedServiceMethodAnnotation import AuthorizedServiceMethod

from domain import AuthorizationOperation
from enumeration.InstallmentStatus import InstallmentStatus
from dto import CreditCardDto, InstallmentDto
from model import CreditCard
from helper.static import MathStaticHelper


@Service()
class CreditCardService:

    @AuthorizedServiceMethod(requestClass=[[CreditCardDto.CreditCardRequestDto]], operations=[AuthorizationOperation.POST])
    def createAll(self, dtoList, authorizedRequest):
        self.validator.creditCard.validateCreateAll(dtoList, authorizedRequest.resourceKeys)
        modelList = self.mapper.creditCard.fromRequestDtoListToModelList(dtoList)
        creditResponseDtoList = self.service.credit.findAllForCreditCardCreation(
            list(set([
                dto.creditKey
                for dto in dtoList
                if ObjectHelper.isNotNone(dto.creditKey)
            ]))
        )
        self.saveAllModel(modelList)
        return self.mapper.creditCard.toResponseDtoList(modelList, creditResponseDtoList)


    @AuthorizedServiceMethod(requestClass=[str, [str]], operations=[AuthorizationOperation.PATCH])
    def proccessAllInstalments(self, key, installmentKeyList, authorizedRequest):
        if 0 == len(installmentKeyList):
            raise GlobalException(message=f'Installment already processed', status=HttpStatus.BAD_REQUEST)
        dto = self.findAllByQuery(
            CreditCardDto.CreditCardQueryAllDto(
                keyList = [key]
            )
        )[0]
        installmentResponseDtoList = []
        totalInstallmentValue = 0
        for installmentResponseDto in self.service.installment.findAllByKeyIn(installmentKeyList):
            try:
                if 0 >= dto.customLimit - (dto.value + installmentResponseDto.value + totalInstallmentValue):
                    self.service.credit.proccessInstalment(dto.creditKey, installmentResponseDto.key)
                    totalInstallmentValue += installmentResponseDto.value
                else:
                    raise GlobalException(message='Not enought limit', status=HttpStatus.BAD_REQUEST)
                installmentResponseDtoList.append(installmentResponseDto)
            except Exception as exception:
                log.error(self.proccessAllInstalments, f'Not possible to proccess installment {installmentResponseDto.key}', exception=exception)
                installmentResponseDtoList += self.service.installment.updateAllStatusByKeyList([installmentResponseDto.key], InstallmentStatus.ERROR)
        model = self.findAllModelByQuery(
            CreditCardDto.CreditCardQueryAllDto(
                keyList = [key]
            )
        )[0]
        model.value = dto.value + totalInstallmentValue
        self.saveModel(model)
        return installmentResponseDtoList


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
        creditResponseDtoList = self.service.credit.findAllForCreditCardCreation(
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
        authorizedRequest = self.validator.creditCard.validateDelete(key)
        self.repository.creditCard.deleteByKey(key)
