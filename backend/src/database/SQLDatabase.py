from langchain import SQLDatabase

db = SQLDatabase.from_uri('postgresql://postgres:sl`FuuJu";~kFrfg@34.145.26.239/testDB',
    include_tables=['campaigns','performance_data'],
    sample_rows_in_table_info=2)

