import json

from config import (
    RESULT_HISTORY_FILE,
    LATEST_RESULTS_FILE,
)


class HistoryManager:

    # ==========================================================
    # LOAD RESULT HISTORY
    # ==========================================================

    def load_history(self):

        try:

            with open(

                    RESULT_HISTORY_FILE,

                    "r",

                    encoding="utf-8",

            ) as file:

                return json.load(file)

        except FileNotFoundError:

            return {

                "declared_results": []

            }

    # ==========================================================
    # SAVE RESULT HISTORY
    # ==========================================================

    def save_history(

            self,

            data,

    ):

        with open(

                RESULT_HISTORY_FILE,

                "w",

                encoding="utf-8",

        ) as file:

            json.dump(

                data,

                file,

                indent=4,

                ensure_ascii=False,

            )

    # ==========================================================
    # CHECK RESULT EXISTS
    # ==========================================================

    def result_exists(

            self,

            result,

    ):

        history = self.load_history()

        for stored_result in (

                history[
                    "declared_results"
                ]

        ):

            if (

                    stored_result["year"]

                    ==

                    result["year"]

                    and

                    stored_result["pattern"]

                    ==

                    result["pattern"]

                    and

                    stored_result["result_date"]

                    ==

                    result["result_date"]

            ):

                return True

        return False

    # ==========================================================
    # ADD NEW RESULT
    # ==========================================================

    def add_result(

            self,

            result,

    ):

        history = self.load_history()

        history[

            "declared_results"

        ].append(

            result

        )

        self.save_history(

            history

        )

    # ==========================================================
    # LOAD LATEST RESULTS
    # ==========================================================

    def load_latest_results(self):

        try:

            with open(

                    LATEST_RESULTS_FILE,

                    "r",

                    encoding="utf-8",

            ) as file:

                return json.load(file)

        except FileNotFoundError:

            return {

                "latest_results": []

            }

    # ==========================================================
    # SAVE LATEST RESULTS
    # ==========================================================

    def save_latest_results(

            self,

            data,

    ):

        with open(

                LATEST_RESULTS_FILE,

                "w",

                encoding="utf-8",

        ) as file:

            json.dump(

                data,

                file,

                indent=4,

                ensure_ascii=False,

            )

    # ==========================================================
    # UPDATE LATEST RESULTS
    # ==========================================================

    def update_latest_results(

            self,

            result,

    ):

        latest_results = (

            self.load_latest_results()

        )

        latest_results[

            "latest_results"

        ].append(

            result

        )

        self.save_latest_results(

            latest_results

        )

    # ==========================================================
    # GET LATEST RESULTS
    # ==========================================================

    def get_latest_results(self):

        data = (

            self.load_latest_results()

        )

        return data.get(

            "latest_results",

            []

        )