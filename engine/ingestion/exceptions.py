"""Domain-specific exceptions for secure repository ingestion."""


class RepositoryIngestionError(Exception):
    """Base exception for repository-ingestion failures."""


class RepositoryNotFoundError(RepositoryIngestionError):
    """Raised when the requested repository does not exist."""


class InvalidRepositoryError(RepositoryIngestionError):
    """Raised when the supplied path is not a valid repository directory."""


class RepositoryLimitExceededError(RepositoryIngestionError):
    """Raised when a configured ingestion safety limit is exceeded."""


class UnsafeRepositoryPathError(RepositoryIngestionError):
    """Raised when a repository path violates a security boundary."""