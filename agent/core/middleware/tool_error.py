from __future__ import annotations

import logging
from functools import wraps
from typing import Any, Callable, TypeVar

from agent.utils.logging_config import get_logger

logger = get_logger(__name__)

FuncT = TypeVar("FuncT", bound=Callable[..., Any])


class ToolError(Exception):
    def __init__(
        self,
        message: str,
        tool_name: str | None = None,
        error_code: str | None = None,
        retryable: bool = False,
        **kwargs: Any,
    ) -> None:
        super().__init__(message)
        self.message = message
        self.tool_name = tool_name
        self.error_code = error_code
        self.retryable = retryable
        self.kwargs = kwargs

    def to_dict(self) -> dict[str, Any]:
        return {
            "message": self.message,
            "tool_name": self.tool_name,
            "error_code": self.error_code,
            "retryable": self.retryable,
            **self.kwargs,
        }


class ToolTimeoutError(ToolError):
    def __init__(
        self,
        tool_name: str | None = None,
        timeout: float | None = None,
        **kwargs: Any,
    ) -> None:
        message = f"Tool execution timed out{' after ' + str(timeout) + 's' if timeout else ''}"
        super().__init__(
            message=message,
            tool_name=tool_name,
            error_code="TIMEOUT",
            retryable=True,
            timeout=timeout,
            **kwargs,
        )


class ToolValidationError(ToolError):
    def __init__(
        self,
        message: str,
        tool_name: str | None = None,
        field: str | None = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(
            message=message,
            tool_name=tool_name,
            error_code="VALIDATION_ERROR",
            retryable=False,
            field=field,
            **kwargs,
        )


class ToolPermissionError(ToolError):
    def __init__(
        self,
        message: str,
        tool_name: str | None = None,
        permission: str | None = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(
            message=message,
            tool_name=tool_name,
            error_code="PERMISSION_DENIED",
            retryable=False,
            permission=permission,
            **kwargs,
        )


class ToolNotFoundError(ToolError):
    def __init__(self, tool_name: str, **kwargs: Any) -> None:
        super().__init__(
            message=f"Tool not found: {tool_name}",
            tool_name=tool_name,
            error_code="TOOL_NOT_FOUND",
            retryable=False,
            **kwargs,
        )


class ToolExecutionError(ToolError):
    def __init__(
        self,
        message: str,
        tool_name: str | None = None,
        original_error: Exception | None = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(
            message=message,
            tool_name=tool_name,
            error_code="EXECUTION_ERROR",
            retryable=False,
            original_error=str(original_error) if original_error else None,
            **kwargs,
        )


def handle_tool_error(
    func: FuncT,
) -> FuncT:
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        try:
            return func(*args, **kwargs)
        except ToolError as e:
            logger.error(
                f"Tool error: {e.error_code or 'UNKNOWN'} - {e.message}",
                extra={"tool_name": e.tool_name, "retryable": e.retryable},
            )
            raise
        except TimeoutError as e:
            error = ToolTimeoutError(tool_name=func.__name__, original_error=e)
            logger.error(f"Tool timeout: {error.message}")
            raise error from e
        except PermissionError as e:
            error = ToolPermissionError(
                message=str(e), tool_name=func.__name__, original_error=e
            )
            logger.error(f"Tool permission error: {error.message}")
            raise error from e
        except ValueError as e:
            error = ToolValidationError(
                message=str(e), tool_name=func.__name__, original_error=e
            )
            logger.error(f"Tool validation error: {error.message}")
            raise error from e
        except Exception as e:
            error = ToolExecutionError(
                message=str(e), tool_name=func.__name__, original_error=e
            )
            logger.error(f"Tool execution error: {error.message}", exc_info=True)
            raise error from e

    return wrapper  # type: ignore


async def async_handle_tool_error(func: Callable[..., Any]) -> Callable[..., Any]:
    @wraps(func)
    async def wrapper(*args: Any, **kwargs: Any) -> Any:
        try:
            return await func(*args, **kwargs)
        except ToolError as e:
            logger.error(
                f"Tool error: {e.error_code or 'UNKNOWN'} - {e.message}",
                extra={"tool_name": e.tool_name, "retryable": e.retryable},
            )
            raise
        except TimeoutError as e:
            error = ToolTimeoutError(tool_name=func.__name__, original_error=e)
            logger.error(f"Tool timeout: {error.message}")
            raise error from e
        except PermissionError as e:
            error = ToolPermissionError(
                message=str(e), tool_name=func.__name__, original_error=e
            )
            logger.error(f"Tool permission error: {error.message}")
            raise error from e
        except ValueError as e:
            error = ToolValidationError(
                message=str(e), tool_name=func.__name__, original_error=e
            )
            logger.error(f"Tool validation error: {error.message}")
            raise error from e
        except Exception as e:
            error = ToolExecutionError(
                message=str(e), tool_name=func.__name__, original_error=e
            )
            logger.error(f"Tool execution error: {error.message}", exc_info=True)
            raise error from e

    return wrapper


def format_error_response(error: ToolError) -> dict[str, Any]:
    return {
        "status": "error",
        "error": error.to_dict(),
    }
