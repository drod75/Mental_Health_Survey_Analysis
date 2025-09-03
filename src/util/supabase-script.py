import os
from supabase import create_client, Client
from dotenv import load_dotenv
import logging
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

    def fetch_data(self, table_name: str, **filters: str):
        """
        Fetches data from a Supabase table with multiple filter conditions.

        Args:
            table_name: The name of the table to fetch data from.
            **filters: Keyword arguments where the key is the column name
                       and the value is the filter value.

        Returns:
            The data from the table that matches the filter conditions.
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
                logger.warning(f"No data found for the given filters in {table_name}.")
                return None

        except Exception as e:
            logger.error(f"An error occurred: {e}")

    def insert_data(self, table_name: str, data: dict) -> bool:
        """
        Takes in a table name and inserts the data which is a dictionary, into the table that is in supabase.

        Args:
            table_name (str): _description_
            data (dict): _description_

        Returns:
            bool: Inidcator whether or not operation succeeded
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
