# Expense Tracker
Ideally this will simplify sharing expense tracking from Lunch Money
- Streamlit website
- PNG to group chat
- Excel with results

## Commands
- `poetry install`
- `poetry shell`
- tests - `python -m unittest discover`

## Notes

Flow of Data

- [ ] Excel expense tracker
  - pivot tables to summarize transactions
  - bar graph w/ amount per category (reference Lunch Money)
  - bar graph w/ highest spending per merchants
  - line graph w/ cumulative spending
- [ ] Lunch Money scripts
  - create transactions for Fidelity + PayPal transactions from CSV
  - get monthly transactions as CSV
- [ ] Excel expense tracker generator (package)
  - python script for PDF - load CSV, build graphs, create PDF
  - python script for Excel - load CSV, build Pivot Tables, build graphs, create Excel
- [ ] Integrations
  - python script to screenshot PDF monthly summary and send to Messenger OR Discord
  - python script to upload Excel into existing Excel "Timmy / Jon Rent" as new page
- [ ] Streamlit
	- show tables, graphs in local UI

### Caveats
- ERROR: pandas `groupby` removing columns when converting to list of dicts?
  - Solution: `reset_index` creates new columns from levels of index so it will convert nicely
- ERROR: VSCode fails to find unittest tests and tries to use pytest
  - Solution: add following to settings.json - `"python.experiments.optOutFrom": ["pythonTestAdapter"]`
- `poetry add python-dotenv`
  - DO NOT install `dotenv` as that is a different package
- ERROR: VSCode cannot find packages installed w/ Poetry
  - Solution: Cmd+Shift+P +  `Python: Select Interpreter` - selected 3.10.11 env that poetry created
- `poetry add numpy==1.26`
  - NumPy had a major `2.0` release on 16 Jun 2024 (1 week ago) and that breaks Pandera's compatability with Pandas
  - This command pins `numpy` version to the release before that major `2.0` release
  - NOTE: Installing this required explicit python version too: `python = "<3.13,>=3.10"`


### To Do
Expense Tracker Service
- data
  - [ ] fix: previous existing zscript
  - [ ] feat: zscript to upload Fidelity + PayPal transactions
- datasource
  - lunch money
    - [ ] get transactions
    - [ ] write results to file to permanently cache
- service
  - StatisticService
    - [ ] calculate
    - [ ] get
- client
  - [ ] types
  - [ ] Streamlit
  - [ ] PNG summary 
    - [ ] spike: Discord integration
    - [ ] spike: Messenger integration
  - [ ] Excel
    - [ ] spike: build in Google Sheets
---
- [ ] update repo description

#### Archive To Do
- [ ] add pre commit hooks

### Bootstrap Steps
expense_tracker package
- shell
  ```shell
  mkdir -p expense-tracker/expense_tracker && touch expense-tracker/expense_tracker/__init__.py
  cd expense-tracker
  poetry init
  poetry add arrow
  poetry add --group dev black flake8 isort
  # implementing StatisticService
  poetry add pandera
  ```
- powershell
  ```powershell
  New-Item -ItemType Directory -Path "expense-tracker/expense_tracker" -Force
  New-Item -ItemType File -Path "expense-tracker/expense_tracker/__init__.py" -Force
  Set-Location "expense-tracker"
  poetry init
  poetry add arrow
  poetry add --group dev black flake8 isort
  ```

client
```shell
cd expense-tracker
mkdir client && cd client
touch utils.py streamlit_app.py
poetry init
poetry add arrow
poetry add git+https://github.com/Borghese-Gladiator/expense-tracker.git
# poetry add streamlit pandas numpy
# poetry add matplotlib
# generated example code via ChatGPT
# streamlit run .\streamlit.py
```

<details>
<summary>Archive</summary>

## Methodology
```
Aggregate by Interval
APPROACH 1: custom build every group by incrementing arrow
    PRO: easy increment
    CON: hard group since I need to build bins and sort each into bins
APPROACH 2: custom column and standard group by
    PRO: easy group by
    CON: wasted extra column AND unable to support weekly?
```


# Expense Aggregation
Python ETL pipeline to build full transaction history from multiple credit cards

Currently, it is only one Pandas script that aggregates CSVs though

## Usage Instructions
- download transaction history
  - rename statements to include company name (can use `Powershell` script potentially)
    - if company not present in "company enum", write company parse logic in "find_transactions_table" and "normalize_transaction_df"
