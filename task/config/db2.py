import mysql.connector
import logging as logger
import datetime
from dotenv import load_dotenv
import os

load_dotenv()  # take environment variables from .env.
HOST = os.environ.get("DB_DEFAULT_HOSTNAME")
PORT = os.environ.get("DB_DEFAULT_PORT")
USERNAME = os.environ.get("DB_DEFAULT_USERNAME")
PASS = os.environ.get("DB_DEFAULT_PASSWORD")
DBNAME = os.environ.get("DB_DEFAULT_DATABASE_NAME")


class Database:
    __instance = None
    def __init__(self):
        if self.__instance is None or self.__instance.is_connected() == False:
            self.__instance = mysql.connector.connect(
                user=USERNAME,
                password=PASS,
                host=HOST,
                database=DBNAME,
            )
            self.__instance.autocommit = False
    def query(self, query, autoCommit=None, fetch="ALL"):
        print("in db2:",datetime.datetime.now())
        try:
            cursor = self.__instance.cursor()
            print("in db2:",datetime.datetime.now())
            result = cursor.execute(query)
            print("in db2:",datetime.datetime.now())
            return result
            if autoCommit is not None:
                self.__instance.commit()
                operation = True if cursor.lastrowid == 0 else {"id": cursor.lastrowid}
                return {"result": operation}
            fields = [field_md[0] for field_md in cursor.description]
            if fetch != "SINGLE":
                result = [dict(zip(fields, row)) for row in cursor.fetchall()]
                return {"result": result}
            else:
                result = [dict(zip(fields, row)) for row in cursor.fetchone()]
                return {"result": result}
        except Exception as e:
            return {"result": None, "error": e, "query": query}
            logger.error(e)
        finally:
            if self.__instance.is_connected():
                logger.info("Mantendo conexão.")
                # self.__instance.cursor.close()
                # self.__instance.close()
                # logger.debug("Removendo instancia da Database... 