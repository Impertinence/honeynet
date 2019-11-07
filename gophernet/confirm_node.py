if "utility" in data:
                    node_id = data.replace("[GETNODES]: utility-", "", 1)
                    
                    def find_node(node_id):
                        node_c.execute('SELECT * FROM nodes WHERE node_id="' + node_id + '";')
                        
                        return node_c.fetchall()
                    
                    if find_node(node_id) != []:
                        def node_lookup(node_id):
                            node_c.execute('SELECT * FROM nodes;')
                            
                            return node_c.fetchall()
                            
                        nodes = node_lookup(node_id)

                    else:
                        def node_lookup(node_id):
                            node_c.execute('SELECT * FROM nodes;')
                            
                            return node_c.fetchall()
                            
                        nodes = node_lookup(node_id)
                    
                        confirmed_nodes = []
                    
                        for node in nodes:
                            def verify_node(node_ip):
                                message = bytes("[VERIFY_NODE]: utility-" + node_id, "utf-8")
                                tcpClient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                                tcpClient.connect((node_ip, transmit_port))
                                
                                tcpClient.send(message)
                                    
                            #replace 0.0.0.0 with node[2]
                            verify_node('0.0.0.0')
                            
                            def confirm_node(node_id):
                                confirm_conn = sqlite3.connect('dbs/nodes.db')
                                confirm_c = confirm_conn.cursor()
                                
                                confirm_c.execute('SELECT * FROM confirmed_nodes WHERE node_id="' + node_id + '";')
                                
                                return len(confirm_c.fetchall())
                                    
                                threading.Timer(1, confirm_node, [node_id]).start()
                            confirm_node(node[0])