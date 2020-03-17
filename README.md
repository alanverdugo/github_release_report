A humble script to build a humble report about Github releases in an organization.

<p align="center">
    <a href="https://www.python.org/">
        <img src="https://img.shields.io/badge/built%20with-Python3-red.svg" />
    </a>
</p>

## Usage:
```bash
python3 report_releases.py [-h] [-v]
        -s START_DATE
        -e END_DATE
        -o ORG
        -u USER
        -t TOKEN
        -a API_URL
```

## Arguments:
```bash
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
```


## Execute with Docker:

A Dockerfile is included in order to make execution easier. Since the entrypoint accepts extra parameters, they can be supplied after the image name in `docker run`. See below for an example:

### Build:
```bash
docker build -t <image_name> .
```

Example:
```bash
docker build -t github_releases .
```

### Run:
```bash
docker run -v /home/alan/git/github_release_report/:/output github_releases \
    -o <ORGANIZATION_NAME> \
    -s <YYYY-MM-DD> \
    -e <YYYY-MM-DD> \
    -u <GITHUB_USERNAME> \
    -t <GITHUB_API_TOKEN> \
    -a <GITHUB_API_URL>
```

Example:
```bash
docker run -v /home/alan/git/github_release_report/:/output github_releases \
    -o MarketingSystems \
    -s 2020-03-02 \
    -e 2020-03-13 \
    -u octocat \
    -t my_g1thub_t0k3n \
    -a https://api.github.com \
    -d
```



## Build status
Type            | Service               | Branch            | Status
---             | ---                   | ---               | ---
CI (Linux)      | Travis                | master            | [![Build Status](https://travis-ci.com/alanverdugo/github_release_report.svg?branch=master)](https://travis-ci.com/alanverdugo/github_release_report)
CI (Linux)      | Travis                | development       | [![Build Status](https://travis-ci.com/alanverdugo/github_release_report.svg?branch=development)](https://travis-ci.com/alanverdugo/github_release_report)


## SonarCloud status

[![SonarCloud](https://sonarcloud.io/images/project_badges/sonarcloud-white.svg)](https://sonarcloud.io/dashboard?id=alanverdugo_github_release_report)

[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=alanverdugo_github_release_report&metric=alert_status)](https://sonarcloud.io/dashboard?id=alanverdugo_github_release_report)

[![Bugs](https://sonarcloud.io/api/project_badges/measure?project=alanverdugo_github_release_report&metric=bugs)](https://sonarcloud.io/dashboard?id=alanverdugo_github_release_report)

[![Code Smells](https://sonarcloud.io/api/project_badges/measure?project=alanverdugo_github_release_report&metric=code_smells)](https://sonarcloud.io/dashboard?id=alanverdugo_github_release_report)

[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=alanverdugo_github_release_report&metric=coverage)](https://sonarcloud.io/dashboard?id=alanverdugo_github_release_report)

[![Duplicated Lines (%)](https://sonarcloud.io/api/project_badges/measure?project=alanverdugo_github_release_report&metric=duplicated_lines_density)](https://sonarcloud.io/dashboard?id=alanverdugo_github_release_report)

[![Lines of Code](https://sonarcloud.io/api/project_badges/measure?project=alanverdugo_github_release_report&metric=ncloc)](https://sonarcloud.io/dashboard?id=alanverdugo_github_release_report)

[![Maintainability Rating](https://sonarcloud.io/api/project_badges/measure?project=alanverdugo_github_release_report&metric=sqale_rating)](https://sonarcloud.io/dashboard?id=alanverdugo_github_release_report)

[![Reliability Rating](https://sonarcloud.io/api/project_badges/measure?project=alanverdugo_github_release_report&metric=reliability_rating)](https://sonarcloud.io/dashboard?id=alanverdugo_github_release_report)

[![Security Rating](https://sonarcloud.io/api/project_badges/measure?project=alanverdugo_github_release_report&metric=security_rating)](https://sonarcloud.io/dashboard?id=alanverdugo_github_release_report)

[![Technical Debt](https://sonarcloud.io/api/project_badges/measure?project=alanverdugo_github_release_report&metric=sqale_index)](https://sonarcloud.io/dashboard?id=alanverdugo_github_release_report)

[![Vulnerabilities](https://sonarcloud.io/api/project_badges/measure?project=alanverdugo_github_release_report&metric=vulnerabilities)](https://sonarcloud.io/dashboard?id=alanverdugo_github_release_report)
