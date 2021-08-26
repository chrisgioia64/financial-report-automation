# Financial Report Automation

This project scrapes and downloads financial reports from the website https://www.districtdirectory.org .

## How to Run

Run the python script `scraper.py` to download a large chunk of the financial reports. All files will be downloaded into a folder called `reports` in your local directory.

A log file will be generated for every script run. The log will list which files were successfully added (`ADDED`), could not be downloaded by the script (`MISSING`), and those which already existed in the `reports` folder from a prior script run (`ALREADY EXISTS`)

**Tip:** After manually adding the missing financial reports, re-run the script to check all missing files were successfully added.

### Additional Options

    python scraper.py brazoria

The command above will scrape files starting with the county `brazoria` (case insensitive) and ignore all counties earlier (i.e. Aransas and Bastrop counties).

## Statistics

As of 8/25/2021, the script added 682 reports and missed 192 reports.
