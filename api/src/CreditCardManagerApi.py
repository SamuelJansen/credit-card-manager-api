from python_framework import ResourceManager, Serializer

from model import ModelAssociation


app = ResourceManager.initialize(__name__, ModelAssociation.MODEL, managerList=[])


import io
import csv
from flask import make_response
from dto import CreditCardDto


@app.route(f'{app.api.baseUrl}/download', methods=['GET'])
def get():
    si = io.StringIO()
    cw = csv.writer(si)
    cw.writerows([
        [f'{creditCard.label}', f'{creditCard.value}']
        for creditCard in app.api.resource.repository.creditCard.findAllByQuery(
            Serializer.getObjectAsDictionary(CreditCardDto.CreditCardQueryDto())
        )
    ])
    output = make_response(si.getvalue())
    output.headers["Content-Disposition"] = "attachment; filename=export.csv"
    output.headers["Content-type"] = "text/csv"
    return output