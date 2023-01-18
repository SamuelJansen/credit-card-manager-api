from python_framework import Controller, ControllerMethod, HttpStatus

from domain.SecurityContext import SecurityContext
from dto import AuthorizationAccessShareDto

@Controller(
    url = '/resource/share',
    tag = 'Resource',
    description = 'Security controller'
    , logRequest = True
    , logResponse = True
)
class ResourceShareController:

    @ControllerMethod(url = '/all',
        roleRequired=[SecurityContext.ADMIN, SecurityContext.RESOURCE_ADMIN, SecurityContext.USER, SecurityContext.RESOURCE_USER],
        requestClass=[[AuthorizationAccessShareDto.AuthorizationAccessShareRequestDto]],
        responseClass=[]
    )
    def post(self, dtoList):
        return self.service.security.shareAll(dtoList), HttpStatus.CREATED

    @ControllerMethod(url = '/all',
        roleRequired=[SecurityContext.ADMIN, SecurityContext.RESOURCE_ADMIN, SecurityContext.USER, SecurityContext.RESOURCE_USER],
        requestClass=[[AuthorizationAccessShareDto.AuthorizationAccessShareRequestDto]],
        responseClass=[]
    )
    def delete(self, dtoList):
        return self.service.security.revokeAll(dtoList), HttpStatus.ACCEPTED
