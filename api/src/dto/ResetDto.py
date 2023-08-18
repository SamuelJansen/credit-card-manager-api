class ResetRequestDto:
    def __init__(self,
        credit = None,    
        creditCardList = None
    ):
        self.credit = credit
        self.creditCardList = creditCardList


class ResetResponseDto:
    def __init__(self,
        credit = None,    
        creditCardList = None
    ):
        self.credit = credit
        self.creditCardList = creditCardList