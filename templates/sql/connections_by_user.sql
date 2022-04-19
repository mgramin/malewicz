select string_agg(usename, ', ') as usename
     , count
     , row_number() over () as id
  from (select usename
             , count
             , dense_rank() over (order by count desc) as rank
          from (select coalesce(usename, 'NULL') as usename
                     , count(1) as count
                  from pg_stat_activity
                 group by usename) s )s
 where rank <= 5
 group by count
 order by count desc
