select state
     , count
     , row_number() over () as id
  from (select state
             , count
             , dense_rank() over (order by count desc) as rank
          from (select coalesce(state, 'NULL') as state
                     , count(1) as count
                  from pg_stat_activity
                 group by state) s) s
 where rank <= 5
