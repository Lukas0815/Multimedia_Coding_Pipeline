from typing import List, Generator


def mm_encode(source: Generator[bytes, None, None]) -> Generator[bytes, None, None]:
    for byte in source:
        # TODO: Do something sensible.


        bits = byte2bit(byte)
        firstHam = ham74(bits[:4])
        lastHam = ham74(bits[4:])
        result = firstHam + lastHam
        hexres = hex(int(result, 2))
        print("byte: ", byte, "result: ", result, " hexres: ", hexres)
        yield result.encode("utf-8", "ignore")
        #yield hexres.encode()

def mm_decode(source: Generator[bytes, None, None]) -> Generator[bytes, None, None]:
    for byte in source:
        # TODO: Do something sensible.
        print("rec: ", byte)

        yield "a".encode()


#selfmade function
'''
Function takes a byte and converts it to bit
Prefix zeros are added to fill up to 8 bit
'''
def byte2bit(byte):
        #bits = bin(int(byte.hex(), 16))[2:]

        #Do NOT know if this is very slow... and this returns it as string
        return format(int(byte.hex(), 16), '08b')

def ham74(bits):
        p1mod = changeStr(bits, 3, "0")
        p1 = countOnes(p1mod) % 2
        
        p2mod = changeStr(bits, 2, "0")
        p2 = countOnes(p2mod) % 2

        p3mod = changeStr(bits, 1, "0")
        p3 = countOnes(p3mod) % 2

        erg = []
        erg.append(str(p1))
        erg.append(str(p2))
        erg.append(bits[0])
        erg.append(str(p3))
        erg.append(bits[1:])
        return ''.join(erg)

def countOnes(strbits):
#       counter = 0
#       for x in strbits:
#               if x == '1':
#                       counter += counter
#       return counter
        return strbits.count("1")

#Allow to alter the given string on given postion
def changeStr(originalStr ,pos, replace):
        pos -= 1
        newStr = []
        counter = 0
        for c in originalStr:
                if (counter == pos):
                        newStr.append(replace)
                        counter += 1
                        continue

                newStr.append(c)
                counter += 1
        #print(newStr)
        return ''.join(newStr)