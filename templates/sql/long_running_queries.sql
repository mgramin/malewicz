select pid
     , now() - query_start as duration
     , query
  from pg_stat_activity
 where query <> ''::text
   and state <> 'idle'
   and now() - query_start > interval '5 minutes'
 order by now() - query_start desc
