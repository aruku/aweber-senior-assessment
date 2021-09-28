# AWeber Senior Backend Software Engineer Assessment

Done in short bursts in less than a week while on vacation.

## Installation

Use pipenv to install the dependencies:

```bash
pipenv install
```

## Usage

Launch the server:

```bash
pipenv run python app.py
```

Issue the following requests:

```
GET http://localhost:3000/api/widgets/
GET, DELETE http://localhost:3000/api/widget/id
POST, PUT http://localhost:3000/api/widget/id {
  "name": "widget1",
  "number_parts": 8
}
```

### Static analyzers

Use pipenv to install the dev dependencies:

```bash
pipenv install --dev
```

Run them with:

```bash
pipenv run pep8 --show-source app.py
pipenv run bandit -r app.py
pipenv run flake8 app.py
```