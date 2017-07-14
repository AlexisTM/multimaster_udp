# The API should check if the data_type md5 is the same as yours
# data_type is often < 32 bytes (the 16 bytes md5sum is written in ascii in 32 bytes)
string data_type
# The maximum size is 65k for UDP datagrams
# The length of the message (data field)
int16 length
uint8[] data
