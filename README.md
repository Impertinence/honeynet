WHAT IS CONDIMENT?

Condiment is a decentralized storage network protocol and platform being developed by Gopher Labs. Condiment leverages the processing power and storage space of the world's 20+ billion internet connected devices
to provide a living, breathing platform for secure decentralized data storage, hosting, and browsing.



COMMON TERMS AND CONCEPTS:

Browser - Nodes on the network which only have read access to public satellite buckets.

Storage - A node which stores files on the network. Any internet connected device with excess storage space of at least 200gb can be a storage node.

Mechanic - A node which repairs file loss due to node churn. Certain nodes may go offline for various reason. In these cases, the mechanic node retrieves any remaining file fragments from their remote locations and generates the missing file fragments, ensuring all files are available on the network 24/7.

Utility - A utility node is a node which provides utility information on the network including, fragment locations, node lists, network health and node churn. 

Satellite - A satellite node is a node on the Condiment network which is able to write and read files from the network

Bucket - A bucket is a collection of artificial filepaths on the network which can either be made private to satellite access, or public to Condiment browsers 



HOW DOES CONDIMENT WORK? 

Condiment encrypts satellite files and then uses Reed Solomon Erasure coding to encode files into 10 data elements and 20 parity elements providing redundancy for satellite files on the network.
These encoded and encrypted file fragments are then split among the most viable storage nodes in terms of activity, storage space, bandwidth, and physical distance relative to the satellite uploading the file. 
Files are encrypted and encoded on the satellite system and can only be retrieved by that satellite, preventing access to files on the network, even to network operators.




BENEFITS OF CONDIMENT:

Condiment allows for a more secure and permanent file hosting and browsing solution. To destroy or read a file without permission, attackers must compromise 50% or more of the network's devices. Even in 
this extreme case, attackers must be able to crack AES to actually read files stored on the network unless files are stored in a public bucket. Condiment provides faster file access as nodes provide file 
fragments rather than a singular file. This allows for browser nodes to retrieve 50% of a files fragments in order to read the file instead of retrieving an entire file. 



BUILT BY PRANAV HEGDE AND GOPHER LABS
