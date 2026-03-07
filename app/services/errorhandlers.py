from fastapi import HTTPException


class ErrorHandler:
    @staticmethod
    def Error(e) -> HTTPException:
        return HTTPException(status_code=400, detail=str(e))

    @staticmethod
    def NotFound(e) -> HTTPException:
        return HTTPException(status_code=404, detail=str(e))

    @staticmethod
    def Unauthorized(e) -> HTTPException:
        return HTTPException(status_code=401, detail=str(e))

    @staticmethod
    def Forbidden(e) -> HTTPException:
        return HTTPException(status_code=403, detail=str(e))

    @staticmethod
    def ServerError(e) -> HTTPException:
        return HTTPException(status_code=500, detail=str(e))

    @staticmethod
    def ALreadyExists(e) -> HTTPException:
        return HTTPException(status_code=409, detail=str(e))

    @staticmethod
    def UnprocessableEntity(e) -> HTTPException:
        return HTTPException(status_code=422, detail=str(e))
