# This app will encode or decode text messages in an image file.
# The app will use RGB channels so only PNG files will be accepted.
# This technique will focus on Least Significant Bit (LSB) encoding.

from PIL import Image
import os

def encode(img, msg):
  # Convert each character to binary and store in LSB of image pixels
  pixels = img.load()
  width, height = img.size
  letterSpot = 0
  pixel = 0
  letterBinary = ""
  msgLength = len(msg)
  red, green, blue = pixels[0, 0]
  pixels[0, 0] = (msgLength, green, blue)  # Store message length in red channel of first pixel

  for i in range(msgLength * 3):
    x = i % width
    y = i // width

    red, green, blue = pixels[x, y]
    redBinary = numberToBinary(red)
    greenBinary = numberToBinary(green)
    blueBinary = numberToBinary(blue)

    if pixel % 3 == 0:
      letterBinary = numberToBinary(ord(msg[letterSpot]))
      greenBinary = greenBinary[0:7] + letterBinary[0]
      blueBinary = blueBinary[0:7] + letterBinary[1]
    elif pixel % 3 == 1:
      redBinary = redBinary[0:7] + letterBinary[2]
      greenBinary = greenBinary[0:7] + letterBinary[3]
      blueBinary = blueBinary[0:7] + letterBinary[4]
    else:
      redBinary = redBinary[0:7] + letterBinary[5]
      greenBinary = greenBinary[0:7] + letterBinary[6]
      blueBinary = blueBinary[0:7] + letterBinary[7]
      letterSpot += 1

    red = binaryToNumber(redBinary)
    green = binaryToNumber(greenBinary)
    blue = binaryToNumber(blueBinary)
    pixels[x, y] = (red, green, blue)
    pixel += 1

  img.save("secretImg.png", 'png')

def decode(img):
  msg = ""
  pixels = img.load()
  red, green, blue = pixels[0, 0]
  msgLength = red
  width, height = img.size
  pixel = 0
  letterBinary = ""
  x = 0
  y = 0

  while len(msg) < msgLength:
    red, green, blue = pixels[x, y]
    redBinary = numberToBinary(red)
    greenBinary = numberToBinary(green)
    blueBinary = numberToBinary(blue)

    if pixel % 3 == 0:
      letterBinary = greenBinary[7] + blueBinary[7]
    elif pixel % 3 == 1:
      letterBinary += redBinary[7] + greenBinary[7] + blueBinary[7]
    else:
      letterBinary += redBinary[7] + greenBinary[7] + blueBinary[7]
      letterAscii = binaryToNumber(letterBinary)
      msg += chr(letterAscii)

    pixel += 1
    x = pixel % width
    y = pixel // width

  return msg

# Helper Functions

def numberToBinary(num):
  """Takes a base10 number and converts to a binary string with 8 bits"""
  binary = bin(num)[2:]  # strip the '0b' prefix
  while len(binary) < 8:
    binary = '0' + binary
  return binary

def binaryToNumber(binStr):
  """Takes a string binary value and converts it to a base10 integer."""
  decimal = 0
  for i in range(len(binStr)):
    if binStr[-(i+1)] == '1':
      decimal += 2 ** i
  return decimal

def main():
  choice = input("Do you want to (e)ncode or (d)ecode? ").lower()
  filename = input("Enter the image filename (PNG format): ")

  if not os.path.exists(filename):
    print("File not found.")
    return

  if not filename.lower().endswith(".png"):
    print("Only PNG files are supported.")
    return

  img = Image.open(filename)

  if choice == 'e':
    msg = input("Enter the message to hide: ")
    encode(img, msg)
    print("Message encoded and saved as 'secretImg.png'.")
  elif choice == 'd':
    decodedMsg = decode(img)
    print("Decoded message:", decodedMsg)
  else:
    print("Invalid option. Choose 'e' for encode or 'd' for decode.")
  img.close()

if __name__ == '__main__':
  main()