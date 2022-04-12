select c.table_schema
     , c.table_name
     , c.column_name
     , c.ordinal_position
     , c.is_nullable
     , c.data_type
     , c.character_maximum_length
  from pg_tables t
  join information_schema.columns c on c.table_schema = t.schemaname
                                   and c.table_name = t.tablename
 where table_schema not in ('pg_catalog', 'information_schema')