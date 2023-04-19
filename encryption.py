import sys
import random
import json
import re
import base64
from AES import AES
from ECC import ECC
from DataConvert import converter
# from PIL import Image

def findAesKey(mes, keySize):
    key = converter.base64ToValue(mes[0:int(keySize/2)])
    print(len(key))
    print(key)
    return int(key)

def findEccPublicKey(EccPrivateKey):
    ecc_obj_AESkey = ECC.ECC()
    public_key = ecc_obj_AESkey.gen_pubKey(EccPrivateKey)
    return public_key

def main(EccPublicKey, keySize, partNum):
    print("="*70)
    print("  Please enter the name of file to encrypt present in ./test_files/")
    print("="*70)
    input_file = input(
        "Enncrypt : ")
    file_type = input_file.split(".")[1]
    output_file = "test."+file_type

    # 1. Multimedia data -> Base64 Encoding and plain text
    multimedia_data = converter.fileToBase64("test_files/" + input_file)

    # keySize partNum encryption!
    ecc = ECC.ECC()
    (C1_KeySize, C2_KeySize) = ecc.encryption(EccPublicKey, str(KeySize))



    # 2. break message into many parts and get related keys
    messageBox = []
    keyBox = []
    keyBox.append(EccPublicKey)

    singleLen = int(len(multimedia_data)/partNum)+1
    for i in range(0, partNum):
        mi = multimedia_data[i*singleLen: (i+1)*singleLen]
        messageBox.append(mi)
        keyBox.append(findAesKey(mi, keySize))

    # 3. encrypt the first message part m1 with ECC public key
    # ecc = ECC.ECC()
    (C1_multimedia, C2_multimedia) = ecc.encryption(EccPublicKey, messageBox[0])


    # 4. use keys in keyBox to encrypt other messages
    aesMessageBox = []
    for i in range(1, partNum):
        aes = AES.AES(keyBox[i])
        encrypted_multimedia = aes.encryptBigData(messageBox[i])
        aesMessageBox.append(encrypted_multimedia)

    # 5. write into cipher, save the json file
    cipher = {
        "file_type": file_type,
        # "KeySize": KeySize,
        "C1_KeySize":C1_KeySize,
        "C2_KeySize":C2_KeySize,
         "PartNum":PartNum,
        "C1_multimedia": C1_multimedia,
        "C2_multimedia": C2_multimedia,
    }
    for i in range(0,len(aesMessageBox)):
        cipher["AesMessagePart" + str(i+2)] = aesMessageBox[i]

    b = json.dumps(cipher)
    f2 = open('cipher.json', 'w')
    f2.write(b)
    f2.close()

    print("====================")
    print("Encryption Succeeded")
    print("====================")
    print()


if __name__ == "__main__":
    privateKeyECC=59450895769729158456103083586342075745962357150281762902433455229297926354304
    publicKeyEcc = findEccPublicKey(privateKeyECC)
    KeySize = 35
    PartNum = 5
    main(publicKeyEcc, KeySize, PartNum)