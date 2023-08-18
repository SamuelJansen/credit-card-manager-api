from python_helper import DateTimeHelper
from python_framework import StaticConverter, Serializer
from python_framework import SqlAlchemyProxy as sap

from ModelAssociation import INSTALLMENT, MODEL
from constant import InstallmentConstant, ModelConstant
from converter.static import InstallmentStaticConverter


class Installment(MODEL):
    __tablename__ = INSTALLMENT

    id = sap.Column(sap.Integer(), sap.Sequence(f'{__tablename__}{sap.ID}{sap.SEQ}'), primary_key=True)
    key = sap.Column(sap.String(sap.MEDIUM_STRING_SIZE), nullable=False, unique=True)
    purchaseKey = sap.Column(sap.String(sap.MEDIUM_STRING_SIZE), nullable=False)
    label = sap.Column(sap.String(sap.MEDIUM_STRING_SIZE), nullable=False)
    value = sap.Column(sap.Float(*ModelConstant.DEFAUTL_FLOAT_MONETARY_FORMAT), nullable=False, default=InstallmentConstant.DEFAULT_VALUE)
    installmentAt = sap.Column(sap.DateTime(), nullable=False, default=DateTimeHelper.now())
    installments = sap.Column(sap.Integer(), nullable=False)
    order = sap.Column(sap.Integer(), nullable=False)
    status = sap.Column(sap.String(sap.MEDIUM_STRING_SIZE), nullable=False, default=InstallmentConstant.DEFAULT_STATUS)

    def __init__(self,
        id = None,
        key = None,
        purchaseKey = None,
        label = None,
        value = None,
        installmentAt = None,
        installments = None,
        order = None,
        status = None
    ):
        self.id = id
        self.key = StaticConverter.getValueOrDefault(key, Serializer.newUuidAsString())
        self.purchaseKey = purchaseKey
        self.label = label
        self.value = value
        self.installmentAt = installmentAt
        self.installments = installments
        self.order = order
        self.status = status
        self.setDefaultValues()

    def __onChange__(self, *args, **kwargs):
        InstallmentStaticConverter.overrideDefaultValues(self)
        return self

    def __repr__(self):
        return f'{self.__tablename__}(id={self.id}, key={self.key}, label={self.label}, value={self.value}, installmentAt={self.installmentAt}, purchaseAt={self.purchaseAt}, purchaseKey={self.purchaseKey})'
