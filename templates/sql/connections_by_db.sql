select datname
     , count
     , row_number() over () as id
  from (select datname
     , count
     , dense_rank() over (order by count desc) as rank
  from (select coalesce(datname, 'NULL') as datname
             , count(1) as count
          from pg_stat_activity
         group by datname) s )s
where rank <= 5
