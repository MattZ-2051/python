"""
module for google storage functionality
this uses the key credentials from the google cloud console landpro-server service account
"""
import os
import json

from google.cloud import storage

project_id = os.getcwd() + "/key.json"
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = project_id


class GoogleCloud:
    """
    class that contains googel cloud functions
    that will upload pdfs to cloud db
    messages from this class will be labeled GC:
    """

    def __init__(self) -> None:
        self.client = storage.Client.from_service_account_json(project_id)
        self.bucket = self.client.get_bucket("py_landpro")

    def _upload(self, blob, local_file_path):
        """
        private class method for upload to bucket
        args:
            bucket_path - path to new bucket
            local_file_path - path to local file
        """
        try:
            blob.upload_from_filename(local_file_path, content_type="application/pdf")
            print("GC: file successfully uploaded to bucket")
        except Exception as error:
            print("GC: error uploading file to bucket", error)

    def upload_to_bucket(self, bucket_params: dict or list) -> list:
        """
        Upload data to py_landpro dv and return pathname

        args:
            bucket_params -
            KEYS
            bucket_path - name of object when stored in google cloud
            path names can be included in this as well
            ex:
            .../Idaho/Counties/Ada/Ada County/Documents/Subdivisions/S00102/S00102.pdf

            local_file_path: pathname of file you want to upload from local directory
        """
        bucket = self.bucket
        if isinstance(bucket_params, list):
            for params in bucket_params:
                blob = bucket.blob(params["bucket_path"])
                local_file_path = params["local_file_path"]
                self._upload(blob, local_file_path)

        if isinstance(bucket_params, dict):
            blob = bucket.blob(bucket_params["bucket_path"])
            local_file_path = bucket_params["local_file_path"]
            self._upload(blob, local_file_path)

    def get_ocr_result(self, blob_path) -> str:
        """
        function for getting ocr text from object path in google cloud

        args:
            blob_path - pathname of json file from ocr result in google cloud
            bucket

        """
        bucket = self.bucket
        blob = bucket.blob(blob_path)
        content = blob.download_as_string()
        response = json.loads(content)
        text_list = []
        for res in response["responses"]:
            annotation = res["fullTextAnnotation"]
            text_list.append(annotation["text"])
        return " ".join(text_list)


storage_api = GoogleCloud()
