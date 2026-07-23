from datetime import datetime

import pytz

from config import (
    INDEX_FILE,
    RESULT_DASHBOARD_URL,
    WEBSITE_NAME,
)

from services.history_manager import (
    HistoryManager,
)


class WebsiteGenerator:

    # ==========================================================
    # GENERATE WEBSITE
    # ==========================================================

    def generate_website(self):

        history_manager = HistoryManager()

        results = (
            history_manager.get_latest_results()
        )

        html_content = (
            self.generate_html(
                results
            )
        )

        with open(

                INDEX_FILE,

                "w",

                encoding="utf-8",

        ) as file:

            file.write(
                html_content
            )

    # ==========================================================
    # GENERATE HTML CONTENT
    # ==========================================================

    def generate_html(

            self,

            results,

    ):

        india_timezone = (
            pytz.timezone(
                "Asia/Kolkata"
            )
        )

        last_checked = (

            datetime.now(
                india_timezone
            ).strftime(
                "%d %B %Y %I:%M:%S %p"
            )

        )

        latest_result_html = ""

        for result in reversed(results):

            latest_result_html += f"""

            <div class="result-card">

                <h3>
                    {result["title"]}
                </h3>

                <p>
                    <b>Academic Year :</b>
                    {result["year"]}
                </p>

                <p>
                    <b>Credit Pattern :</b>
                    {result["pattern"]}
                </p>

                <p>
                    <b>Result Date :</b>
                    {result["result_date"]}
                </p>

            </div>

            """

        return f"""

<!DOCTYPE html>

<html>

<head>

<title>
{WEBSITE_NAME}
</title>

<link
rel="stylesheet"
href="style.css"
>

</head>

<body>

<div class="container">

<h1>
{WEBSITE_NAME}
</h1>

<hr>

<h2>
Monitoring Status
</h2>

<p>
ACTIVE
</p>

<hr>

<h2>
Last Checked
</h2>

<p>
{last_checked}
</p>

<hr>

<h2>
Declared Results
</h2>

{latest_result_html}

<hr>

<h2>
Official SPPU Result Dashboard
</h2>

<a href="{RESULT_DASHBOARD_URL}">
Visit Official Website
</a>

<hr>

<p>
Powered by GitHub Actions
</p>

</div>

</body>

</html>

"""