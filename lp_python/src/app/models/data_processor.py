"""
this module defined the class for LPD data object class
all other classes will extend this class
"""
from datetime import datetime
import json
from app.database import sql_api
from app.py_utils import Util


class DataProcessor:
    """
    other data objects will inherit this class
    the vars defined in this class will be apart of every other model
    messages from this class will be labeled Model_dp:
    """

    def __init__(self, feat_id: str = None) -> None:
        # feature_id auto incremented field in mysql
        self.feat_id = feat_id
        self.state = None  # required - state that data belongs to
        self.county = None  # required - county that data belongs to
        self.category = (
            None  # required - category that relates to data (ex: Subdivisions)
        )
        self.source = None  # required - name of source that data came from
        self.source_date = None  # required - date that source data was created
        self.text_location = None  # location of json text file belonging to ocr result
        self.document_name = None  # name of document file as seen on ftp server
        self.entered_by = "py-script"  # user that create entry
        self.entered_date = datetime.now()  # date that data was entered
        self.shape = "POINT(1 1)"
        self.processed = False
        self.archive_storage_path = None
        self.cloud_storage_path = None
        self.instrument = None
        self.original_create_date = None
        self.updated_by = None
        self.updated_date = None
        self.processed = False
        self.lpd_comments = None
        self.keywords = None
        self.located_by = None

        if feat_id:
            self._get_existing_object(feat_id)

    def _get_existing_object(self, feat_id: str) -> None:
        query_string = "SELECT * FROM py_landprodata.data_processor WHERE `FeatId` = %s"
        query_data = tuple(feat_id)
        result = sql_api.select_one(query_string, query_data)
        if result:
            self.feat_id = result["FeatId"]
            self.state = result["State"]
            self.county = result["County"]
            self.shape = result["SHAPE"]
            self.category = result["Category"]
            self.source = result["Source"]
            self.source_date = result["Source Date"]
            self.instrument = result["Instrument"]
            self.original_create_date = result["Original Create Date"]
            self.text_location = result["Text Location"]
            self.document_name = result["Document Name"]
            self.entered_by = result["Entered By"]
            self.entered_date = result["Entered Date"]
            self.updated_by = result["Updated By"]
            self.updated_date = result["Updated Date"]
            self.processed = result["Processed"]
            self.archive_storage_path = result["Archive Storage Path"]
            self.lpd_comments = result["landproDATA comments"]
            self.keywords = result["keywords"]
            self.located_by = result["located_by"]
            print("Model_dp: existing row found for", feat_id)

    def update_text_location(self, document_name, text_location) -> None:
        """
        method to update text location attribute that will be called in google text detection
        args:
            document_name - name of file without .pdf attached
        """
        row_query = "UPDATE py_landprodata.data_processor SET `Text Location` = %s WHERE `Document Name` = %s"
        row_data = (text_location, document_name)
        sql_api.insert(row_query, row_data)
        self.text_location = text_location

    def _check_if_row_exists(self) -> bool:
        """
        private method to check if row already exists to prevent duplicates of objects
        """
        query_string = "SELECT * FROM py_landprodata.data_processor WHERE Category = %s AND State = %s AND County = %s AND `Document Name` = %s"
        query_data = (self.category, self.state, self.county, self.document_name)
        return sql_api.check_if_object_exists(query_string, query_data)

    def update_keywords(self, new_keywords):
        """
        function to update keywords for a existing dp object
        args:
            new_keywords - json string of new keywords to be added
        """
        query_string = "SELECT * FROM py_landprodata.data_processor WHERE `FeatId` = %s"
        query_data = [str(self.feat_id)]
        result = sql_api.select_one(query_string, query_data)
        if result is not None:
            if bool(result.get("keywords")):
                existing_keywords = json.loads(result["keywords"])
            else:
                existing_keywords = json.loads("{}")
        else:
            existing_keywords = json.loads("{}")
        new_words = json.loads(new_keywords["matches"])
        kw_json = json.dumps({**existing_keywords, **new_words})
        row_query = "UPDATE py_landprodata.data_processor SET `keywords` = %s WHERE `FeatId` = %s"
        row_data = (kw_json, self.feat_id)
        sql_api.insert(row_query, row_data)

    def new_row(
        self,
        source_date: str,
        archive_storage_path: str,
        cloud_storage_path: str,
        blob_name: str,
    ) -> None:
        """
        method for inserting new row into data_processor table when new instance is created
        """
        self.source_date = source_date
        self.archive_storage_path = archive_storage_path
        self.cloud_storage_path = cloud_storage_path
        self.document_name = blob_name
        directory_array = archive_storage_path.split("/")
        for index, folder in enumerate(directory_array):
            if folder == "US States":
                self.state = directory_array[index + 1]
            if folder == "Counties":
                self.county = directory_array[index + 1]
                self.source = directory_array[index + 2]
            if folder == "Documents":
                self.category = directory_array[index + 1]
        required_values = [
            self.state,
            self.county,
            self.category,
            self.source_date,
            self.archive_storage_path,
            self.cloud_storage_path,
            self.document_name,
        ]
        if not all(required_values):
            print("Model_dp: all required values must be set")
            return

        if not self._check_if_row_exists():
            row_query = (
                "INSERT INTO py_landprodata.data_processor "
                "(State, County, SHAPE, Category, Source, `Source Date`, `Text Location`, `Document Name`, `Entered By`, `Entered Date`, Processed, `Archive Storage Path`, `Cloud Storage Path`) "
                "VALUES (%s, %s, ST_GeomFromText(%s), %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            )
            row_data = (
                self.state,
                self.county,
                self.shape,
                self.category,
                self.source,
                self.source_date,
                self.text_location,
                self.document_name,
                self.entered_by,
                self.entered_date,
                self.processed,
                self.archive_storage_path,
                self.cloud_storage_path,
            )
            self.feat_id = sql_api.insert(row_query, row_data)
            print("Model_dp: New data processor row successfully created")
            return self
        else:
            print("Model_dp: Row already exists for this data")
            return None

    def create_new_obj_from_file(self, file: str, ftp_file_path: str):
        """
        method to create object from a given file
        """
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
            return self.new_row(
                source_date=source_date,
                archive_storage_path=ftp_file_path,
                cloud_storage_path=cloud_storage_path,
                blob_name=blob_name,
            )
        except Exception as error:
            print("ftp: error creating data object", error)
