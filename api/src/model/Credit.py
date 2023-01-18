from python_framework import StaticConverter, Serializer
from python_framework import SqlAlchemyProxy as sap

from ModelAssociation import CREDIT, MODEL
from constant import CreditConstant, ModelConstant
from converter.static import CreditStaticConverter


class Credit(MODEL):
    __tablename__ = CREDIT

    id = sap.Column(sap.Integer(), sap.Sequence(f'{__tablename__}{sap.ID}{sap.SEQ}'), primary_key=True)
    key = sap.Column(sap.String(sap.MEDIUM_STRING_SIZE), nullable=False, unique=True)
    limit = sap.Column(sap.Float(*ModelConstant.DEFAUTL_FLOAT_MONETARY_FORMAT), nullable=False, default=CreditConstant.DEFAULT_LIMIT)
    customLimit = sap.Column(sap.Float(*ModelConstant.DEFAUTL_FLOAT_MONETARY_FORMAT), nullable=False, default=CreditConstant.DEFAULT_CUSTOM_LIMIT)
    value = sap.Column(sap.Float(*ModelConstant.DEFAUTL_FLOAT_MONETARY_FORMAT), nullable=False, default=CreditConstant.DEFAULT_VALUE)

    def __init__(self,
        id = None,
        key = None,
        limit = None,
        customLimit = None,
        value = None
    ):
        self.id = id
        self.key = StaticConverter.getValueOrDefault(key, Serializer.newUuidAsString())
        self.limit = limit
        self.customLimit = customLimit
        self.value = value
        self.setDefaultValues()

    def __onChange__(self, *args, **kwargs):
        CreditStaticConverter.overrideDefaultValues(self)
        return self

    def __repr__(self):
        return f'{self.__tablename__}(id={self.id}, key={self.key}, value={self.value}, customLimit={self.customLimit}, limit={self.limit})'
