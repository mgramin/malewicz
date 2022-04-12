select coalesce(usename, 'NULL') as usename
     , count(1) as count
     , row_number() over () as id
  from pg_stat_activity
 group by usename
