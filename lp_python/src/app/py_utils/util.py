"""
util file for helper Util class that contains various helper methods for application
"""
from importlib.resources import is_resource
import os

from datetime import datetime
from app.database import sql_api

# pylint: disable=W0702


class Util:
    """
    utils class
    messages from here will be labeled Util:
    """

    def __init__(self) -> None:
        pass

    @staticmethod
    def update_row_dates(
        table_name: str, updated_by: str, updated_date: datetime, feature_id: str
    ) -> None:
        """
        method for updating updated by and updated date for table rows
        args:
          table_name: table where row that needs update lives
          updated_by: name of operator who updated entry (ex: py-script)
          updated_date: date that table was updated
          feature_id: featId of row being updated
        """
        row_query = (
            "UPDATE %s SET `Updated By` = %s AND `Updated Date` = %s WHERE FeatId = %s"
        )
        row_data = (table_name, updated_by, updated_date, feature_id)
        sql_api.insert(row_query, row_data)

    @staticmethod
    def get_datetime_from_file(file: str) -> datetime:
        """
        helper method to convert file date into datetime
        arg:
            file - file name for pdf (EX: 05-19-21  01:57AM  2385362 s0016.pdf)
        """
        file_date = file.split(" ")[0].split("-")
        file_time = file.split(" ")[2]
        military_time = datetime.strptime(file_time, "%I:%M%p").strftime("%H:%M")
        year = int("20" + file_date[2])
        day = int(file_date[1])
        month = int(file_date[0])
        hour = int(military_time.split(":")[0])
        minute = int(military_time.split(":")[1])
        return datetime(year, month, day, hour, minute, 0, 0)

    @staticmethod
    def create_local_directory(file_path: str) -> None:
        """
        method to create local directory so ftp functions
        can upload pdfs into it
        args:
            file_path - name of local directory to create under
            assets / pdf
        """
        try:
            os.makedirs(f"./assets/pdf/{file_path}")
            print("Util: Local directory made for", file_path)
        except Exception as error:
            print("Util: local directory already exist", error)

    @staticmethod
    def remove_local_file(file_path: str) -> None:
        """
        method that removes file from local directory
        args:
            file_path - file path from local directory
        """
        try:
            os.remove(file_path)
            print("Util: successfully remove file", file_path)
        except Exception as error:
            print(f"error removing {file_path}", error)

    @staticmethod
    def get_cloud_storage_path(ftp_file_path: str, file_name: str) -> str:
        """
        method that creates cloud storage path from give file path
        args:
            ftp_file_path - file path from ftp server
        """
        cloud_storage_path = ""
        file_path_list = ftp_file_path.split("/")
        folder_name = file_name.split(".")[0]
        for index, file in enumerate(file_path_list):
            if file == "Documents":
                cloud_storage_path = "/".join(
                    [*file_path_list[index:-1], folder_name, file_name]
                )
        return cloud_storage_path

    @staticmethod
    def get_blob_uri(blob_name: str, ftp_file_path: str) -> str:
        """
        function for handling blob uri
        for different data types and file locations
        args:
          blob_name - name of object in google cloud
          ftp_file_path - file path that object comes from in ftp server
        """
        return f"gs://py_landpro/{ftp_file_path}{blob_name}/{blob_name}.pdf"

    @staticmethod
    def order_file_by_datetime(files: list):
        file_datetime_list = []
        for file in files:
            file_extension = file.split(".")[-1]
            if (file_extension != "tif") and (file_extension != "TIF"):
                file_date = file.split(" ")[0].split("-")
                file_time = file.split(" ")[2]
                military_time = datetime.strptime(file_time, "%I:%M%p").strftime(
                    "%H:%M"
                )
                year = int("20" + file_date[2])
                day = int(file_date[1])
                month = int(file_date[0])
                hour = int(military_time.split(":")[0])
                minute = int(military_time.split(":")[1])
                file_datetime = datetime(year, month, day, hour, minute, 0, 0)
                file_datetime_list.append(
                    {"file": file, "file_datetime": file_datetime}
                )
                sorted_files = sorted(
                    file_datetime_list, key=lambda x: x["file_datetime"], reverse=True
                )
        return [item["file"] for item in sorted_files][:100]
