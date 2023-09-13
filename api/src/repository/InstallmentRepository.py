from python_helper import ObjectHelper, Method

from python_framework import SqlAlchemyProxy as sap
from python_framework import Repository

from model import Installment, Purchase


@Repository(model = Installment.Installment)
class InstallmentRepository:

    @Method
    def getQueryFilter(self, query, modelClass, joinList=None, additionalCondition=None):
        sessionQuery = self.repository.session.query(modelClass)
        if ObjectHelper.isNotEmpty(joinList):
            for join in joinList:
                sessionQuery.join(join)
        return self.repository.getQueryFilter(
            query,
            modelClass,
            additionalCondition = additionalCondition
        )

    @Method
    def findAllByQueryAndCommit(self, query, modelClass, joinList=None, additionalCondition=None):
        instanceList = []
        if ObjectHelper.isNotNone(query):
            instanceList = self.getQueryFilter(
                query,
                modelClass,
                joinList = joinList,
                additionalCondition = additionalCondition
            ).all()
        self.repository.session.commit()
        return self.repository.load(instanceList)

    @Method
    def existsByQueryAndCommit(self, query, modelClass, joinList=None, additionalCondition=None):
        exists = self.repository.session.query(
            sap.literal(True)
        ).filter(
            self.getQueryFilter(
                query,
                modelClass,
                joinList = joinList,
                additionalCondition = additionalCondition
            ).exists()
        ).scalar()
        self.repository.session.commit()
        return exists

    def save(self, model):
        return self.repository.saveAndCommit(model)

    def saveAll(self, modelList):
        return self.repository.saveAllAndCommit(modelList)

    def findAll(self):
        return self.repository.findAllAndCommit(self.model)

    def findByKey(self, key):
        return self.repository.findByKeyAndCommit(key, self.model)

    def findAllByKeyIn(self, keyList):
        return self.repository.findAllByKeyInAndCommit(keyList, self.model)

    def existsByKey(self, key):
        return self.repository.existsByKeyAndCommit(key, self.model)

    def notExistsByKey(self, key):
        return not self.existsByKey(key)

    def deleteByKey(self, key):
        self.repository.deleteByKeyAndCommit(key, self.model)

    def deleteAllByKeyIn(self, keyList):
        if ObjectHelper.isEmpty(keyList):
            return []
        self.repository.deleteAllByKeyInAndCommit(keyList, self.model)

    def findById(self, id):
        return self.repository.findByIdAndCommit(id, self.model)

    def findAllByIdIn(self, idList):
        return self.repository.findAllByIdInAndCommit(idList, self.model)

    def existsById(self, id):
        return self.repository.existsByIdAndCommit(id, self.model)

    def notExistsById(self, id):
        return not self.existsById(id)

    def deleteById(self, id):
        self.repository.deleteByIdAndCommit(id, self.model)

    def findAllByQuery(self, query, joinList=None, additionalCondition=None):
        return self.findAllByQueryAndCommit(query, self.model, joinList=joinList, additionalCondition=additionalCondition)

    def findAllByQueryWithinInstallmentDatesAndCreditCardKeyIn(self, query, fromDateTime, toDateTime, creditCardKeyList):
        return self.findAllByQuery(
            query,
            joinList = [] if ObjectHelper.isEmpty(creditCardKeyList) else [Purchase.Purchase],
            additionalCondition = sap.and_(
                sap.and_(
                    self.model.installmentAt >= fromDateTime,
                    self.model.installmentAt <= toDateTime
                ),
                sap.and_(
                    True if ObjectHelper.isEmpty(creditCardKeyList) else Purchase.Purchase.key == self.model.purchaseKey,
                    True if ObjectHelper.isEmpty(creditCardKeyList) else Purchase.Purchase.creditCardKey.in_(creditCardKeyList)
                )
            )
        )

    def existsByQuery(self, query):
        return self.repository.existsByQueryAndCommit(query, self.model)
