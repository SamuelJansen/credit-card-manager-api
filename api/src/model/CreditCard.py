from python_framework import StaticConverter, Serializer
from python_framework import SqlAlchemyProxy as sap

from ModelAssociation import CREDIT_CARD, MODEL
from constant import CreditCardConstant, ModelConstant
from converter.static import CreditCardStaticConverter


class CreditCard(MODEL):
    __tablename__ = CREDIT_CARD

    id = sap.Column(sap.Integer(), sap.Sequence(f'{__tablename__}{sap.ID}{sap.SEQ}'), primary_key=True)
    key = sap.Column(sap.String(sap.MEDIUM_STRING_SIZE), nullable=False, unique=True)
    creditKey = sap.Column(sap.String(sap.MEDIUM_STRING_SIZE), nullable=False)
    label = sap.Column(sap.String(sap.MEDIUM_STRING_SIZE), nullable=False)
    customLimit = sap.Column(sap.Float(*ModelConstant.DEFAUTL_FLOAT_MONETARY_FORMAT), nullable=False, default=CreditCardConstant.DEFAULT_CUSTOM_LIMIT)
    value = sap.Column(sap.Float(*ModelConstant.DEFAUTL_FLOAT_MONETARY_FORMAT), nullable=False, default=CreditCardConstant.DEFAULT_VALUE)
    expirationDate = sap.Column(sap.Date(), nullable=False)
    closingDay = sap.Column(sap.Integer(), nullable=False, default=CreditCardConstant.DEFAULT_CLOSING_DAY)
    dueDay = sap.Column(sap.Integer(), nullable=False, default=CreditCardConstant.DEFAULT_DUE_DAY)

    def __init__(self,
        id = None,
        key = None,
        creditKey = None,
        label = None,
        customLimit = None,
        value = None,
        expirationDate = None,
        closingDay = None,
        dueDay = None
    ):
        self.id = id
        self.key = StaticConverter.getValueOrDefault(key, Serializer.newUuidAsString())
        self.creditKey = creditKey
        self.label = label
        self.customLimit = customLimit
        self.value = value
        self.expirationDate = expirationDate
        self.closingDay = closingDay
        self.dueDay = dueDay
        self.setDefaultValues()

    def __onChange__(self, *args, **kwargs):
        CreditCardStaticConverter.overrideDefaultValues(self)
        return self

    def __repr__(self):
        return f'{self.__tablename__}(id={self.id}, key={self.key}, label={self.label}, closingDay={self.closingDay}, dueDay={self.dueDay}, creditKey={self.creditKey})'
