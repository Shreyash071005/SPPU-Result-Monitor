from datetime import datetime, timedelta

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

        results = history_manager.get_latest_results()

        html_content = self.generate_html(
            results
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
    # GENERATE HTML
    # ==========================================================

    def generate_html(
            self,
            results,
    ):

        india_timezone = pytz.timezone(
            "Asia/Kolkata"
        )

        last_checked = datetime.now(
            india_timezone
        )

        next_run = (
                last_checked +
                timedelta(minutes=5)
        )

        last_checked_str = (
            last_checked.strftime(
                "%d %B %Y %I:%M:%S %p IST"
            )
        )

        next_run_str = (
            next_run.strftime(
                "%d %B %Y %I:%M:%S %p IST"
            )
        )

        total_results = len(results)

        # ------------------------------------------------------
        # LATEST RESULT
        # ------------------------------------------------------

        latest_result_html = ""

        if results:

            latest = results[-1]

            latest_result_html = f"""
            <div class="latest-result">

                <h3>{latest["title"]}</h3>

                <p>
                <b>Academic Year :</b>
                {latest["year"]}
                </p>

                <p>
                <b>Credit Pattern :</b>
                {latest["pattern"]}
                </p>

                <p>
                <b>Declared On :</b>
                {latest["result_date"]}
                </p>

            </div>
            """

        # ------------------------------------------------------
        # DECLARED RESULT CARDS
        # ------------------------------------------------------

        result_cards = ""

        for result in reversed(results):

            result_cards += f"""

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

        # ------------------------------------------------------
        # HTML
        # ------------------------------------------------------

        return f"""

<!DOCTYPE html>

<html>

<head>

<meta charset="UTF-8">

<meta name="viewport"
content="width=device-width, initial-scale=1.0">

<title>
{WEBSITE_NAME}
</title>

<link rel="stylesheet"
href="style.css">

</head>

<body>

<div class="container">

<h1>
{WEBSITE_NAME}
</h1>


<div class="status-box">

<h2>
Monitoring Status
</h2>

<p class="active-status">
● ACTIVE
</p>

</div>


<div class="info-box">

<h2>
Last Monitoring Run
</h2>

<p>
{last_checked_str}
</p>

</div>


<div class="info-box">

<h2>
Next Monitoring Run
</h2>

<p>
{next_run_str}
</p>

</div>


<div class="info-box">

<h2>
Monitoring Frequency
</h2>

<p>
Every 5 Minutes
</p>

</div>


<div class="info-box">

<h2>
Total Results Stored
</h2>

<p>
{total_results}
</p>

</div>


<h2>
Latest Declared Result
</h2>

{latest_result_html}


<h2>
Declared Results
</h2>

{result_cards}


<div class="official-link">

<h2>
Official SPPU Result Dashboard
</h2>

<a href="{RESULT_DASHBOARD_URL}"
target="_blank">

Visit Official Website

</a>

</div>


<div class="system-info">

<h2>
System Information
</h2>

<p>
Hosting : GitHub Pages
</p>

<p>
Automation : GitHub Actions
</p>

<p>
Backend : Python 3.12
</p>

<p>
Monitoring : 24 x 7
</p>

</div>


<div class="footer">

<p>
Powered By
</p>

<p>
Python + GitHub Actions + GitHub Pages
</p>

</div>

</div>

</body>

</html>

"""