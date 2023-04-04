import mysql.connector as msc
from mysql.connector.types import RowType
import os
from src.lib.result import Result

def create_connection() -> Result[msc.MySQLConnection, Exception]:
    """Create a connection to the database.

    Returns:
        Result[msc.MySQLConnection, Exception]: The connection to the database.
    """
    try:
        db_conn = msc.connect(
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            db=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            passwd=os.getenv("DB_PASS")
        )
        
        return Result.ret(db_conn)
    except Exception as e:
        return Result.Err(e)
    
def execute_query(query: str, db_conn: msc.MySQLConnection, values: tuple[str | int | float] | list[tuple[str | int | float]] | None = None) -> Result[RowType, Exception]:
    """Execute a query on the database.
    
    WARNING: This function does not make any attempt at sanitizing the query string.
    Please make sure that the query string is sanitized before passing it to this function.

    Args:
        query (str): The query to execute.
        db_conn (msc.MySQLConnection): The connection to the database.
        values (tuple[str  |  int  |  float] | list[tuple[str  |  int  |  float]] | None, optional): The values to pass to the query as arguments. Defaults to None.
        
    Example:
    
    ```
    db_conn = create_connection()
    query = "SELECT * FROM users WHERE username = %s"
    values = ("username",)
    result = execute_query(query, db_conn, values)
    ```
    """
    
    try:
        cursor = db_conn.cursor()
        cursor.execute(query, values)
        rt_result = cursor.fetchall()
        cursor.close()
    
        return Result.ret(rt_result)
    except Exception as e:
        return Result.Err(e)

def destroy_connection(db_conn: msc.MySQLConnection):
    """Destroy the connection to the database.

    Args:
        db_conn (msc.MySQLConnection): The connection to the database.
    """
    db_conn.close()