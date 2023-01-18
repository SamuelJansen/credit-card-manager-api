from globals import getGlobalsInstance
globalsInstance = getGlobalsInstance()
from domain import AuthorizationOperation


ADMIN_0_ACCOUNT_KEY = globalsInstance.getSetting('simple-accounts.admin-zero')
USER_0_ACCOUNT_KEY = globalsInstance.getSetting('simple-accounts.user-zero')
USER_1_ACCOUNT_KEY = globalsInstance.getSetting('simple-accounts.user-one')

ADMIN_ACCOUNT_KEYS = [
    ADMIN_0_ACCOUNT_KEY
]

USER_ACCOUNT_KEYS = [
    USER_0_ACCOUNT_KEY,
    USER_1_ACCOUNT_KEY
]

ADMIN_OPERATIONS = [
    AuthorizationOperation.GET,
    AuthorizationOperation.POST,
    AuthorizationOperation.PATCH,
    AuthorizationOperation.PUT,
    AuthorizationOperation.DELETE
]
USER_OPERATIONS = [
    AuthorizationOperation.GET
]
