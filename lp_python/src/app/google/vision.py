"""
module for google vision functionality
this uses the key credentials from the google cloud console landpro-server service account
"""
import os
import re

from google.cloud import vision
from app.google.storage import storage_api
from app.py_utils import Util

project_id = os.getcwd() + "/key.json"
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = project_id


class GoogleVision:
    """
    class that will handle googlevision api functionality
    messages from this class will be labeled GV:
    """

    MIME_TYPE = "application/pdf"
    FEATURE = vision.Feature(type_=vision.Feature.Type.DOCUMENT_TEXT_DETECTION)
    BATCH_SIZE = 1

    def __init__(self) -> None:
        self.vision_client = vision.ImageAnnotatorClient()

    def detect_text(self, ftp_file_path: str, files: list or dict) -> dict:
        """
        google function for pdf text detections
        see https://cloud.google.com/vision/docs/pdf for more details
        """
        results = []
        if isinstance(files, list):
            for file in files:
                if file:
                    blob_name = file["blob_name"]
                    ftp_file_path = file["ftp_file_path"]
                    file_uri = Util.get_blob_uri(blob_name, file["ftp_file_path"])
                    try:
                        gcs_source = vision.GcsSource(uri=file_uri)
                        input_config = vision.InputConfig(
                            gcs_source=gcs_source, mime_type=self.MIME_TYPE
                        )
                        gcs_destination_uri = (
                            f"gs://py_landpro/{ftp_file_path}{blob_name}/"
                        )
                        gcs_destination = vision.GcsDestination(uri=gcs_destination_uri)
                        output_config = vision.OutputConfig(
                            gcs_destination=gcs_destination, batch_size=self.BATCH_SIZE
                        )
                        async_request = vision.AsyncAnnotateFileRequest(
                            features=[self.FEATURE],
                            input_config=input_config,
                            output_config=output_config,
                        )
                        operation = self.vision_client.async_batch_annotate_files(
                            requests=[async_request]
                        )
                        print("GV: Waiting for the detection operation to finish.")
                        operation.result(timeout=2000)

                        # Once the request has completed and the output has been
                        # written to GCS, we can list all the output files.
                        storage_client = storage_api.client

                        match = re.match(r"gs://([^/]+)/(.+)", gcs_destination_uri)
                        bucket_name = match.group(1)
                        prefix = match.group(2)

                        bucket = storage_client.get_bucket(bucket_name)

                        # List objects with the given prefix, filtering out folders.
                        blob_list = [
                            blob
                            for blob in list(bucket.list_blobs(prefix=prefix))
                            if not blob.name.endswith("/")
                        ]
                        # pull json files out of response and upload them to db in text location field
                        document_text_list = []
                        for blob in blob_list:
                            if blob.name.split(".")[1] == "json":
                                document_text_list.append(blob.name)
                        print("GV: detection finished for", blob_name)
                        results.append(
                            {"blob_name": blob_name, "documents": document_text_list}
                        )
                    except Exception as error:
                        print(
                            "GV: error in text detection", error, "for file", blob_name
                        )
        return results


vision_api = GoogleVision()
