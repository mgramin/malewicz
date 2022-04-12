select table_name
     , rank
     , total_size
  from (select table_name
             , rank() over (order by total_size desc) as rank
             , total_size
          from (select table_name
                     , pg_total_relation_size(quote_ident(table_name)) as total_size
                  from information_schema.tables
                 where table_schema not in ('pg_catalog', 'information_schema')
                   and table_catalog = current_database()) as base) as agg
 where rank <= %(max_table_count)s
