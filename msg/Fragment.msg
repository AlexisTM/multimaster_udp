# Total number of fragments
uint8 n_fragments
# fragment_id: Used to check if everything arrived
# Range: [0, n_fragments-1]
uint8 packet_id
uint8[] data
