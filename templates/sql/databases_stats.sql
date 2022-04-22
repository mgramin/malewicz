with data as (
  select d.oid,
        (select spcname from pg_tablespace where oid = dattablespace) as tblspace,
        d.datname as database_name,
        pg_catalog.pg_get_userbyid(d.datdba) as owner,
        has_database_privilege(d.datname, 'CONNECT') as has_access,
        pg_database_size(d.datname) as raw_size,
        stats_reset,
        blks_hit,
        blks_read,
        xact_commit,
        xact_rollback,
        conflicts,
        deadlocks,
        temp_files,
        temp_bytes
  from pg_catalog.pg_database d
  join pg_stat_database s on s.datid = d.oid
 where has_database_privilege (d.datname, 'CONNECT') = true
   and d.datistemplate = false)
select database_name || coalesce(' [' || nullif(tblspace, 'pg_default') || ']', '') as name
     , pg_size_pretty(raw_size) as size
     , (now() - stats_reset)::interval(0)::text as stats_age
     , case
         when blks_hit + blks_read > 0
         then
           (round(blks_hit * 100::numeric / (blks_hit + blks_read), 2))::text
       end as cache_eff
     , case
            when xact_commit + xact_rollback > 0 then
                    (round(xact_commit * 100::numeric / (xact_commit + xact_rollback), 2))::text
       end as committed
     , conflicts as conflicts
     , deadlocks as deadlocks
     , temp_files::text as temp_files_count
     , pg_size_pretty(temp_bytes) as temp_files_size
  from data
 order by raw_size desc nulls last
