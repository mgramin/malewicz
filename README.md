# Malewicz

Hackable GUI SQL-manager written in SQL itself (and a pinch of the purest HTML, of course)


> "If you want something done, do it yourself. Yep!"
>
> Jean-Baptiste Emanuel Zorg, "The Fifth Element", 1997.

[See it in action](https://malewicz.herokuapp.com)

## What is Malewicz?

Malewicz is Yet Another WEB client for DB schema exploring and performance analysis. Something like [PgHero](https://github.com/ankane/pghero), [Pgweb](https://github.com/sosedoff/pgweb) or even [phpMyAdmin](https://github.com/phpmyadmin/phpmyadmin), but with some key features:

- Hackable - Malewicz was originally created specifically for hacking and extending (template driven, live reload)
- Suprematistic - use only your SQL skills (and a little bit HTML) without any noisy boilerplate code
- Lightning-fast AJAX web interface - but without a single line of JavaScript (we use [Hotwire Turbo](https://turbo.hotwired.dev))
- SQL Market - Make your own templates, share it and use foreign templates
- Simple and powerful integration with awesome tools, for charts, diagrams etc.
- Support PostgreSQL (for now)


### We were inspired by

- [dbt](https://github.com/dbt-labs/dbt-core) - Just drop your SQL-queries to your repository and the magic happens
- [YeSQL](https://github.com/krisajenkins/yesql) - Keep the SQL as SQL
- Treat your [Database as Code](https://github.com/mgramin/database-as-code)


## Run from sources

Init and activate virtual env (optional):
```
virtualenv .venv
source .venv/bin/activate
```

Install dependencies:
```
pip3 install -r requirements.txt
```

Set database connection parameters in `config.toml` file or set environment variable `DATABASE_URL` with datbase URI:

```
postgres://[USER]:[PASSWORD]@[HOST]:5432/[DATABASE]
```

Run:
```
python app.py
```


## Run from Docker

```
cd demo
docker-compose up -d
```


## SQL scripts conventions

- Use Python-style naming for parameters: `%(schema_name)s`, `%(max_table_count)s`
- Keep to [axis](https://gramin.pro/posts/rivers-and-axis) when formatting
