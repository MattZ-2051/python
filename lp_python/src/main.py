"""
main script file
"""
import pandas as pd
import json

from app.ftp import ftp_api
from app.py_utils import Util
from app.google import storage_api
from app.google import vision_api
from app.models import DataProcessor
from app.py_utils import KeywordAnalyzer


ftp_file_path = (
    "LPD Archive/US States/Idaho/Counties/Ada/Ada County/Documents/Subdivisions/"
)


def prepare_files_for_upload():
    Util.create_local_directory(ftp_file_path)
    ftp_api.download_files(ftp_file_path)


def create_dp_object_from_server():
    files = ftp_api.get_pdf_files_from_path(ftp_file_path)
    for file in files[:100]:
        dp_obj = DataProcessor()
        new_obj = dp_obj.create_new_obj_from_file(file, ftp_file_path)
        if new_obj:
            google_bucket_params = ftp_api.get_bucket_info(
                ftp_file_path, new_obj.document_name
            )
            if len(google_bucket_params) >= 1:
                storage_api.upload_to_bucket(google_bucket_params)
                vision_results = vision_api.detect_text(
                    ftp_file_path, [google_bucket_params]
                )
                if len(vision_results) >= 1:
                    for result in vision_results:
                        dp_obj.update_text_location(
                            result["blob_name"],
                            pd.Series(result["documents"]).to_json(),
                        )
                    text_location = json.loads(dp_obj.text_location)
                    text_list = []
                    for file in text_location:
                        res = storage_api.get_ocr_result(text_location[file])
                        text_list.append(res)
                    text_to_search = "/n".join(text_list)
                    section_keywords = KeywordAnalyzer.get_matched_sections(
                        text_to_search=text_to_search,
                        state=dp_obj.state,
                        agency=dp_obj.source,
                        county=dp_obj.county,
                        category=dp_obj.category,
                    )
                    dp_obj.update_keywords(section_keywords)
                    township_keywords = KeywordAnalyzer.get_matched_township(
                        text_to_search=text_to_search,
                        state=dp_obj.state,
                        agency=dp_obj.source,
                        county=dp_obj.county,
                        category=dp_obj.category,
                    )
                    dp_obj.update_keywords(township_keywords)


prepare_files_for_upload()
create_dp_object_from_server()
