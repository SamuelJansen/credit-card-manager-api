from python_helper import DateTimeHelper
from python_framework import StaticConverter, Serializer
from python_framework import SqlAlchemyProxy as sap

from ModelAssociation import PURCHASE, MODEL
from constant import PurchaseConstant, ModelConstant
from converter.static import PurchaseStaticConverter


class Purchase(MODEL):
    __tablename__ = PURCHASE

    id = sap.Column(sap.Integer(), sap.Sequence(f'{__tablename__}{sap.ID}{sap.SEQ}'), primary_key=True)
    key = sap.Column(sap.String(sap.MEDIUM_STRING_SIZE), nullable=False, unique=True)
    creditCardKey = sap.Column(sap.String(sap.MEDIUM_STRING_SIZE), nullable=False)
    label = sap.Column(sap.String(sap.MEDIUM_STRING_SIZE), nullable=False)
    value = sap.Column(sap.Float(*ModelConstant.DEFAUTL_FLOAT_MONETARY_FORMAT), nullable=False, default=PurchaseConstant.DEFAULT_VALUE)
    purchaseAt = sap.Column(sap.DateTime(), nullable=False, default=DateTimeHelper.now())
    installments = sap.Column(sap.Integer(), nullable=False, default=PurchaseConstant.DEFAULT_INSTALLMENTS)

    def __init__(self,
        id = None,
        key = None,
        creditCardKey = None,
        label = None,
        value = None,
        installments = None,
        purchaseAt = None
    ):
        self.id = id
        self.key = StaticConverter.getValueOrDefault(key, Serializer.newUuidAsString())
        self.creditCardKey = creditCardKey
        self.label = label
        self.value = value
        self.installments = installments
        self.purchaseAt = purchaseAt
        self.setDefaultValues()

    def __onChange__(self, *args, **kwargs):
        PurchaseStaticConverter.overrideDefaultValues(self)
        return self

    def __repr__(self):
        return f'{self.__tablename__}(id={self.id}, key={self.key}, label={self.label}, value={self.value}, installments={self.installments}, purchaseAt={self.purchaseAt}, creditCardKey={self.creditCardKey})'
