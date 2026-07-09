class DatabaseError(Exception):
    """Base database exception for BloodIQ."""


class DatabaseConnectionError(DatabaseError):
    """Raised when the database cannot be reached or authenticated."""


class DatabaseOperationError(DatabaseError):
    """Raised when a transaction or CRUD operation fails."""