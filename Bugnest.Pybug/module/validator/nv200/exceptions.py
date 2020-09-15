class ValidatorError(Exception):
    def __init__(self, msg):
        super().__init__('Validator Error >> '+msg)
