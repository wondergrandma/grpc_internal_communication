# grpc_internal_communication

GRPC Internal Communication is a scraping microservice designed for a film streaming platform. Its primary responsibility is to collect essential metadata about films uploaded to the service. This metadata is then made available to other services (such as frontend, mobile app). Data is stored in Postgre database.

# Table of Contents
- [Scraper](#Scraper)
- [Model example](#Model_example)
- [Usage](#Usage)
- [Future Development](#Future_Development)

## Scraper

All scrapers must extend the `BaseScraper` class. This enforces the **Factory design pattern**, ensuring that the system remains modular, maintainable, and easily extendable with new scraper implementations in the future.

### TmdbScraper

Currently, the service includes a single scraper: `TmdbScraper`. This scraper is responsible for extracting film data from  [tmdb](https://www.themoviedb.org/). 

## Model example

### Film

```python
Id: int
Name: str
MakeYear: int
Hour: int
Minute: int
Categories: List
Overview: str
Actors: List
Directors: List
Rating: int
CoverPath: str
```

### Category

```python
Id: int
Genre: str 
Film: List
```

### Actor

```python
Id: int
Name: str 
Surname: str
Film: List
```

### Director

```python
Id: int
Name: str
Surname: str
Film: List
```

## Usage

This project uses [Poetry](https://python-poetry.org/) to manage dependencies and virtual environments. Poetry must be installed on your system before continuing.

- `git clone https://github.com/wondergrandma/grpc_internal_communication.git`
- `cd grpc_internal_communication`
- `poetry install`
- `poetry shell`
- `python main.py`

## Future Development
Containerization of the service and implementation of additional scrapers.
