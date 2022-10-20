import dataclasses
import sqlite3
import databases

from quart import Quart, request, jsonify, abort, g


@dataclasses.dataclass
class User:
    user_id: str
    user_pass: str



def validate_request(User):
    pass

async def _get_db():
    db = getattr(g, "_sqlite_db", None)
    if db is None:
        db = g._sqlite_db = databases.Database(app.config["DATABASES"]["URL"])
        await db.connect()
    return db



@app.errorhandler(401)
def invalid_user():
    return {"error": "The Username or password is invalid,Try again!!"}, 401

def verify_user(db, authorization):
    if authorization is not None:
        print(authorization.type + "Name: "+authorization.username+"Password: "+authorization.password)

        if authorization is not None and authorization.type == 'basic':
            responseFromDB = await db.fetch_one("SELECT user_id FROM users where usr_id :username user_pass=:password",
                                                values={"username": authorization.username, "password": authorization.password})
            app.logger.debug(type(responseFromDB))
            if responseFromDB:
                return responseFromDB.user_id
            else:
                print("Error with the username or password")
                abort(401)
        else:
            abort(401)



