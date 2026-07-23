from datetime import datetime

import pytz

from services.dashboard_parser import (
    DashboardParser,
)

from services.history_manager import (
    HistoryManager,
)

from services.email_service import (
    EmailService,
)

from services.website_generator import (
    WebsiteGenerator,
)


# ==========================================================
# CONSOLE LOGGER
# ==========================================================

def print_banner():

    print("\n")

    print("=" * 70)

    print(
        "SPPU RESULT MONITOR".center(70)
    )

    print("=" * 70)

    print()


def info(message):

    print(
        f"[INFO] {message}"
    )


def success(message):

    print(
        f"[SUCCESS] {message}"
    )


def warning(message):

    print(
        f"[WARNING] {message}"
    )


def error(message):

    print(
        f"[ERROR] {message}"
    )


def print_current_time():

    india_timezone = pytz.timezone(
        "Asia/Kolkata"
    )

    current_time = (

        datetime.now(
            india_timezone
        ).strftime(
            "%d %B %Y %I:%M:%S %p"
        )

    )

    print(
        f"Current Time : {current_time}"
    )

    print()


# ==========================================================
# FIRST DEPLOYMENT CHECK
# ==========================================================

def is_first_deployment():

    history_manager = HistoryManager()

    history = history_manager.load_history()

    return len(
        history.get(
            "declared_results",
            []
        )
    ) == 0


# ==========================================================
# MAIN MONITORING PIPELINE
# ==========================================================

def monitor_results():

    print_banner()

    print_current_time()

    parser = DashboardParser()

    history_manager = HistoryManager()

    email_service = EmailService()

    website_generator = WebsiteGenerator()

    # ------------------------------------------------------
    # FETCH DASHBOARD
    # ------------------------------------------------------

    info(
        "Fetching SPPU Result Dashboard..."
    )

    try:

        results = (
            parser.get_all_results()
        )

        success(
            "Dashboard Fetched Successfully."
        )

    except Exception as exception:

        error(
            f"Failed to fetch dashboard."
        )

        error(
            str(exception)
        )

        return

    print()

    info(
        f"Engineering Results Found : {len(results)}"
    )

    print()

    # ------------------------------------------------------
    # NO RESULTS FOUND
    # ------------------------------------------------------

    if not results:

        warning(
            "No Engineering Results Found."
        )

        try:

            website_generator.generate_website()

        except Exception:
            pass

        return

    # ------------------------------------------------------
    # FIRST DEPLOYMENT LOGIC
    # ------------------------------------------------------

    first_deployment = (
        is_first_deployment()
    )

    if first_deployment:

        warning(
            "FIRST DEPLOYMENT DETECTED."
        )

        warning(
            "Existing results will be stored."
        )

        warning(
            "No email notifications will be sent."
        )

        print()

    # ------------------------------------------------------
    # PROCESS RESULTS
    # ------------------------------------------------------

    for result in results:

        print("-" * 70)

        print()

        print(
            f"Title : {result['title']}"
        )

        print()

        print(
            f"Result Date : {result['result_date']}"
        )

        print()

        # --------------------------------------------------
        # RESULT ALREADY EXISTS
        # --------------------------------------------------

        if history_manager.result_exists(
                result
        ):

            warning(
                "Result Already Exists."
            )

            print()

            continue

        # --------------------------------------------------
        # NEW RESULT FOUND
        # --------------------------------------------------

        success(
            "NEW RESULT DECLARED."
        )

        print()

        # --------------------------------------------------
        # SAVE RESULT HISTORY
        # --------------------------------------------------

        try:

            history_manager.add_result(
                result
            )

            success(
                "Result History Updated."
            )

        except Exception as exception:

            error(
                str(exception)
            )

        # --------------------------------------------------
        # UPDATE WEBSITE RESULTS
        # --------------------------------------------------

        try:

            history_manager.update_latest_results(
                result
            )

            success(
                "Latest Results Updated."
            )

        except Exception as exception:

            error(
                str(exception)
            )

        # --------------------------------------------------
        # FIRST DEPLOYMENT
        # --------------------------------------------------

        if first_deployment:

            continue

        # --------------------------------------------------
        # SEND EMAIL NOTIFICATION
        # --------------------------------------------------

        info(
            "Sending Email Notification..."
        )

        try:

            email_service.send_new_result_email(
                result
            )

            success(
                "Email Sent Successfully."
            )

        except Exception as exception:

            error(
                "Email Notification Failed."
            )

            error(
                str(exception)
            )

        print()

    # ------------------------------------------------------
    # GENERATE WEBSITE
    # ------------------------------------------------------

    print()

    info(
        "Generating Website..."
    )

    try:

        website_generator.generate_website()

        success(
            "Website Generated Successfully."
        )

    except Exception as exception:

        error(
            "Website Generation Failed."
        )

        error(
            str(exception)
        )

    # ------------------------------------------------------
    # COMPLETED
    # ------------------------------------------------------

    print()

    print("=" * 70)

    success(
        "Monitoring Completed Successfully."
    )

    print("=" * 70)

    print()


# ==========================================================
# MAIN
# ==========================================================

if __name__ == "__main__":

    try:

        monitor_results()

    except KeyboardInterrupt:

        print()

        warning(
            "Monitoring Stopped by User."
        )

        print()

    except Exception as exception:

        print()

        error(
            "Unexpected Error Occurred."
        )

        error(
            str(exception)
        )

        print()