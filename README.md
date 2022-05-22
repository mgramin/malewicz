# Malewicz

Hackable GUI SQL-manager written in SQL itself (and a pinch of purest HTML, of course)


> "If you want something done, do it yourself. Yep!"
>
> Jean-Baptiste Emanuel Zorg, "The Fifth Element", 1997.

[See it in action](https://malewicz.herokuapp.com)

## What is Malewicz?

Malewicz is Yet Another WEB client for DB schema exploring and performance analysis. Something like [PgHero](https://github.com/ankane/pghero), [Pgweb](https://github.com/sosedoff/pgweb) or even [phpMyAdmin](https://github.com/phpmyadmin/phpmyadmin), but with some key features:

- Hackable - Malewicz was originally created specifically for hacking and extending  (template driven, live, without compilation and restarting)
- Suprematistic - use only your SQL skills (and a little bit HTML) without any noisy boilerplate code
- Lightning-fast AJAX web interface - but without a single line of JavaScript (we use [Hotwire Turbo](https://turbo.hotwired.dev))
- SQL Market - Make your own templates, share it and use foreign templates
- Simple and powerful integration with awesome tools, for charts, diagrams driving and etc.
- Support PostgreSQL for now (but...)

Malewicz have not query editor, use your favorite editor for work with Malewicz sql and html files.


### We were inspired by

- [dbt](https://github.com/dbt-labs/dbt-core)
- [YeSQL](https://github.com/krisajenkins/yesql) - Keep the SQL as SQL
- [Database as Code](https://github.com/mgramin/database-as-code)
