# README.md - `lptwitdelete`

<!-- TOC -->

- [README.md - `lptwitdelete`](#readmemd---lptwitdelete)
  - [Overview](#overview)
  - [Installation](#installation)
    - [API keys](#api-keys)
  - [Documentation](#documentation)
  - [Quick Start](#quick-start)
    - [Delete most recent 3200 statuses using the Twitter API](#delete-most-recent-3200-statuses-using-the-twitter-api)
    - [Delete statuses between two dates, using a downloaded archive](#delete-statuses-between-two-dates-using-a-downloaded-archive)
    - [Acquiring your complete Twitter archive](#acquiring-your-complete-twitter-archive)
    - [Dry runs](#dry-runs)
  - [Licensing](#licensing)

<!-- /TOC -->

## Overview

`lptwtitdelete` is a Python script and package for deleting your account's Twitter statuses on the basis of a limited number of status criteria.

**NOTE: DELETING STATUSES FROM TWITTER IS PERMANENT. USE THIS SOFTWARE AT YOUR OWN RISK.**

## Installation

To install `lptwitdelete`, clone this repository and install using `setup.py`:

```bash
git clone git@github.com:widdowquinn/lptwitdelete.git && cd lptwitdelete
python setup.py install
```

This will install the `lptwitdelete` package for Python, and the script `lptwitdelete`, which can also be run using the alias `lptd`.

### API keys

API keys are required to interact with Twitter. You should obtain these for yourself from [https://developer.twitter.com](https://developer.twitter.com). By default, `lptd` will look for these keys in the file `~/twitter/lptwitdelete/conf.yml`, and expects the following information in YAML format:

```yaml
lptwitdelete:
  api_key:
    XXXXXXXXXXXXXXXXXXXXXXXXX
  api_secret_key:
    XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
  access_token:
    XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
  access_token_secret:
    XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
```

If you choose to store your API keys elsewhere, this location can be specified with the `-c`/`--confpath` option.

## Documentation

Detailed documentation for this package can be found on ReadTheDocs, at:

- [https://lptwitdelete.readthedocs.io/en/latest](https://lptwitdelete.readthedocs.io/en/latest)

A brief summary of usage is provided below, in the Quick Start

## Quick Start

The `lptwitdelete` program can be run using the name `lptwitdelete`, or the abbreviation `lptd`. For brevity, this `README.md` uses the `lptd` abbreviation.

### Delete most recent 3200 statuses using the Twitter API

Issue the following command at the terminal:

```bash
lptd -v --delete -o deleted.json <YOUR_USERNAME>
```

This will open your browser to authenticate you with Twitter (if necessary), and authorise the application to modify your account. Twitter will provide an authentication code in your browser, and this should be entered at the prompt as below:

```bash
$ lptd -o downloaded_test.json widdowquinn
Please enter the verification code from your browser > 5049179
```

Once the authentication code is provided, `lptd` will do the following:

1. acquire your recent Twitter stream (up to the most recent ≈3200 status updates) using the online API
2. write these tweets to the file `deleted.json` in machine-readable [`JSON` format](https://en.wikipedia.org/wiki/JSON)
3. attempt to delete the statuses from Twitter

The unique IDs of statuses which `lptd` cannot delete will be written to the terminal if the `--verbose` or `-v` option is selected.

### Delete statuses between two dates, using a downloaded archive

If you have a local archive of your Twitter history (see below) you can use this to identify statuses for deletion. In this example, we will use the `--start_date` and `--end_date` options to restrict deletion of tweets to a particular date.

Issuing the command at the terminal:

```bash
lptd -v --delete -a tweets.js -o deleted.json --start_date 2020-01-01 --end_date 2020-02-18 <YOUR_USERNAME>
```

again opens the browser to authenticate with Twitter (if necessary), and authorise the application to modify your account. Once authenticated, the command will delete from your timeline all tweets between 1st January 2020 and 18th February 2020, inclusive. The script does the following:

1. reads in your local Twitter archive (in `JSON` format) from `tweets.js`
2. filters the statuses from the archive, retaining only those that were created on or after 1st January 2020, up to and including 18th February 2020
3. writes the retained tweets to the file `deleted.json`, in `JSON` format
4. attempts to delete each of the statuses from step (2) from Twitter


### Acquiring your complete Twitter archive

This tool uses the [`tweepy` library](https://www.tweepy.org/) to access the Twitter API. The API is limited by Twitter to return no more than (approximately) the most recent 3200 Twitter statuses, so to filter and delete on the basis of older statuses you will need to acquire your own Twitter archive. This can be done via the Twitter web interface as follows.

1. Log on to the Twitter web interface [https://twitter.com/<YOUR_USERNAME>](https://twitter.com)
2. Click on the **More** icon (three dots in a circle), and select **Settings and Privacy**
3. Under **Data and Permissions**, click on **Your Twitter data**
4. Click on **Download an archive of your data**

Save the compressed `.zip` file to a local drive. Uncompress this file to obtain a directory of files describing your Twitter history. The archive of your Twitter statuses is the file named `tweet.js` in this subdirectory.

### Dry runs

`lptd` will only delete your Twitter statuses if the `--delete` switch is passed. This is intended as a brake to prevent some accidental deletions of Twitter statuses. If you do not use the `--delete` option, then no data should be deleted. Additionally, passing the `--skip_auth` argument means that no attempt is made to authenticate against Twitter, and your data should be safe. Without the `--delete` option, the command-lines above do the following:

```bash
lptd -v -o deleted.json <YOUR_USERNAME>
```

downloads your recent Twitter history to the file `deleted.json`. No tweets are deleted.

```bash
lptd -v -a tweets.js -o deleted.json --start_date 2020-01-01 --end_date 2020-02-18 <YOUR_USERNAME>
```

extracts the tweets from 1st January 2020 to 18th February 2020 inclusive to the file `deleted.json`. No tweets are deleted.

**NOTE: DELETING STATUSES FROM TWITTER IS PERMANENT. USE THIS SOFTWARE AT YOUR OWN RISK.**

## Licensing

Unless otherwise indicated, all code is subject to the following agreement:

```text
The MIT License

Copyright (c) 2020 Leighton Pritchard

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
```