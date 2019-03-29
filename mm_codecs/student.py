from typing import List, Generator


def mm_encode(source: Generator[bytes, None, None]) -> Generator[bytes, None, None]:
 
    for byte in source:
        work = int.from_bytes(byte, byteorder='big')       #give int representation of byte
        front_int = work >> 4
        end_int = work & 15

        front = ham74(front_int)
        end = ham74(end_int)

        #interleaving
        inter_table = [list(front[0:4]), list(front[4:]), list(end[:4]), list(end[4:])]
        interleaved = []

        for i in range(4):
                for j in range(4):
                        interleaved.append(inter_table[j][i])
        
        front_byte = int(''.join(interleaved[:8]), 2).to_bytes(1, byteorder='big', signed=False)
        end_byte = int(''.join(interleaved[8:]), 2).to_bytes(1, byteorder='big', signed=False)
      
        # one can only return ONE byte. So yield twice. YES, THIS WORKS AND NOBODY TOLD ME
        # yield int(front,2).to_bytes(1, byteorder='big', signed=False)
        # yield int(end, 2).to_bytes(1, byteorder='big', signed=False)

        yield front_byte
        yield end_byte


def mm_decode(source: Generator[bytes, None, None]) -> Generator[bytes, None, None]:
    for byte in source:

        # front_int = decode(byte)
        # end_int = decode(next(source))
        front_int = int.from_bytes(byte, byteorder='big')
        end_int = int.from_bytes(next(source), byteorder='big')

        front_list = list(bin(front_int)[2:].zfill(8))
        end_list = list(bin(end_int)[2:].zfill(8))

        inter_table = [front_list[:4], front_list[4:], end_list[:4], end_list[4:]]
        dec_front, dec_end = [], []

        for i in range(4):
                for j in range(4):
                        if i < 2:
                                dec_front.append(inter_table[j][i])
                        else:
                                dec_end.append(inter_table[j][i])
        
        front_int = decode(int(''.join(dec_front), 2))
        end_int = decode(int(''.join(dec_end), 2))

        #putting it back together
        ges = front_int << 4
        ges = ges + end_int
        erg = ges.to_bytes(1, byteorder='big', signed=False)
        yield erg
        

# gets int as input, return hammingcode of x as string
def ham74(x):
        test1 = x & 13          #1101
        p1 = count1(test1) % 2

        test2 = x & 11          #1011
        p2 = count1(test2) % 2

        test3 = x & 7           #0111
        p3 = count1(test3) % 2

        binx = bin(x)[2:].zfill(4)
        code = str(p1) + str(p2) + binx[0] + str(p3) + binx[1:]

        # return string representation
        return '0' + code 

# gets int as input and counts amount of 1 in bin(x)
def count1(x):
        return bin(x).count('1')

def originalBytes(x):
        binrep = bin(x)[2:].zfill(8)
        binx = binrep[3] + binrep[5:]
        binx = int(binx, 2)
        return binx

def decode(x):
        #x = int.from_bytes(byte, byteorder='big')
        
        #Calculate s1, s2 and s3
        t1 = x & 0b01010101
        s1 = count1(t1) % 2

        t2 = x & 0b00110011
        s2 = count1(t2) % 2

        t3 = x & 0b00001111
        s3 = count1(t3) % 2
        if (s1+s2+s3) == 0:
                # no error detected
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
                return originalBytes(intrep)