- update script "CONSTANTS"
- run locally
  ```
  poetry install
  poetry shell
  python main.py
  ```

## Notes
Bootstrap Steps
- `poetry init`
- `git init`
- write `.gitignore` using online `Python.gitignore`
- `poetry add loguru tabula-py[jpype] pandas`
  - NOTE: `tabula` is a package, but not related to reading PDFs
- write main.py
- download `financial_transaction_history` from all my credit card companies
- > write methodology
- [X] download PDFs
- [X] extract tables from PDFs to build transactions list CSV => gave up
- [X] download all as CSVs
- [X] build aggregated table
  - [X] add default column of rent_applicable_transaction
  - [X] remove credit 
- [X] create Excel spreadsheet
- [ ] build subset Excel spreadsheet by filter on rent_applicable_transaction column


### PDF Extraction Libraries
- pypdf
  - extract text and manually filter using index per type of PDF instead
  - Pros - very easy for library since I simply run `page.extract_text().split('\n')`
  - Cons
    - certain text gets appended together with no delimeter (eg: `Dec 11 Dec 11 MASALA BAYLITTLETONMA $116.37 `)
    - tons of custom code
      - pick page number
      - pick start of transaction list string
      - pick end of transaction list string
      - write logic to parse out each string
  - (possible implementation: Check row content to determine when to stop)
- camelot
  - NOTE: `poetry add camelot-py[base]` (NOT `camelot`)
  - camelot-py installation
    - use Python 3.8 - depends on `pdftopng 0.2.3` which requires Python 3.8, 3.7, or 3.6.
    - `poetry add opencv-python`
    - download [Ghostscript](https://ghostscript.com/releases/gsdnld.html)
      - check installed with either command:
        - `gswin64c --version`
        - ```python
          import ctypes
          from ctypes.util import find_library
          find_library("".join(("gsdll", str(ctypes.sizeof(ctypes.c_voidp) * 8), ".dll")))
          ```
    - `poetry add ghostscript`
  - CLI usage
    - `camelot lattice -plot text .\capital_one_Smry_2023_1496.pdf`
      - `poetry add matplotlib` - `ImportError: matplotlib is required for plotting.`
  - NOTE: Did not find any text and could not figure out how to customize
- tabula
  - NOTE: `poetry add tabula-py`
  - > WARNING: The stream doesn't provide any stream length, using fallback readUntilEnd, at offset 64514
  - This warning indicates that the library is unable to determine the length of the PDF stream, so it falls back to a method called readUntilEnd.
  - Tabula works for basic tables, but my financial documents require customization. Tabula customizes via template which are generated by the desktop app.
    - the Tabula desktop app requires installation of ORACLE Java 8. Using OpenJDK 8 (Zulu) does not seem to work. Oracle Java 8 does not ship with an installer and requires manual config (JAVA_HOME I assume?). Either way, I elected against spending more effort on Java 8 which I would need to uninstall manually

#### PDF Methodology

Method A
- download PDFs
- extract tables from PDFs to build transactions list CSV
- build Excel spreadsheet from aggregated table
  - add default column of rent_applicable_transaction
- build subset Excel spreadsheet of rent applicable transactions using column

Method B
- download PDFs
- extract tables from PDFs to build transactions list CSV
- build Next.js webapp
	- display list of transactions in Material Table (filter + sort columns)
	- display list of J Shee transactions via hard-coded code
	- deploy to Vercel

### Troubleshooting

```
Package operations: 1 install, 0 updates, 0 removals

  - Installing pdftopng (0.2.3): Failed

  RuntimeError

  Unable to find installation candidates for pdftopng (0.2.3)

  at ~\AppData\Roaming\pypoetry\venv\lib\site-packages\poetry\installation\chooser.py:74 in choose_for
       70│
       71│             links.append(link)
       72│
       73│         if not links:
    →  74│             raise RuntimeError(f"Unable to find installation candidates for {package}")
       75│
       76│         # Get the best link
       77│         chosen = max(links, key=lambda link: self._sort_key(package, link))
       78│

Cannot install pdftopng.
```

# To DO
- write ETL pipeline to get near real-time data
  - write Extract script to download transaction info
    - integrate w/ banks
  - update Transform script to run on transaction info
  - write Load script to save transaction info
    - build Google Sheets w/ pivot tables + graphs like "Timmy Expense Tracker"
- investigate using cron for ETL pipeline

</details>