import sqlite3

conn = sqlite3.connect('dbs/utility_dbs/nodes.db')
c = conn.cursor()

node_id = "WEOGIJWPOIjjwoegjeoiLJkg"
node_ip = "0.0.0.0"
node_type = "storage"

#c.execute('INSERT INTO nodes (node_id, node_type, node_ip, last_connect) VALUES ("' + node_id + '", "' + node_type + '", "' + node_ip + '", "last_connect")')
#conn.commit()

c.execute('SELECT * FROM nodes WHERE node_type="storage"')
print(c.fetchall())