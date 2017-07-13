# Send the data, by using the ID, the length of the message and the serialized message
# from it the current IPv4
uint32 Origin
int32 ID
# The maximum size is 65k for UDP datagrams
int16 length
uint8[] data
