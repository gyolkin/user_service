from fastapi import FastAPI, responses, status

from user_service.application.exceptions import (
    EntityNotExistError,
    UserAlreadyLockedError,
)


def setup_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(EntityNotExistError, _entity_not_exist_handler)
    app.add_exception_handler(
        UserAlreadyLockedError,
        _user_already_locked_handler,
    )


def _entity_not_exist_handler(
    _,
    exc: EntityNotExistError,
) -> responses.JSONResponse:
    return responses.JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={'message': str(exc)},
    )


def _user_already_locked_handler(
    _,
    exc: UserAlreadyLockedError,
) -> responses.JSONResponse:
    return responses.JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={'message': str(exc)},
    )
