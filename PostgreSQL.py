import Spartacus.Database
import OmniDatabase
import sys
from collections import OrderedDict

v_schemaName = sys.argv[1]

print('Schema name: ' + v_schemaName)

try:
    #Connect to databases
    v_dbConn1 = OmniDatabase.PostgreSQL('host', 'port', 'service', 'user', 'password')
    v_dbConn2 = OmniDatabase.PostgreSQL('host', 'port', 'service', 'user', 'password')

    #Check created / dropped tables
    v_tableConn1 = v_dbConn1.QueryTables(p_schema = v_schemaName)
    v_tableConn2 = v_dbConn2.QueryTables(p_schema = v_schemaName)
    v_tableDiff = v_tableConn1.Compare(v_tableConn2, ['table_schema', 'table_name'], 'status', 'diff')

    if len(v_tableDiff.Rows) > 0:
        print('\nCreate / Drop table\n')
        print(v_tableDiff.Pretty())

    #Check altered tables
    v_tableConn1 = v_dbConn1.QueryTablesFields(p_schema = v_schemaName)
    v_tableConn2 = v_dbConn2.QueryTablesFields(p_schema = v_schemaName)
    v_tableDiff = v_tableConn1.Compare(v_tableConn2, ['table_name', 'column_name'], 'status', 'diff')

    if len(v_tableDiff.Rows) > 0:
        print('\nAlter table\n')
        print(v_tableDiff.Pretty())

    #Check created / dropped foreign keys
    v_tableConn1 = v_dbConn1.QueryTablesForeignKeys(p_schema = v_schemaName)
    v_tableConn2 = v_dbConn2.QueryTablesForeignKeys(p_schema = v_schemaName)
    v_tableDiff = v_tableConn1.Compare(v_tableConn2, ['table_name', 'constraint_name'], 'status', 'diff')

    if len(v_tableDiff.Rows) > 0:
        print('\nAdd / Drop foreign key\n')
        print(v_tableDiff.Pretty())

    #Check created / dropped primary keys
    v_tableConn1 = v_dbConn1.QueryTablesPrimaryKeys(p_schema = v_schemaName)
    v_tableConn2 = v_dbConn2.QueryTablesPrimaryKeys(p_schema = v_schemaName)
    v_tableDiff = v_tableConn1.Compare(v_tableConn2, ['table_name', 'constraint_name', 'column_name'], 'status', 'diff')

    if len(v_tableDiff.Rows) > 0:
        print('\nAdd / Drop primary key\n')
        print(v_tableDiff.Pretty())

    #Check created / dropped uniques
    v_tableConn1 = v_dbConn1.QueryTablesUniques(p_schema = v_schemaName)
    v_tableConn2 = v_dbConn2.QueryTablesUniques(p_schema = v_schemaName)
    v_tableDiff = v_tableConn1.Compare(v_tableConn2, ['table_name', 'constraint_name', 'column_name'], 'status', 'diff')

    if len(v_tableDiff.Rows) > 0:
        print('\nAdd / Drop unique\n')
        print(v_tableDiff.Pretty())

    #Check created / dropped indexes
    v_tableConn1 = v_dbConn1.QueryTablesIndexes(p_schema = v_schemaName)
    v_tableConn2 = v_dbConn2.QueryTablesIndexes(p_schema = v_schemaName)
    v_tableDiff = v_tableConn1.Compare(v_tableConn2, ['table_name', 'index_name', 'column_name'], 'status', 'diff')

    if len(v_tableDiff.Rows) > 0:
        print('\nAdd / Drop index\n')
        print(v_tableDiff.Pretty())

    #Check created / dropped functions
    v_tableConn1 = v_dbConn1.QueryFunctions(p_schema = v_schemaName)
    v_tableConn2 = v_dbConn2.QueryFunctions(p_schema = v_schemaName)
    v_tableDiff = v_tableConn1.Compare(v_tableConn2, ['name', 'id'], 'status', 'diff')

    if len(v_tableDiff.Rows) > 0:
        print('\nCreate / Drop function\n')
        print(v_tableDiff.Pretty())

    v_functionList = []

    i = 0

    while i < len(v_tableConn1.Rows):
        j = 0

        while j < len(v_tableConn2.Rows):
            if v_tableConn1.Rows[i]['id'] == v_tableConn2.Rows[j]['id']:
                v_functionList.append(v_tableConn1.Rows[i]['id'])
                v_tableConn1.Rows.pop(i)
                i -= 1
                v_tableConn2.Rows.pop(j)
                j -= 1
                break

            j += 1

        i += 1

    if(len(v_functionList) > 0):
        v_functionListConn1 = Spartacus.Database.DataTable()
        v_functionListConn2 = Spartacus.Database.DataTable()

        #Check altered functions fields
        for v_function in v_functionList:
            v_tableConn1 = v_dbConn1.QueryFunctionFields(p_function = v_function, p_schema = v_schemaName)

            if len(v_functionListConn1.Columns) == 0:
                for v_column in v_tableConn1.Columns:
                    v_functionListConn1.Columns.append(v_column)

                v_functionListConn1.Columns.append('id')

            for v_row in v_tableConn1.Rows:
                v_rowTmp = list(v_row)
                v_rowTmp.append(v_function)
                v_functionListConn1.Rows.append(OrderedDict(zip(v_functionListConn1.Columns, tuple(v_rowTmp))))

            v_tableConn2 = v_dbConn2.QueryFunctionFields(p_function = v_function, p_schema = v_schemaName)

            if len(v_functionListConn2.Columns) == 0:
                for v_column in v_tableConn2.Columns:
                    v_functionListConn2.Columns.append(v_column)

                v_functionListConn2.Columns.append('id')

            for v_row in v_tableConn2.Rows:
                v_rowTmp = list(v_row)
                v_rowTmp.append(v_function)
                v_functionListConn2.Rows.append(OrderedDict(zip(v_functionListConn2.Columns, tuple(v_rowTmp))))

        v_tableDiff = v_functionListConn1.Compare(v_functionListConn2, ['id', 'type', 'name'], 'status', 'diff')

        if len(v_tableDiff.Rows) > 0:
            print('\nAlter function fields\n')
            print(v_tableDiff.Pretty())

        v_functionListConn1 = Spartacus.Database.DataTable()
        v_functionListConn2 = Spartacus.Database.DataTable()

        #Check altered functions definitions
        for v_function in v_functionList:
            v_functionDefinition = v_dbConn1.GetFunctionDefinition(p_function = v_function)

            if len(v_functionListConn1.Columns) == 0:
                v_functionListConn1.Columns.append('definition')
                v_functionListConn1.Columns.append('id')

            v_rowTmp = []
            v_rowTmp.append(v_functionDefinition)
            v_rowTmp.append(v_function)
            v_functionListConn1.Rows.append(OrderedDict(zip(v_functionListConn1.Columns, tuple(v_rowTmp))))

            v_functionDefinition = v_dbConn2.GetFunctionDefinition(p_function = v_function)

            if len(v_functionListConn2.Columns) == 0:
                v_functionListConn2.Columns.append('definition')
                v_functionListConn2.Columns.append('id')

            v_rowTmp = []
            v_rowTmp.append(v_functionDefinition)
            v_rowTmp.append(v_function)
            v_functionListConn2.Rows.append(OrderedDict(zip(v_functionListConn2.Columns, tuple(v_rowTmp))))

        v_tableDiff = v_functionListConn1.Compare(v_functionListConn2, ['id'], 'status', 'diff')

        if len(v_tableDiff.Rows) > 0:
            print('\nAlter function definition\n')
            print(v_tableDiff.Pretty())

    #Check created / altered / dropped sequences
    v_tableConn1 = v_dbConn1.QuerySequences(p_schema = v_schemaName)
    v_tableConn2 = v_dbConn2.QuerySequences(p_schema = v_schemaName)
    v_tableDiff = v_tableConn1.Compare(v_tableConn2, ['sequence_name'], 'status', 'diff')

    if len(v_tableDiff.Rows) > 0:
        print('\nAdd / Drop index\n')
        print(v_tableDiff.Pretty())
except Spartacus.Database.Exception as exc:
	print(str(exc))
