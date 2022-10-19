class NoMoreTicketsForFlightsException(Exception):

    def __init__(self, flight_id, message="No more tickets for this flight"):
        self.flight_id = flight_id
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'NoMoreTicketsForFlightsException: {self.message}'


class UserAlreadyExistException(Exception):

    def __init__(self, username, email, message='User already exist'):
        self.username = username
        self.email = email
        self.message = message

    def __str__(self):
        return f'UserAlreadyExistException: {self.message}'


class TicketNotFoundException(Exception):
    def __init__(self, message="Ticket not found"):
        super().__init__(self.message)
        self.message = message

    def __str__(self):
        return f'TicketNotFoundException: {self.message}'


class PasswordTooShortException(Exception):
    def __init__(self, message="The password is too short"):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'PasswordTooShortException: {self.message}'


class FlightNotFoundException(Exception):
    def __init__(self, message="Flight not found"):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'FlightNotFound: {self.message}'


class AirlineAlreadyExistException(Exception):
    def __init__(self, message="Airline company with this parameters already exist"):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'AirlineAlreadyExist: {self.message}'


class CustomerAlreadyExistException(Exception):
    def __init__(self, message="Customer with this parameters already exist"):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'CustomerAlreadyExistException: {self.message}'


class UniqueConstraintAlreadyExist(Exception):
    def __init__(self, message="Ticket with this Unique Constraint already exist"):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'UniqueConstraintAlreadyExist: {self.message}'


class UserNotExistException(Exception):
    def __init__(self, message="The username or password is not exist"):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'UserNotExistException: {self.message}'


class AdministratorAlreadyExistException(Exception):
    def __init__(self, message="Administrator with this Unique Constraint already exist"):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'AdministratorAlreadyExistException: {self.message}'


class OtherRolePermissionsRequired(Exception):
    def __init__(self, message="You don't have the right permissions for your request"):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'OtherRolePermissionsRequired: {self.message}'


class WrongInstanceException(Exception):
    def __init__(self, message="Object must be the instance of class!"):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'WrongInstanceException: {self.message}'


class ObjectNotExistException(Exception):
    def __init__(self, message="Object does not exist in the db!"):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'ObjectNotExistException: {self.message}'

class OtherInstanceOfClassException(Exception):
    def __init__(self, message="This instance doesn't own the same id like the object!"):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'OtherInstanceOfClassException: {self.message}'

class WrongParametersException(Exception):
    def __init__(self, message="Wrong parameters for instance!"):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'WrongParametersException: {self.message}'

class DataIsNotValid(Exception):
    def __init__(self, message="The data is not valid!!!"):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'WrongParametersException: {self.message}'