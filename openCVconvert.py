import numpy as np
import encodeAndDecode as ed
import cv2
import importQKD
from qiskit import QuantumCircuit, execute, transpile, Aer, IBMQ
from qiskit.tools.jupyter import *
from qiskit.visualization import *
# from ibm_quantum_widgets import *
from random import getrandbits
import binascii

import sys
#numpy.set_printoptions(threshold=sys.maxsize)

np.seterr(invalid='ignore')
print("package imported")

# from qiskit_textbook.tools import array_to_latex
# Loading your IBM Quantum account(s)
print("loading IBM Quantum account")

# Users adjustable
provider = IBMQ.enable_account('dd8c461ba86616beebb9455030bf20f149e4882b8d27cd3d1e40f0d65e0a2b1d4dc5f90591e13d72b3bfcd583cb3f14154882a7afa58918e7cda3a95f4aaf191')
pic = "punk5822.png"
compare_key = 50  # how many bits to compare between bob and alice for detecting the eavesdropper.
eavesdropper_exits = False  # True or False
amount_of_qubits = 1000  # how many bits and bases does alice and bob have to generate.


# eavesdropper
def eavesdropper(eve_here, encoded_qubits):
    if eve_here:
        eve_bases = importQKD.eve_chooses_bases(len(encoded_qubits))
        eve_bits = importQKD.eve_measure(eve_bases, encoded_qubits, len(encoded_qubits))
        return encoded_qubits, eve_bits
    else:
        return encoded_qubits, None


# generate quantum key
def qkd(qubits, eve_exits, amount_of_compare_key):
    alice_bits = importQKD.AliceChooseBits(qubits)
    print("alice_bits", alice_bits)
    alice_bases = importQKD.AliceChooseBases(qubits)
    print("alice_bases", alice_bases)
    encoded_qubits = importQKD.EncodeClassicaltoQubits(alice_bases, alice_bits, qubits)

    # eavesdropper here
    eve = eavesdropper(eve_exits, encoded_qubits)
    eve_bits = eve[1]
    encoded_qubits = eve[0]

    bob_bases = importQKD.BobChooseBases(qubits)
    print("bob_bases", bob_bases)
    bob_bits = importQKD.BobMeasure(bob_bases, encoded_qubits, qubits)
    print("BobBits", bob_bits)
    agreeing_indices = importQKD.CompareBases(alice_bases, bob_bases)
    alice_key = importQKD.AliceCreateKey(agreeing_indices, alice_bits)
    bob_key = importQKD.BobCreateKey(agreeing_indices, bob_bits)
    if alice_key[:amount_of_compare_key] == bob_key[:amount_of_compare_key]:
        print("Same Key")
        print("part of alice key", alice_key[:amount_of_compare_key])
        print("part of bob key  ", bob_key[:amount_of_compare_key])
        return "Same key", alice_key, bob_key
    else:
        print("There is an eavesdropper")
        print("part of alice key", alice_key[:amount_of_compare_key])
        print("part of bob key  ", bob_key[:amount_of_compare_key])
        return "eve here", eve_bits


# input image
img = cv2.imread(pic)
print("inputted the image")

# encode
ImgBit = ed.encode(img)
print("encoded array to bits")

print("quantum key distribution:")

Key = qkd(amount_of_qubits, eavesdropper_exits, compare_key)
if Key[0] == "Same key":
    AliceKey = Key[1]
    BobKey = Key[2]
    print("Alice's Key" + str(AliceKey))
    print("Bob's Key" + str(BobKey))

    encrypted_message = importQKD.encrypt_message(ImgBit, AliceKey)
    decrypted_message = importQKD.decrypt_message(encrypted_message, BobKey)

    # decode
    decodeImg = ed.decode(decrypted_message)
    print(decodeImg)

    if (img == decodeImg).all():
        print("Alice and Bob get the same picture")
    else:
        print("something went wrong")
        print("Img"+str(img.tolist()))
        print("decodeImg"+str(decodeImg.tolist()))

    cv2.imwrite("/Users/leoluonew/Desktop/學習歷程/高二/多元學習/東華專題/量子加密/punk5822b.jpg", decodeImg, [cv2.IMWRITE_JPEG_QUALITY, 100])
else:
    pass
