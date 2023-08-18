from python_helper import ObjectHelper
from python_framework import SqlAlchemyProxy as sap
from python_framework import Repository

from model import Credit


@Repository(model = Credit.Credit)
class CreditRepository:

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

    # def deleteAllByKeyIn(self, keyList):
    #     if ObjectHelper.isEmpty(keyList):
    #         return []
    #     self.repository.deleteAllByKeyInAndCommit(keyList, self.model)

    def deleteAllByKeyIn(self, keyList):
        if ObjectHelper.isEmpty(keyList):
            return []
        self.repository.deleteAllByKeyInAndCommit(self.model, keyList)

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

    def findAllByQuery(self, query):
        return self.repository.findAllByQueryAndCommit(query, self.model)

    def existsByQuery(self, query):
        return self.repository.existsByQueryAndCommit(query, self.model)
