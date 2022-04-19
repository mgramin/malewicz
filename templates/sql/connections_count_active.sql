select count(1) as count
  from pg_stat_activity
 where state = 'active'
