import os
from supabase import create_client, Client
from dotenv import load_dotenv
import logging
from typing import Optional, Any
from rich.console import Console

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)
logger.info("Supabase process starting!")


class SupabaseScript:
    def __init__(self) -> None:
        load_dotenv()

        self.supabase_url = os.getenv("SUPABASE_URL")
        self.supabase_key = os.getenv("SUPABASE_KEY")

        self.supabase: Client = create_client(self.supabase_url, self.supabase_key)  # type: ignore

    def fetch_data(self, table_name: str, **filters: str) -> Optional[Any]:
        """The `fetch_data` function retrieves data from a specified table in a database based on provided
        filters.

        Parameters
        ----------
        table_name : str
            The `table_name` parameter in the `fetch_data` method is a string that specifies the name of the
        table from which data needs to be fetched.
         : str
            The `fetch_data` method takes in a `table_name` parameter as a string and any number of keyword
        arguments (**filters) where the key is a column name and the value is the filter value for that
        column. The method then constructs a query to fetch data from the specified table based on the

        Returns
        -------
            The `fetch_data` method returns the fetched data from the specified table if data is found based on
        the provided filters. If no data is found for the given filters, it returns `None`.

        """
        try:
            query = self.supabase.table(table_name).select("*")

            for column, value in filters.items():
                query = query.eq(column, value)

            response = query.execute()

            if response.data:
                logger.info(f"Successfully fetched data from {table_name}")
                return response.data
            else:
                logger.warning(
                    f"No data found for {table_name}, if this is an error check filters."
                )
                return None

        except Exception as e:
            logger.error(f"An error occurred: {e}")

    def insert_data(self, table_name: str, data: dict) -> bool:
        """The `insert_data` function inserts data into a specified table and returns a boolean indicating
        success or failure.

        Parameters
        ----------
        table_name : str
            The `table_name` parameter in the `insert_data` method refers to the name of the table in which you
        want to insert the data. It is a string that specifies the name of the table where the data will be
        inserted.
        data : dict
            The `data` parameter in the `insert_data` method is expected to be a dictionary containing the data
        that you want to insert into the specified table. Each key-value pair in the dictionary represents a
        column and its corresponding value that you want to insert into the table.

        Returns
        -------
            The `insert_data` method returns a boolean value. It returns `True` if the data insertion was
        successful, and `False` if there was an error during the insertion process.

        """
        try:
            query = self.supabase.table(table_name).insert(data)
            response = query.execute()

            if response.data:
                logger.info(f"Successfully inserted data into {table_name}")
            else:
                logger.warning(f"Failed to insert data into {table_name}.")
                return False

        except Exception as E:
            logger.error(f"An error occurred: {E}")
            return False

        return True


def testing(script: SupabaseScript) -> bool:
    """The function `testing` fetches data from a table named "survey_data" using a SupabaseScript object
    and prints the data to the console, returning True if successful and logging an error message if an
    exception occurs.

    Parameters
    ----------
    script : SupabaseScript
        The `script` parameter in the `testing` function is expected to be an object of type
    `SupabaseScript`. This object likely contains methods and properties related to interacting with a
    Supabase database or executing scripts on a Supabase server.

    Returns
    -------
        The function `testing` is returning a boolean value. If the try block is executed successfully
    without any exceptions, it will return `True`. If an exception occurs during the execution of the
    try block, it will catch the exception, log an error message, and return `False`.

    """
    try:
        data = script.fetch_data(table_name="survey_data")
        console = Console()
        console.print(data)

    except Exception as E:
        logger.error(f"Error trying to run tests, {str(E)}")
        return False

    return True


if __name__ == "__main__":
    scripter = SupabaseScript()
    if not testing(scripter):
        logger.error("Error trying to run supabase process")

    logger.info("Supabase process was successful!")
