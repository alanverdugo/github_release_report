#!/usr/bin/env python
"""
A humble script to build a humble report about Github releases in an organization.

Usage: report_releases.py [-h] [-v]
            -s START_DATE
            -e END_DATE
            -o ORG
            -u USER
            -t TOKEN
            -a API_URL

Optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose         Print INFO, WARNING, and ERROR messages to the stdout
                        or stderr.
  -s START_DATE, --start-date START_DATE
                        Start date for range (YYYY-MM-DD).
  -e END_DATE, --end-date END_DATE
                        End date for range (YYYY-MM-DD).
  -o ORG, --organization ORG
                        Github user
  -u USER, --user USER  Github user
  -t TOKEN, --token TOKEN
                        Github token
  -a API_URL, --api_url API_URL
                        URL of the Github API
"""
import os
import argparse
import datetime
import logging
import requests
import pandas


# Logging configuration and local env vars.
LOG = logging.getLogger()

HEADERS = {
    'Accept': 'application/vnd.github.v3+json'
}

PARAMS = {
    'filter': 'all',
    'state': 'all',
    'per_page': 100
}

# Get the full path where this program exist.
DIR_PATH = os.path.dirname(os.path.realpath(__file__))


def main():
    """Drive program flow."""
    args = parse_args()

    # Authenticate.
    auth = requests.auth.HTTPBasicAuth(args["user"], args["token"])

    # Get the list of repositories in the organization.
    LOG.info("Getting repositories in the %s organization...", args["org"])
    repo_urls = f"{args['api_url']}/orgs/{args['org']}/repos"
    # Execute get request.
    response = requests.get(repo_urls,
                            headers=HEADERS,
                            params=PARAMS,
                            auth=auth)
    # Parse response.
    parsed_response = response.json()

    # Put all the repository names in a list.
    repo_list = [repo["name"] for repo in parsed_response]

    # Build a dataframe with the releases data.
    get_releases(repo_list=repo_list, args=args, auth=auth)


def get_releases(repo_list: list,
                 args: dict,
                 auth: requests.auth.HTTPBasicAuth):
    """
    Get release data from the releases endpoint and add it to a dataframe.

    :param repo_list: A list containing the name of the repositories in the org.
    :param args: A dictionary containing the CLI arguments.
    :param auth: The requests authentication object.
    :returns df_releases: A Pandas DataFrame with GitHub releases data.
    """
    # Get data for each repository.
    release_url_list = []
    for repo in repo_list:
        # Get a list of releases URLs.
        release_url_list.append(f"{args['api_url']}/repos/{args['org']}/{repo}/releases")

    # The list of column names that will be used in the dataframe and final
    # report(s).
    columns = ["DATE (UTC)", "AUTHOR", "TAG", "REPOSITORY", "NAME", "URL"]

    # Create a dataframe to manage the data.
    df_releases = pandas.DataFrame(columns=columns)

    # Get data for releases.
    LOG.info("Getting releases in the %s organization...", args["org"])
    for release_url in release_url_list:
        # Execute get request.
        response = requests.get(release_url,
                                headers=HEADERS,
                                params=PARAMS,
                                auth=auth)
        # Add the data to a pandas dataframe.
        for release in response.json():
            df_releases = \
                df_releases.append({columns[0]: release["published_at"],
                                    columns[1]: release["author"]["login"],
                                    columns[2]: release["tag_name"],
                                    columns[3]: release["url"].split("/")[7],
                                    columns[4]: release["name"],
                                    columns[5]: release["html_url"]},
                                   ignore_index=True)

    # Convert the DATE column to datetime.
    df_releases[columns[0]] = pandas.to_datetime(df_releases[columns[0]])
    start_date = pandas.to_datetime(args["start_date"], format="%Y-%m-%d")
    end_date = pandas.to_datetime(args["end_date"], format="%Y-%m-%d")

    # Change timezone.
    #df_releases["DATE (UTC)"] = df_releases["DATE (UTC)"].dt.tz_convert()

    # Remove timezone information from the DATE column.
    df_releases[columns[0]] = \
        df_releases[columns[0]].dt.strftime("%Y-%m-%d %H:%M:%S")
    # Convert back to datetime.
    df_releases[columns[0]] = pandas.to_datetime(df_releases["DATE (UTC)"])

    # Filter for the specified period.
    df_releases = df_releases[(df_releases[columns[0]] > start_date) &
                              (df_releases[columns[0]] < end_date)]

    # Order datafame (by descending date).
    df_releases = df_releases.sort_values(by=[columns[0]], ascending=True)

    # Save the data into .csv and .xlsx files.
    save_output_files(df_releases, start_date, end_date)


