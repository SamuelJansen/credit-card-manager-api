from python_framework import Controller, ControllerMethod, HttpStatus

from domain.SecurityContext import SecurityContext


@Controller(
    url = '/security/state',
    tag = 'Security',
    description = 'Security controller'
    # , logRequest = True
    # , logResponse = True
)
class SecurityStateController:

    @ControllerMethod(url = '/',
        roleRequired=[SecurityContext.ADMIN, SecurityContext.RESOURCE_ADMIN],
        requestClass=[],
        responseClass=[dict]
    )
    def get(self):
        return self.service.security.getState(), HttpStatus.OK
