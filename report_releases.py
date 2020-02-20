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

    auth = requests.auth.HTTPBasicAuth(args["user"], args["token"])

    # Get the list of repositories in the organization.
    LOG.info("Getting repositories in %s", args["org"])
    repo_urls = f"{args['api_url']}/orgs/{args['org']}/repos"
    response = requests.get(repo_urls, headers=HEADERS, params=PARAMS, auth=auth)
    parsed_response = response.json()

    # Put all the repositories in a list.
    repo_list = []
    for repo in parsed_response:
        repo_list.append(repo["name"])

    # Get releases for each repository.
    release_url_list = []
    for repo in repo_list:
        release_url_list.append(f"{args['api_url']}/repos/{args['org']}/{repo}/releases")

    # Create a dataframe to manage the data.
    df_releases = pandas.DataFrame(columns=['DATE (UTC)',
                                            'AUTHOR',
                                            'TAG',
                                            'REPOSITORY',
                                            'NAME',
                                            'URL'])

    # Get data for releases.
    LOG.info("Getting releases in %s", args["org"])
    for release_url in release_url_list:
        response = requests.get(release_url,
                                headers=HEADERS,
                                params=PARAMS,
                                auth=auth)

        for release in response.json():
            df_releases = \
                df_releases.append({'DATE (UTC)': release["published_at"],
                                    'AUTHOR': release["author"]["login"],
                                    'TAG': release["tag_name"],
                                    'REPOSITORY': release["url"].split("/")[7],
                                    'NAME': release["name"],
                                    'URL': release["html_url"]}, ignore_index=True)

    # Convert the DATE column to datetime.
    df_releases['DATE (UTC)'] = pandas.to_datetime(df_releases["DATE (UTC)"])
    start_date = pandas.to_datetime(args["start_date"], format="%Y-%m-%d")
    end_date = pandas.to_datetime(args["end_date"], format="%Y-%m-%d")

    # Remove timezone information from the DATE column.
    df_releases["DATE (UTC)"] = df_releases["DATE (UTC)"].dt.strftime("%Y-%m-%d %H:%M:%S")
    # Convert back to datetime.
    df_releases['DATE (UTC)'] = pandas.to_datetime(df_releases["DATE (UTC)"])

    # Filter for the specified period.
    df_releases = df_releases[(df_releases['DATE (UTC)'] > start_date) &
                              (df_releases['DATE (UTC)'] < end_date)]

    # Order datafame (descending date).
    df_releases = df_releases.sort_values(by=['DATE (UTC)'], ascending=True)
    LOG.debug(df_releases)

    save_output_files(df_releases, start_date, end_date)


def save_output_files(df_releases: pandas.DataFrame,
                      start_date, end_date):
    """Create the output files with the data in them."""
    LOG.debug("Type of start_date: %s", type(start_date))
    LOG.debug("Type of end_date: %s", type(end_date))
    filename = f"releases_{start_date.strftime('%Y-%m-%d')}_{end_date.strftime('%Y-%m-%d')}"
    # Create the absolute path of the resultant file.
    csv_abs_filename = os.path.join(DIR_PATH, filename + ".csv")
    LOG.info("Saving data to %s", csv_abs_filename)
    # Save data to .csv
    df_releases.to_csv(csv_abs_filename,
                       index=False,
                       sep="|",
                       encoding="utf-8")

    xlsx_abs_filename = os.path.join(DIR_PATH, filename + ".xlsx")
    LOG.info("Saving data to %s", xlsx_abs_filename)
    # Save data to .xlsx
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
    parser.add_argument("-d", "--debug",
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
                        required=True)
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