def save_output_files(df_releases: pandas.DataFrame,
                      start_date, end_date):
    """
    Create the output files (with the data in them).

    :param
    :param
    :param
    """
    LOG.debug("Type of start_date: %s", type(start_date))
    LOG.debug("Type of end_date: %s", type(end_date))

    filename = f"releases_{start_date.strftime('%Y-%m-%d')}_{end_date.strftime('%Y-%m-%d')}"

    # Save data to .csv
    csv_abs_filename = os.path.join(DIR_PATH, filename + ".csv")
    LOG.info("Saving data to %s", csv_abs_filename)
    df_releases.to_csv(csv_abs_filename,
                       index=False,
                       sep="|",
                       encoding="utf-8")

    # Save data to .xlsx
    xlsx_abs_filename = os.path.join(DIR_PATH, filename + ".xlsx")
    LOG.info("Saving data to %s", xlsx_abs_filename)
    df_releases.to_excel(xlsx_abs_filename,
                         index=None,
                         header=True,
                         encoding="utf-8")


def parse_args():  # pragma: no cover
    """
    Get, validate and parse arguments.

    :returns: A dictionary containing the parsed arguments.
    """
    parser = argparse.ArgumentParser()
    # Log level parameters.
    parser.add_argument("-v",
                        "--verbose",
                        help="Print INFO, WARNING, and ERROR messages "
                        "to the stdout or stderr.",
                        dest="verbose",
                        default=False,
                        action="store_true")
    parser.add_argument("-d",
                        "--debug",
                        help="Print DEBUG messages to the stdout or stderr.",
                        dest="debug",
                        default=False,
                        action="store_true")
    parser.add_argument("-s",
                        "--start-date",
                        help="Start date for range (YYYY-MM-DD).",
                        dest="start_date",
                        # Validate that the user's value is a valid date.
                        type=datetime.date.fromisoformat,
                        required=True)
    parser.add_argument("-e",
                        "--end-date",
                        help="End date for range (YYYY-MM-DD).",
                        dest="end_date",
                        # Validate that the user's value is a valid date.
                        type=datetime.date.fromisoformat,
                        required=True)
    parser.add_argument("-o",
                        "--organization",
                        help="Github user",
                        dest="org",
                        type=str,
                        required=True)
    parser.add_argument("-u",
                        "--user",
                        help="Github user",
                        dest="user",
                        type=str,
                        required=True)
    parser.add_argument("-t",
                        "--token",
                        help="Github token",
                        dest="token",
                        type=str,
                        required=True)
    parser.add_argument("-a",
                        "--api_url",
                        help="URL of the Github API",
                        dest="api_url",
                        default="https://api.github.com",
                        type=str,
                        required=False)
    args = vars(parser.parse_args())

    # Set logging level.
    if args["verbose"]:
        LOG.setLevel(logging.INFO)
    elif args["debug"]:
        LOG.setLevel(logging.DEBUG)

    return args


if __name__ == '__main__':  # pragma: no cover
    # Stream handler for human consumption and stderr.
    STREAM_HANDLER = logging.StreamHandler()
    STREAM_FORMATTER = logging.Formatter("%(asctime)s - "
                                         "%(levelname)s - "
                                         "%(message)s")

    STREAM_HANDLER.setFormatter(STREAM_FORMATTER)
    LOG.addHandler(STREAM_HANDLER)

    main()
