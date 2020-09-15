class APIErorr(Exception):
    def __init__(self, msg):
        super().__init__('API error >> '+ msg)

class APIResponse:
    def __init__(self, is_error=bool(), message=str(), status=str()):
        self.is_error = is_error
        self.message = message
        self.status = status

class LoginResponse(APIResponse):
    def __init__(self, is_error=bool(), message=str(), status=str(), key=str()):
        super().__init__(is_error, message, status)
        self.key = key

class GetDebtResponse(APIResponse):
    class Data:
        def __init__(self, username=str(), payment_status=int(), total_payment=float()):
            self.username = username
            self.payment_status = payment_status
            self.total_payment = total_payment

    def __init__(self, is_error=bool(), message=str(), status=str(), data=None):
        super().__init__(is_error, message, status)
        self.data = data

class CheckPermissionResponse(APIResponse):
    class Data:
        def __init__(self, username=str(), payment_status=int(), total_payment=float(), otp= None, otp_expire_date= int()):
            self.username = username
            self.payment_status = payment_status
            self.total_payment = total_payment
            self.otp= otp
            self.otp_expire_date= otp_expire_date

    def __init__(self, is_error=bool(), message=str(), status=str(), data=None):
        super().__init__(is_error, message, status)
        self.data = data

class ChangeResponse(APIResponse):
    def __init__(self, is_error=bool(), status=str(), data=None, message=str()):
        super().__init__(is_error, message, status)
        self.data = data

class UpdateDebtResponse(APIResponse):
    def __init__(self, is_error=bool(), status=str(), data=None, message=str()):
        super().__init__(is_error, message, status)
        self.data = data