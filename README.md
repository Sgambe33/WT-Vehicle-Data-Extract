# WT-Vehicle-Data-Extract

## Introduction

This is a repo containing all the scripts used to parse data from War Thunder and store it in a database.

## Requirements

- Python 3.10+

## How to use

1. Clone the repo
2. Clone this other repo: [War Thunder Datamine](https://github.com/gszabi99/War-Thunder-Datamine).
3. Specify in an `.env` file the path to the datamine repo. Place the file in the directory called "utils". The `.env`
   file should look like this:

```
DATAMINE_LOCATION="path/to/datamine/repo"
```

4. Run `python main.py` in the root directory of this repo.
5. Inside the `nations` folder you will find all the json files containing the data.

## TODO

- [ ] Document the code.

## How to contribute

1. Fork the repo
2. Make your changes
3. Create a pull request