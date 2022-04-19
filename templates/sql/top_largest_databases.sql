select datname as name
     , pg_size_pretty(raw_size) as size
     , datname = current_database() as is_current_database
  from (select datname
             , pg_database_size(datname) as raw_size
          from pg_database
         where datistemplate = false
           and has_database_privilege (datname, 'CONNECT') = true
         order by 2 desc
         limit 5) s
