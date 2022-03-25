import pandas as pd

def db_table_to_route(table):
    return f"./{table}.csv"

def db_create(table, el, index='id'):
    t = pd.read_csv(db_table_to_route(table), index_col=index)
    t.loc[el[index]] = [el[column] for column in t.columns]
    t.to_csv(db_table_to_route(table), index=True, index_label=index)
    return t

def db_read(table, index='id'):
    t = pd.read_csv(db_table_to_route(table), index_col=index)
    t.index = t.index.map(str) # treat indexes as strings
    return t

def db_update(table, el, index='id'):
    t = pd.read_csv(db_table_to_route(table), index_col=index)
    t.index = t.index.map(str) # treat indexes as strings
    for key in el.keys():
        if key != index:
            t.loc[el[index], key] = el[key]
    t.to_csv(db_table_to_route(table), index=True, index_label=index)
    return t

def db_delete(table, el, index='id'):
    t = pd.read_csv(db_table_to_route(table), index_col=index)
    t.index = t.index.map(str) # treat indexes as strings
    t = t.drop(el[index])
    t.to_csv(db_table_to_route(table), index=True, index_label=index)
    return t
