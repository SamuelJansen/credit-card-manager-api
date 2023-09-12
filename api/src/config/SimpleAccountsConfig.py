from globals import getGlobalsInstance
globalsInstance = getGlobalsInstance()
from domain import AuthorizationOperation


ADMIN_0_ACCOUNT_KEY = globalsInstance.getSetting('simple-accounts.admin-zero.user')
ADMIN_1_ACCOUNT_KEY = globalsInstance.getSetting('simple-accounts.admin-one.user')
USER_0_ACCOUNT_KEY = globalsInstance.getSetting('simple-accounts.user-zero.user')
USER_1_ACCOUNT_KEY = globalsInstance.getSetting('simple-accounts.user-one.user')

ADMIN_0_AUTHORIZATION = globalsInstance.getSetting('simple-accounts.admin-zero.authorization')
ADMIN_1_AUTHORIZATION = globalsInstance.getSetting('simple-accounts.admin-one.authorization')
USER_0_AUTHORIZATION = globalsInstance.getSetting('simple-accounts.user-zero.authorization')
USER_1_AUTHORIZATION = globalsInstance.getSetting('simple-accounts.user-one.authorization')

ADMIN_ACCOUNT_KEYS = [
    ADMIN_0_ACCOUNT_KEY,
    ADMIN_1_ACCOUNT_KEY
]
USER_ACCOUNT_KEYS = [
    USER_0_ACCOUNT_KEY,
    USER_1_ACCOUNT_KEY
]

ADMIN_AUTHORIZATIONS = [
    ADMIN_0_AUTHORIZATION
    , ADMIN_1_AUTHORIZATION
]
USER_AUTHORIZATIONS = [
    USER_0_AUTHORIZATION
    , USER_1_AUTHORIZATION
]

class AuthenticatedUser:
    def __init__(self, userKey=None, authentication=None):
        self.userKey = userKey
        self.authentication = authentication

AUTHENTICATED_USERS = [
    AuthenticatedUser(ADMIN_0_ACCOUNT_KEY, ADMIN_0_AUTHORIZATION),
    AuthenticatedUser(ADMIN_1_ACCOUNT_KEY, ADMIN_1_AUTHORIZATION),
    AuthenticatedUser(USER_0_ACCOUNT_KEY, USER_0_AUTHORIZATION),
    AuthenticatedUser(USER_1_ACCOUNT_KEY, USER_1_AUTHORIZATION),
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
