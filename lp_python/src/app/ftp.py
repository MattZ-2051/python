"""
this file will contain ftp class that will handle file operations for local and
ftp directory
"""
import os

from ftplib import FTP
from app.py_utils import Util
from app.config import Config
from app.models import DataProcessor


class FtpServer:
    """
    class to handle file ftp server functionality
    when initiatied it will login to the server using
    env file credentials
    messages from this file will be labeled ftp:
    """

    def __init__(self) -> None:
        self._login()

    def _login(self) -> None:
        ftp = FTP(Config.FTP_HOST)
        try:
            ftp.login(Config.FTP_USER, Config.FTP_PASS)
            self.ftp_connection = ftp
            print("ftp: Logged into FTP server")
        except:
            print("ftp: Error connecting to FTP server")

    def _logout(self) -> None:
        try:
            self.ftp_connection.close()
            print("ftp: connection closed")
        except Exception as logout_error:
            print("ftp: error closing connection", logout_error)

    def get_pdf_files_from_path(self, ftp_file_path: str) -> list:
        """
        method to return pdf files from given directory
        args:
            ftp_file_path - ftp file server path of intended directory to be read from
        """
        self._login()
        pdf_files = []
        with self.ftp_connection as ftp:
            files = []
            ftp.cwd(ftp_file_path)
            ftp.dir(files.append)
            sorted_files = Util.order_file_by_datetime(files)
            for file in sorted_files:
                if file.split(".")[-1] == "pdf":
                    pdf_files.append(file)
        self._logout()
        return pdf_files

    def download_files(self, ftp_file_path: str) -> None:
        """
        function for downloading files from ftp server file directory
        to local directory

        args:
          ftp_file_path - path from ftp server
        """
        self._login()
        with self.ftp_connection as ftp:
            # sorted_files = self._get_sorted_file_list(ftp_file_path)
            files = []
            ftp.cwd(ftp_file_path)
            ftp.dir(files.append)  # Takes a callback for each file
            sorted_files = Util.order_file_by_datetime(files)
            for file in sorted_files:
                file_name = file.split(" ")[-1]
                # Write file in binary mode to local repo under assets/pdf
                local_file_path = (
                    f"{os.getcwd()}/assets/pdf/{ftp_file_path}/{file_name}"
                )
                try:
                    with open(local_file_path, "wb") as file:
                        try:
                            ftp.retrbinary(f"RETR {file_name}", file.write)
                        except Exception as ftp_error:
                            print(
                                "ftp: error downloading file",
                                ftp_error,
                                "for file",
                                file_name,
                            )
                except Exception as file_error:
                    print("ftp: error writing file", file_error)
        self._logout()

    def get_bucket_info(self, ftp_file_dir: str, obj_name: str = None) -> list:
        """
        function that takes a file path and returns info for bucket operations
        returns
        {
            bucket_path: path to bucket for blob when uploading to google cloud
            local_file_path: path to you want to upload in local directory
            blob_name: name of blob in cloud storage (equivalent to document name on dp object)
            ftp_file_path: ftp file path being read from
        }

        args:
            ftp_file_path - ftp file server path of intended directory to be read from
        """
        self._login()
        bucket_params_list = []
        with self.ftp_connection as ftp:
            files = []
            ftp.cwd(ftp_file_dir)
            ftp.dir(files.append)  # Takes a callback for each file
            sorted_files = Util.order_file_by_datetime(files)
            for file in sorted_files:
                if file.split(".")[-1] == "pdf":
                    file_name = file.split(" ")[-1]
                    blob_name = file.split(" ")[-1].split(".")[0]
                    local_file_path = (
                        f"{os.getcwd()}/assets/pdf/{ftp_file_dir}/{file_name}"
                    )
                    bucket_params_list.append(
                        {
                            "bucket_path": f"{ftp_file_dir}{blob_name}/{file_name}",
                            "local_file_path": local_file_path,
                            "blob_name": blob_name,
                            "ftp_file_path": ftp_file_dir,
                        }
                    )
        self._logout()
        if obj_name:
            for item in bucket_params_list:
                if item["blob_name"] == obj_name:
                    return item
        else:
            return bucket_params_list

    def create_data_processor(self, ftp_file_path: str) -> list:
        """
        method to create data_processor objects from files in shared server
        args:
            ftp_file_path - pickup up folder with pdfs to create object from
        """
        self._login()
        new_obj_list = []
        with self.ftp_connection as ftp:
            files = []
            ftp.cwd(ftp_file_path)
            ftp.dir(files.append)  # Takes a callback for each file
            sorted_files = Util.order_file_by_datetime(files)
            for file in sorted_files:
                file_name = file.split(" ")[-1]
                blob_name = file.split(" ")[-1].split(".")[0]
                source_date = Util.get_datetime_from_file(file)
                cloud_storage_path = ""
                file_path_list = ftp_file_path.split("/")
                folder_name = file_name.split(".")[0]
                for index, file in enumerate(file_path_list):
                    if file == "Documents":
                        cloud_storage_path = "/".join(
                            [*file_path_list[index:-1], folder_name, file_name]
                        )
                    # create new instance row for data_processor and insert into db
                try:
                    new_obj = DataProcessor()
                    new_obj.new_row(
                        source_date=source_date,
                        archive_storage_path=ftp.pwd(),
                        cloud_storage_path=cloud_storage_path,
                        blob_name=blob_name,
                    )
                    new_obj_list.append(new_obj)
                except Exception as error:
                    print("ftp: error creating data object", error)
        self._logout()
        return new_obj_list


ftp_api = FtpServer()
