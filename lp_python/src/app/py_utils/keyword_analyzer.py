"""
keyword analyzer class
"""
import re
import pandas as pd

from app.database import sql_api


class KeywordAnalyzer:
    """
    keyword analyzer functions for ocr text
    messages from class will be labeled KWA:
    """

    def __init__(self) -> None:
        pass

    @staticmethod
    def get_matched_sections(
        text_to_search: str,
        state=None,
        county=None,
        agency=None,
        category=None,
    ) -> None:
        """
        function to get keywords from kw_location_patterns
        """
        columns = [state, county, agency, category]
        existing_row = False
        regex_text = text_to_search.replace("\n", " ")
        if all(columns):
            query_string = "SELECT * FROM `py_landprodata`.`kw_patterns_locations` WHERE State = %s AND County = %s AND Agency = %s AND Category = %s AND Type = %s"
            query_data = (state, county, agency, category, "Section")
            kw_row = sql_api.select_one(query_string, query_data)
            if kw_row:
                existing_row = True
                regex = kw_row["Regex"]
                print("existing row found")
            else:
                print("no existing row found")
                regex = r"(SECTION|SECTIONS|5ECTION|SEC|5EC|SEC\'S|SC) [\s\:\.]* ([ZI\d]+) [\s\:\.]*"
        else:
            regex = r"(SECTION|SECTIONS|5ECTION|SEC|5EC|SEC\'S|SC) [\s\:\.]* ([ZI\d]+) [\s\:\.]*"
            # regex = r"(?:TOWNSHIP|TWP|T|7) [\s\:\.\,\-\_]* ([\/ZIO\d]+) [\s\:\.\,\-\_]* (NOR TH|NORTH|SOUTH|N|S|5) [\s\:\.\,\-\_]* (?:RANGE|RGE|RG|RNG|R) [\s\:\.\,\-\_]* ([\/ZIO\d]+) [\s\:\.\,\-\_]* (WEST|EAST|W|E)"
        matches = re.finditer(regex, regex_text, re.VERBOSE)
        # for match in matches:
        if matches:
            if not existing_row:
                new_row_query = (
                    "INSERT INTO py_landprodata.kw_patterns_locations "
                    "(State, County, Agency, Category, Type, Regex)"
                    "VALUES (%s, %s, %s, %s, %s, %s)"
                )
                new_row_data = (state, county, agency, category, "Section", regex)
                sql_api.insert(new_row_query, new_row_data)
            matches_list = []
            print("KWA: matches found", matches)
            for match_num, match in enumerate(matches, start=1):
                print(
                    "Match {match_num} was found at {start}-{end}: {match}".format(
                        match_num=match_num,
                        start=match.start(),
                        end=match.end(),
                        match=match.group(),
                    )
                )
                matches_list.append(match.group())
                for group_num in range(0, len(match.groups())):
                    group_num = group_num + 1
                    print(
                        "Group {group_num} found at {start}-{end}: {group}".format(
                            group_num=group_num,
                            start=match.start(group_num),
                            end=match.end(group_num),
                            group=match.group(group_num),
                        )
                    )
            matches_series = pd.Series(matches_list)
            matches_json = pd.Series({"section": matches_series}).to_json()
            return {"matches": matches_json, "regex": regex}
        else:
            print("KWA: no matches found")
            return None

    @staticmethod
    def get_matched_township(
        text_to_search: str,
        state=None,
        county=None,
        agency=None,
        category=None,
    ) -> None:
        """
        function to get keywords from kw_location_patterns
        """
        columns = [state, county, agency, category]
        existing_row = False
        regex_text = text_to_search.replace("\n", " ")
        if all(columns):
            query_string = "SELECT * FROM `py_landprodata`.`kw_patterns_locations` WHERE State = %s AND County = %s AND Agency = %s AND Category = %s AND Type = %s"
            query_data = (state, county, agency, category, "Township")
            kw_row = sql_api.select_one(query_string, query_data)
            if kw_row:
                existing_row = True
                regex = kw_row["Regex"]
                print("existing row found")
            else:
                print("no existing row found")
                regex = r"(?:TOWNSHIP|TWP|T|7) [\s\:\.\,\-\_]* ([\/ZIO\d]+) [\s\:\.\,\-\_]* (NOR TH|NORTH|SOUTH|N|S|5) [\s\:\.\,\-\_]* (?:RANGE|RGE|RG|RNG|R) [\s\:\.\,\-\_]* ([\/ZIO\d]+) [\s\:\.\,\-\_]* (WEST|EAST|W|E)"
        else:
            regex = r"(?:TOWNSHIP|TWP|T|7) [\s\:\.\,\-\_]* ([\/ZIO\d]+) [\s\:\.\,\-\_]* (NOR TH|NORTH|SOUTH|N|S|5) [\s\:\.\,\-\_]* (?:RANGE|RGE|RG|RNG|R) [\s\:\.\,\-\_]* ([\/ZIO\d]+) [\s\:\.\,\-\_]* (WEST|EAST|W|E)"
        matches = re.finditer(regex, regex_text, re.VERBOSE)
        # for match in matches:
        if matches:
            if not existing_row:
                new_row_query = (
                    "INSERT INTO py_landprodata.kw_patterns_locations "
                    "(State, County, Agency, Category, Type, Regex)"
                    "VALUES (%s, %s, %s, %s, %s, %s)"
                )
                new_row_data = (state, county, agency, category, "Township", regex)
                sql_api.insert(new_row_query, new_row_data)
            matches_list = []
            print("KWA: matches found", matches)
            for match_num, match in enumerate(matches, start=1):
                print(
                    "Match {match_num} was found at {start}-{end}: {match}".format(
                        match_num=match_num,
                        start=match.start(),
                        end=match.end(),
                        match=match.group(),
                    )
                )
                matches_list.append(match.group())
                for group_num in range(0, len(match.groups())):
                    group_num = group_num + 1
                    print(
                        "Group {group_num} found at {start}-{end}: {group}".format(
                            group_num=group_num,
                            start=match.start(group_num),
                            end=match.end(group_num),
                            group=match.group(group_num),
                        )
                    )
            matches_series = pd.Series(matches_list)
            matches_json = pd.Series({"tonwship": matches_series}).to_json()
            return {"matches": matches_json, "regex": regex}
        else:
            print("KWA: no matches found")
            return None
