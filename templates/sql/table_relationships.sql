select distinct 
       ccu.table_name as main_table
     , tc.table_name as slave_table
  from information_schema.table_constraints as tc
  join information_schema.key_column_usage as kcu on tc.constraint_name = kcu.constraint_name
  join information_schema.constraint_column_usage as ccu on ccu.constraint_name = tc.constraint_name
 where tc.constraint_type = 'FOREIGN KEY'
   and tc.table_schema not in ('pg_catalog', 'information_schema')
