# WT-Vehicle-Data-Extract

## Introduction

This is a repo containing all the scripts used to parse data from War Thunder and store it in a database.

## Requirements

- Python 3.10+

## How to use

1. Clone the repo
2. Clone this other repo: [War Thunder Datamine](https://github.com/gszabi99/War-Thunder-Datamine).
3. Specify in an `.env` file (placed inside the utils folder) the path to the datamine repo. Place the file in the directory called "utils". The `.env`
   file should look like this:

   ```
   DATAMINE_LOCATION="path/to/datamine/repo"
   ```

4. Run `python main.py` in the root directory of this repo.

The full execution of the script will result in a database file being created in the root directory of this repo, JSON raw data files in each nation folder,
images in the assets folder and JSON localisation files in the locales folder.

Warning: if the generated database file already exists, versioning featur will automatically be enabled. This means that all the vehicles that have been modified since the last major update will be moved into another table called "vehicles_old" and the new vehicles will be added to the main table.

## TODO

- [ ] Document the code.

## How to contribute

1. Fork the repo
2. Make your changes
3. Create a pull request