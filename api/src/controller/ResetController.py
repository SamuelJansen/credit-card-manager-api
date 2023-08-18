from python_framework import Controller, ControllerMethod, HttpStatus

from domain.SecurityContext import SecurityContext
from dto import ResetDto


@Controller(
    url = '/reset',
    tag = 'Reset',
    description = 'Reset controller'
    # , logRequest = True
    # , logResponse = True
)
class ResetAllController:

    @ControllerMethod(url = '/all',
        roleRequired=[SecurityContext.RESET_ADMIN],
        requestClass=[[ResetDto.ResetRequestDto]],
        responseClass=[[ResetDto.ResetResponseDto]]
    )
    def put(self, dtoList):
        return self.service.reset.resetAll(dtoList), HttpStatus.ACCEPTED
