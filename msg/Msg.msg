# Maximum IP packet size : 65,535 bytes, let's say 64k.
# With 256 (high level) Fragments of size of 64k gives 16Mo
# It already means you are sending 256*50 (IP fragmentation) 
# packets and means 12800 packets needs to be sent, stored and defragmented over UDP, an unreliable link.
# If you need that much, please use TCP to each host.
uint8 status
# Status:
#   7 (LSB): Is a fragment (read fragment from the data)
uint8 IS_FRAGMENT=1 #0b00000001 (status & IS_FRAGMENT == 1 if fragment, 0 if no fragment)
# The packet id, increase for each MESSAGE 
# (fragments have the same ID, different data and type Fragment)
uint16 packet_id
# Data
uint8[] data
