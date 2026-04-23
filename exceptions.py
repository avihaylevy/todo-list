# Task not found exception
class TaskNotFoundException(Exception):
    pass


# Task cannot be empty exception
class TaskCannotBeEmptyException(Exception):
    pass


# Already exists exception
class TaskAlreadyExistsException(Exception):
    pass
