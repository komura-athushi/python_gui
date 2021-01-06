import struct

#ファイルをオープンする、withでcloseをしなくていいらしい
with open('test.cag','wb') as file:
    for i in range(5):
        b_data = 'abcd'.encode()
        file.write(b_data)

    for i in range(5):
        number = struct.pack('iiiiff',1,2,3,32767,256.6,0.01)
        file.write(number)


