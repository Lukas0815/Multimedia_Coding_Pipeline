
# gets int as input, return hammingcode of x as string
def ham74(x):
        test1 = x & 13          #1101
        p1 = count1(test1) % 2
        print("test1: ", bin(test1))

        test2 = x & 11          #1011
        p2 = count1(test2) % 2

        test3 = x & 7           #0111
        p3 = count1(test3) % 2

        binx = bin(x)[2:].zfill(4)
        code = str(p1) + str(p2) + binx[0] + str(p3) + binx[1:]
        print('p1: ', p1, ' p2: ', p2, ' p3: ', p3, ' binx[0]: ', binx[0], ' rest: ', binx[1:])

        # return string representation
        return '0' + code 

# gets int as input and counts amount of 1 in bin(x)
def count1(x):
        return bin(x).count('1')

def originalBytes(x):
        binrep = bin(x)[2:].zfill(8)
        binx = binrep[3] + binrep[5:]
        binx = int(binx, 2)
        #return binx.to_bytes(1, byteorder='big', signed=False)
        return binx

def decode(x):
        #x = int.from_bytes(byte, byteorder='big')
        #print(bin(var[0])[2:].zfill(8))
        
        #Calculate s1, s2 and s3
        t1 = x & 0b01010101
        s1 = count1(t1) % 2

        t2 = x & 0b00110010
        s2 = count1(t2) % 2

        t3 = x & 0b00001111
        s3 = count1(t3) % 2
        if (s1+s2+s3) == 0:
                # no error detected
                #print("rec: ", originalBytes(x))
                return originalBytes(x)
        else:
                # Error detected
                location = s1 + s2*2 + s3*4
                s = list(bin(x)[2:].zfill(8))           #make list out of binary representation
                
                if s[location] == '1':
                        s[location] = '0'
                else:
                        s[location] = '1'
                intrep = int(''.join(s), 2)
                #print("byte: ", byte, "s1-s3", s1, s2, s3, "changed: ", ''.join(s), "  original data:  ", originalBytes(intrep))
                #print("rec: ", originalBytes(intrep))
                return originalBytes(intrep)


front = '00110010'
end = '01100100'

inter_table = [list(front[:4]), list(front[4:]), list(end[:4]), list(end[4:])]
interleaved = []

for i in range(4):
        for j in range(4):
                interleaved.append(inter_table[j][i])

print("interleaved: ", interleaved)

front_byte = int(''.join(interleaved[:8]), 2).to_bytes(1, byteorder='big', signed=False)
end_byte = int(''.join(interleaved[8:]), 2).to_bytes(1, byteorder='big', signed=False)


## DECODE
front_int = int.from_bytes(front_byte, byteorder='big')
end_int = int.from_bytes(end_byte, byteorder='big')

front_list = list(bin(front_int)[2:].zfill(8))
end_list = list(bin(end_int)[2:].zfill(8))

inter_table = [front_list[:4], front_list[4:], end_list[:4], end_list[4:]]
dec_front = []
dec_end = []

for i in range(4):
        for j in range(4):
                if i < 2:
                        dec_front.append(inter_table[j][i])
                else:
                        dec_end.append(inter_table[j][i])

print("front: ", dec_front, "  end: ", dec_end)
front_int = int(''.join(dec_front), 2)
end_int = int(''.join(dec_end), 2)

# TODO: Do something sensible.
front_int = decode(front_int)
end_int = decode(end_int)

#putting it back together
ges = front_int << 4
ges = ges + end_int
erg = ges.to_bytes(1, byteorder='big', signed=False)

print("erg: ", erg)