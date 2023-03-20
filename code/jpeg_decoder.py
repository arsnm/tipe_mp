import numpy as np
from collections import deque, namedtuple
from itertools import product
from math import ceil, cos, pi
from scipy.interpolate import griddata
from typing import Callable, Tuple, Union
from pathlib import Path

# JPEG markers (for our supported segments)
SOI  = bytes.fromhex("FFD8")    # Start of image
SOF0 = bytes.fromhex("FFC0")    # Start of frame (Baseline DCT)
SOF2 = bytes.fromhex("FFC2")    # Start of frame (Progressive DCT)
DHT  = bytes.fromhex("FFC4")    # Define Huffman table
DQT  = bytes.fromhex("FFDB")    # Define quantization table
DRI  = bytes.fromhex("FFDD")    # Define restart interval
SOS  = bytes.fromhex("FFDA")    # Start of scan
DNL  = bytes.fromhex("FFDC")    # Define number of lines
EOI  = bytes.fromhex("FFD9")    # End of image

# Restart markers
RST = tuple(bytes.fromhex(hex(marker)[2:]) for marker in range(0xFFD0, 0xFFD8))

# Containers for the parameters of each color component
ColorComponent = namedtuple("ColorComponent", "name order vertical_sampling horizontal_sampling quantization_table_id repeat shape")
HuffmanTable = namedtuple("HuffmanTable", "dc ac")


class JPEGReader:
    def __init__(self, filename:Path):
        with open(filename, 'rb') as image:
            self.__file = image.read()
        self.fileSize = len(self.__file) #Size in bytes of the file
        self.filePath = filename if isinstance(filename, Path) else Path(filename)
        self.quantizationTable = [QuantizationTable()] * 4

        if not self.__file.startswith(SOI + b"\xFF"):
            raise NotJpeg("Error, the given file is not a JPEG ")
        print(f"Reading file '{filename.name}' ({self.fileSize:,} bytes)")

        self.handlers = {
            DHT: self.defineHuffmanTable,
            DQT: self.defineQuantizationTable,
            DRI: self.defineRestartInterval,
            SOF0: self.startFrame,
            SOF2: self.startFrame,
            SOS: self.startScan,
            EOI: self.endImage,
        }

        # Initialize decoding paramenters
        self.fileHeader= 2            # Offset (in bytes, 0-index) from the beginning of the file
        self.scanFinished= False      # If the 'end of image' marker has been reached
        self.scanMode= None           # Supported modes: 'baseline_dct' or 'progressive_dct'
        self.imageWidth = 0            # Width in pixels of the image
        self.imageHeight = 0           # Height in pixels of the image
        self.colorComponents = {}      # Hold each color component and its respective paramenters
        self.sampleShape = ()          # Size to upsample the subsampled color components
        self.huffmanTables = {}        # Hold all huffman tables
        self.quantizationTables = {}   # Hold all quantization tables
        self.restartInterval = 0       # How many MCUs before each restart marker
        self.imageArray = None         # Store the color values for each pixel of the image
        self.scanCount = 0             # Counter for the performed scans

        # Main loop to find and process the supported file segments
        while not self.scanFinished:
            try:
                current_byte = self.__file[self.fileHeader]
            except IndexError:
                del self.__file
                break

            # Whether the current byte is 0xFF
            if (current_byte == 0xFF):

                # Read the next byte
                segMarker = self.__file[self.fileHeader : self.fileHeader+2]
                self.fileHeader += 2

                # Whether the two bytes form a marker (and isn't a restart marker)
                if (segMarker != b"\xFF\x00") and (segMarker not in RST):

                    # Attempt to get the handler for the marker
                    segHandler = self.handlers.get(segMarker)
                    segSize = ((self.__file[self.fileHeader] << 8) + self.__file[self.fileHeader+ 1]) - 2
                    self.fileHeader += 2

                    if segHandler is not None:
                        # If a handler was found, pass the control to it
                        my_data = self.__file[self.fileHeader : self.fileHeader+segSize]
                        segHandler(my_data)
                    else:
                        # Otherwise, just skip the data segment
                        self.fileHeader += segSize
            
            else:
                # Move to the next byte if the current byte is not 0xFF
                self.fileHeader += 1

    
    def __str__ (self) -> str:
        
        # Print Quantization Table
        string = "DQT ========== \n"
        for i in range(4):
            if self.quantizationTable[i].set == True:
                string += f"Table ID : {i}\n"
                string += f"Table Data : \n"
                for j in range(64):
                    if j % 8 == 0:
                        string += '\n'
                    string += f"{self.quantizationTable[i].table[j]} "
            string += '\n'
        return string 
                    
    @classmethod
    def reader(self):
        starter = self.__file.read(2)
        if starter[0] != 0xFF or starter[1] != SOI:
            self.header = False
            print("Error, the given arguement is not a JPEG")
            return
        buffer_size = 2
        while self.header:
            buffer = self.__file.read(buffer_size)
            if len(buffer) != 2:
                print("Error - File ended prematurely")
                self.header = False
            
            if buffer[0] != 0xFF:
                print("Error - Expected a marker")
                self.header = False
            
            if buffer[1] == DQT:
                JPEGReader.readQuantizationTable(self)
            if APP0 <= buffer[1] <= APP15:
                JPEGReader.readAPPN(self) 

    @classmethod
    def readAPPN(self):
        print("Reading APPN Marker")
        length = (self.__file.read(1) << 8) + self.__file.read(1)
        self.__file.read(length - 2)

    @classmethod
    def readQuantizationTable(self):
        print("Reading DQT Marker")
        length = (self.__file.read(1) << 8) + self.__file.read(1)
        length -= 2
        while length > 0:
            tableInfo = self.__file.read(1)
            length -= 1
            tableID = tableInfo & 0x0F

            if tableID > 3:
                print(f"Error - Invalid quantization table id : {int(tableID)}")
                self.header = False
                return self
            self.quantizationTable[tableID].set = True
            
            if tableInfo >> 4 != 0:
                for i in range(64):
                    self.quantizationTable[tableID].table[i] = (self.__file.read(1) << 8) + self.__file.read(1)
                length -= 128
            else:
                for i in range(64):
                    self.quantizationTable[tableID].table[i] = self.__file.read(1)
                length -= 64
        if length != 0:
            print("Error - DQT invalid")
            self.header = False



class QuantizationTable:
    def __init__(self):
        self.table = [0] * 64
        self.set = False


# ----------------------------------------------------------------------------------------------------

# Decoder exceptions

class JpegError(Exception):
    """Parent of all other exceptions of this decoder."""


class NotJpeg(JpegError):
    """File is not a JPEG image."""

class CorruptedJpeg(JpegError):
    """Failed to parse the file headers."""

class UnsupportedJpeg(JpegError):
    """JPEG image is encoded in a way that our decoder does not support."""

# ---------------------------------------------------------------------------------------------------------------------

#Script :

if __name__ == "__main__":
    import sys
    # if len(sys.argv) < 2:
    #     print("Error - Invalid Argument")
    # else:
    #     try:
    #         for arg in sys.argv[1:]:
    #             decodedJPEG = JPEGReader(arg)
    #             print(decodedJPEG)
    #     except:
    #         print("Error - Something went wrong")
    decodedJPEG = JPEGReader("/Users/arsnm/Documents/cpge/mp/tipe_mp/code/data/image.jpg")
    print(decodedJPEG.reader())







                

        
         