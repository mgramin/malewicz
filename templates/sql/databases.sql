select *
  from pg_database
 where datistemplate = false
   and datname = current_database()
