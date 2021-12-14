from server import server

app = server.app

class ObjectNotFound(Exception):
    pass

class DatabaseError(Exception):
    pass

class AccountError(Exception):
    pass

@app.errorhandler(Exception)
def handle_exception(e):
    return 'Internal Error', 500

@app.errorhandler(ObjectNotFound)
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

@app.errorhandler(DatabaseError)
def handle_not_found(e):
    code = 401
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