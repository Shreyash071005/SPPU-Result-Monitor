import re

import requests
from bs4 import BeautifulSoup

from config import (
    RESULT_DASHBOARD_URL,
    REQUEST_TIMEOUT,
)


class DashboardParser:

    # ==========================================================
    # FETCH DASHBOARD HTML
    # ==========================================================

    def fetch_dashboard(self):

        response = requests.get(

            RESULT_DASHBOARD_URL,

            timeout=REQUEST_TIMEOUT,

        )

        response.raise_for_status()

        return response.text

    # ==========================================================
    # EXTRACT ACADEMIC YEAR
    # ==========================================================

    @staticmethod
    def extract_year(

            title,

    ):

        title = title.upper()

        if "F.E." in title:
            return "FE"

        if "S.E." in title:
            return "SE"

        if "T.E." in title:
            return "TE"

        if "B.E." in title:
            return "BE"

        return None

    # ==========================================================
    # EXTRACT CREDIT PATTERN
    # ==========================================================

    @staticmethod
    def extract_pattern(

            title,

    ):

        match = re.search(

            r"\((\d{4})",

            title,

            flags=re.IGNORECASE,

        )

        if match:

            return match.group(1)

        return None

    # ==========================================================
    # CHECK ENGINEERING RESULT
    # ==========================================================

    def is_engineering_result(

            self,

            title,

    ):

        return (

            self.extract_year(
                title
            )

            is not None

        )

    # ==========================================================
    # PARSE DASHBOARD RESULTS
    # ==========================================================

    def get_all_results(self):

        html = self.fetch_dashboard()

        soup = BeautifulSoup(

            html,

            "html.parser",

        )

        rows = soup.find_all(

            "tr"

        )

        results = []

        for row in rows:

            title = row.get_text(

                separator=" ",

                strip=True,

            )

            # --------------------------------------------------
            # ENGINEERING RESULTS ONLY
            # --------------------------------------------------

            if not self.is_engineering_result(
                    title
            ):

                continue

            columns = row.find_all(

                "td"

            )

            if len(columns) < 4:

                continue

            serial_number = (

                columns[0]
                .get_text(
                    strip=True
                )

            )

            result_date = (

                columns[2]
                .get_text(
                    strip=True
                )

            )

            anchor = row.find(

                "a"

            )

            if anchor is None:

                continue

            onclick = anchor.get(

                "onclick",

                "",

            )

            values = (

                onclick
                .replace(
                    "Enterdetails(",
                    "",
                )
                .replace(
                    ")",
                    "",
                )
                .split(",")

            )

            if len(values) < 2:

                continue

            pattern_name = (

                values[0]
                .replace(
                    "'",
                    "",
                )
                .strip()

            )

            pattern_id = (

                values[1]
                .replace(
                    "'",
                    "",
                )
                .strip()

            )

            year = self.extract_year(
                title
            )

            pattern = self.extract_pattern(
                title
            )

            if year is None:

                continue

            if pattern is None:

                continue

            results.append(

                {

                    "title":
                    title,

                    "year":
                    year,

                    "pattern":
                    pattern,

                    "result_date":
                    result_date,

                    "serial_number":
                    serial_number,

                    "pattern_name":
                    pattern_name,

                    "pattern_id":
                    pattern_id,

                }

            )

        return results