select coalesce(datname, 'NULL') as datname
     , count(1) as count
     , row_number() over () as id
  from pg_stat_activity
 group by datname
