import os
import sys
import random
import json
from AES import AES
from ECC import ECC
from DataConvert import converter
import ast

def findAesKey(mes, keySize):
    key = converter.base64ToValue(mes[0:int(keySize/2)])
    return int(key)

def main(privateKeyECC):
    with open('cipher.json') as f:
        data = json.load(f)


    # 1. read json file
    C1_multimedia = data["C1_multimedia"]
    C2_multimedia = data["C2_multimedia"]
    # PartNum = data["PartNum"]
    # KeySize = data["KeySize"]
    C1_KeySize = data["C1_KeySize"]
    C2_KeySize = data["C2_KeySize"]
    PartNum=data["PartNum"]
    file_type = data["file_type"]
    cipherBox = []

    ecc_obj = ECC.ECC()
    # PartNum = int(ecc_obj.decryption(C1_PartNum, C2_PartNum, privateKeyECC))
    KeySize = int(ecc_obj.decryption(C1_KeySize, C2_KeySize, privateKeyECC))


    for i in range(0, PartNum-1):
        cipherBox.append(data["AesMessagePart" + str(i+2)])

    # 2. decrypt m1 with ECC
    # ecc_obj = ECC.ECC()
    messageECC = ecc_obj.decryption(C1_multimedia, C2_multimedia, privateKeyECC)

    # 3. find AES key from m1 and decrypt m2, then find key in m2 to decrypt m3 .....
    messageBox = []
    keyAES = findAesKey(str(max(C1_multimedia)-min(C1_multimedia)+C2_multimedia), KeySize)

    for i in range(0, PartNum-1):
        aes_obj = AES.AES(keyAES)
        decrypted_multimedia = aes_obj.decryptBigData(cipherBox[i])
        keyAES = findAesKey(str(sum(cipherBox[i])), KeySize)
        messageBox.append(decrypted_multimedia)

    # 4. put messageECC and messageBox together
    # totalMessage = converter.fileToBase64("success.txt")
    totalMessage = messageECC
    for i in messageBox:
        totalMessage = totalMessage + i

    # totalMessage = totalMessage + converter.fileToBase64("success.txt")

    print(totalMessage)

    output_file = "Decrypted_file." + file_type
    converter.base64ToFile(totalMessage, output_file)

    print("====================")
    print("Decryption Succeeded")
    print("====================")

    delete = int(input("Do you want to delete decrypted file?(Yes-1 No-0) : "))
    if (delete):
        os.remove(output_file)


if __name__ == "__main__":
    privateKeyECC = 59450895769729158456103083586342075745962357150281762902433455229297926354304
    main(privateKeyECC)