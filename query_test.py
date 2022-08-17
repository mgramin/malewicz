import unittest

from query import Query

class TestQuery(unittest.TestCase):

    def test_add(self):
        query = Query("""
            -- Short name
            -- Long description
            select field1 as fld1 /* Just comment */
                 , field2 as fld2 -- Just another comment
                 , field3 as fld3 /* Just another comment */
              from foo""")
        query.parse()

        self.assertEqual(query.columns['fld1'], 'Just comment')
        self.assertEqual(query.columns['fld2'], 'Just another comment')
        self.assertEqual(query.columns['fld3'], 'Just another comment')


    def test2(self):
        query = Query("""
-- Slow Queries
-- Slowest queries, by total time
select total_exec_time  -- Total Exec Time
     , calls            -- Calls
     , mean_exec_time   -- Mean Exec Time
     , min_exec_time    -- Min Exec Time
     , max_exec_time    -- Max Exec Time
  from (select sum(calls) as calls
     , round(sum(total_exec_time)::numeric, 2) as total_exec_time
     , round((sum(mean_exec_time * calls) / sum(calls))::numeric, 2) as mean_exec_time
     , round(min(min_exec_time)::numeric, 2) as min_exec_time
     , round(max(max_exec_time)::numeric, 2) as max_exec_time
     , round(sum(total_plan_time)::numeric, 2) as total_plan_time
     , round((sum(mean_plan_time * calls) / sum(calls))::numeric, 2) as mean_plan_time
     , round(min(min_plan_time)::numeric, 2) as min_plan_time
     , round(max(max_plan_time)::numeric, 2) as max_plan_time
     , sum(rows) as rows
     , (select usename from pg_user where usesysid = userid) as usr
     , (select datname from pg_database where oid = dbid) as db
     , query
     , sum(shared_blks_hit) as shared_blks_hit
     , sum(shared_blks_read) as shared_blks_read
     , sum(shared_blks_dirtied) as shared_blks_dirtied
     , sum(shared_blks_written) as shared_blks_written
     , sum(local_blks_hit) as local_blks_hit
     , sum(local_blks_read) as local_blks_read
     , sum(local_blks_dirtied) as local_blks_dirtied
     , sum(local_blks_written) as local_blks_written
     , sum(temp_blks_read) as temp_blks_read
     , sum(temp_blks_written) as temp_blks_written
     , sum(blk_read_time) as blk_read_time
     , sum(blk_write_time) as blk_write_time
     , array_agg(queryid) as queryids
  from pg_stat_statements
 group by userid, dbid, query) as s
 order by total_exec_time desc
 limit 50
""")
        query.parse()
        self.assertEqual(query.columns['total_exec_time'], 'Total Exec Time')


    def test3(self):
        query = Query("""
-- Columns
-- Columns
select ordinal_position         -- Pos.
     , "column_name"              -- Name
     , data_type                -- Type
     , is_nullable              -- Nullable
     , character_maximum_length -- Length
  from (select c.table_schema
     , c.table_name
     , c.column_name
     , c.ordinal_position
     , c.is_nullable
     , c.data_type
     , c.character_maximum_length
  from pg_tables t
  join information_schema.columns c on c.table_schema = t.schemaname
                                   and c.table_name = t.tablename
 where table_schema not in ('pg_catalog', 'information_schema')) s

""")
        query.parse()    



    def test4(self):
        query = Query("""
-- Tables with no stats
-- Tables with no stats
select "table_schema"     -- Schema
     , "table_name"       -- Table
     , "is_empty"         -- Empty
     , "never_analyzed"   -- Never Analyzed
     , "no_stats_columns" -- Columns
  from ({% include 'sql/tables_no_stats.sql' %}) s
""")
        query.parse()


if __name__ == "__main__":
    unittest.main()
