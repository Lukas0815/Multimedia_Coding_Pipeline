from typing import List, Generator


def mm_encode(source: Generator[bytes, None, None]) -> Generator[bytes, None, None]:
 
    for byte in source:
        # TODO: Do something sensible.
        work = int.from_bytes(byte, byteorder='big')       #give int representation of byte
        #split in 4 bit front and 4 bit end (both represented in int)
        front_int = work >> 4
        end_int = work & 15

        front = ham74(front_int)
        end = ham74(end_int)
      
        # print("1: ", bytes(int(front,2)))
        # print("2: ", int(front,2).to_bytes(1, byteorder='big', signed=False))

        # one can only return ONE byte. So yield twice. YES, THIS WORKS AND NOBODY TOLD ME
        yield int(front,2).to_bytes(1, byteorder='big', signed=False)
        yield int(end, 2).to_bytes(1, byteorder='big', signed=False)
        print("orginal: ", byte)


def mm_decode(source: Generator[bytes, None, None]) -> Generator[bytes, None, None]:
    for byte in source:

        # TODO: Do something sensible.
        front_int = decode(byte)
        end_int = decode(next(source))
        # print("byte: ", byte, "  next: ", next(source))

        #putting it back together
        ges = front_int << 4
        ges = ges + end_int
        erg = ges.to_bytes(1, byteorder='big', signed=False)
        print("rec: ", byte, " front: ", front_int, " end: ", end_int)
        print("rec: ", erg)
        yield erg
        

# gets int as input, return hammingcode of x as string
def ham74(x):
        test1 = x & 13          #1101
        p1 = count1(test1) % 2

        test2 = x & 11          #1011
        p2 = count1(test2) % 2

        test3 = x & 7           #0111
        p3 = count1(test3) % 2

        binx = bin(x)[2:]
        code = str(p1) + str(p2) + binx[0] + str(p3) + binx[1:]

        # return string representation
        return code 

# gets int as input and counts amount of 1 in bin(x)
def count1(x):
        return bin(x).count('1')

def originalBytes(x):
        binrep = bin(x)[2:].zfill(8)
        binx = binrep[3] + binrep[5:]
        binx = int(binx, 2)
        #return binx.to_bytes(1, byteorder='big', signed=False)
        return binx

def decode(byte):
        x = int.from_bytes(byte, byteorder='big')
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