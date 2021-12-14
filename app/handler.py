from server import server
from errors import ObjectNotFound, DatabaseError, AccountError
app = server.app

@app.errorhandler(Exception)
def handle_exception(e):
    code = 500
    msg = {
        "error": {
            "message": str(e),
            "type": e.__class__.__name__,
            "code": code
        }
    }
    return msg, code

@app.errorhandler(ObjectNotFound)
def handle_not_found(e):
    code = 404
    msg = {
        "error": {
            "message": str(e),
            "type": e.__class__.__name__,
            "code": code
        }
    }
    return msg, code

@app.errorhandler(ObjectBadFormat)
@app.errorhandler(DatabaseError)
def handle_not_found(e):
    code = 400
    msg = {
        "error": {
            "message": str(e),
            "type": e.__class__.__name__,
            "code": code
        }
    }
    return msg, code

@app.errorhandler(AccountError)
def handle_not_found(e):
    code = 201
    msg = {
        "error": {
            "message": str(e),
            "type": e.__class__.__name__,
            "code": code
        }
    }
    return msg, code