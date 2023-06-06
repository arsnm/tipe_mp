import numpy as np
import encoder
import sys, os
from pathlib import Path
from PIL import Image
import cv2
import pandas as pd
import time as t
import shutil
import utils
import matplotlib.pyplot as plt
from encoder import DCT, padding
from scipy.fftpack import dct

LIM = 25  # number of files to test to


def compare(
    quality=None,
    dataDirectory=None,
    outputDirectory=None,
    subsample=None,
    useStdHuffmanTable=None,
    DeleteFilesAfterward=True,
):
    if quality is None:
        quality = np.random.randint(0, 101)
    if subsample is None:
        subsample = "4:2:2"
    if dataDirectory is None:
        dataDirectory = "./data/datasetBmp"
    if useStdHuffmanTable is None:
        useStdHuffmanTable = False
    outputDirectory = f"./data/treated/quality{quality}-subsample{subsample}-stdHf{useStdHuffmanTable}"
    i = 0
    stat = np.zeros(
        (LIM, 3), dtype=object
    )  # first parameter is size before compression, second after, and third the time to achieve compression
    for filename in os.listdir(dataDirectory):
        if i >= LIM:
            break
        f = os.path.join(dataDirectory, filename)
        if not os.path.exists(outputDirectory):
            os.makedirs(outputDirectory)
        f_out = os.path.join(outputDirectory, filename + ".jpg")
        if os.path.isfile(f):
            previousSize = os.stat(f).st_size
            image = Image.open(f)
            time = t.time_ns()
            encoder.write_jpeg(
                f_out, np.array(image), quality, subsample, useStdHuffmanTable
            )
            time = t.time_ns() - time
            newSize = os.stat(f_out).st_size
            stat[i][0] = previousSize
            stat[i][1] = newSize
            stat[i][2] = time
        i += 1
    if DeleteFilesAfterward:
        shutil.rmtree(outputDirectory)
    write_stat("./data/treated/stat.txt", stat, quality, subsample, useStdHuffmanTable)


def write_stat(statFile, stat, quality, subsample, standHuffTables):
    with open(statFile, "a+") as f:
        f.write("\n" * 2)
        f.write("New sample \n")
        f.write(f"Size of sample : {LIM} images \n")
        f.write(
            f"Parameters of compression : (quality) {quality}, (subsample) {subsample}, (usage of standard HuffTables) {'Yes' if standHuffTables else 'No'} \n"
        )
        avgPreviousSize = np.average(stat[:, 0])
        avgNewSize = np.average(stat[:, 1])
        f.write(
            f"Average size of image before compression : {avgPreviousSize} bytes \n"
        )
        f.write(f"Average size of images after compression : {avgNewSize} bytes \n")
        f.write(f"Ratio is {avgPreviousSize / avgNewSize:.2f}")


def write_stat_csv(outputDirectory, stat, quality, subsample, standHuffTables):
    pass

def energyCompaction(imgPath):
    img = cv2.imread(imgPath)

    imgYCrCB = cv2.cvtColor(
        img, cv2.COLOR_RGB2YCrCb
    )  # Convert RGB to YCrCb (Cb applies V, and Cr applies U).

    Y, Cr, Cb = cv2.split(padding(imgYCrCB, 8, 8))
    Y = Y.astype('int') - 128
    blocks_Y = utils.divide_blocks(Y, 8, 8)
    dctBlocks_Y = np.zeros_like(blocks_Y)
    for i in range(len(blocks_Y)):
        dctBlocks_Y[i] = dct(dct(blocks_Y[i], axis=0, norm="ortho"), axis=1, norm="ortho")
    avg_Y = utils.averageMatrix(blocks_Y)
    avgDct_Y = utils.averageMatrix(dctBlocks_Y)

    x = np.random.randint(blocks_Y.shape[0])
    arr1 = blocks_Y[x]
    arr2 = dctBlocks_Y[x]

    fig, (ax1, ax2 )= plt.subplots(1, 2)

    valueMax, valueMin = max(np.max(arr1), np.max(arr2)), min(np.min(arr1), np.min(arr2))
    # fig.suptitle('Matrice de la luminance de "villeLyon.jpg"')

    ax1.matshow(arr1, cmap="cool", vmin=valueMin, vmax=valueMax)
    ax1.set_title('avant DCT')

    ax2.matshow(arr2, cmap="cool", vmin=valueMin, vmax=valueMax)
    ax2.set_title('après DCT')
    
    
    for i in range(arr1.shape[0]):
        for j in range(arr1.shape[1]):
            cNormal= int(arr1[i, j])
            cDct = int(arr2[i, j])
            ax1.text(i, j, str(cNormal), va='center', ha='center')
            ax2.text(i, j, str(cDct), va='center', ha='center')
    plt.savefig('./data/energyCompaction.png', transparent=True)


def rgbToYCbCr_channel_bis():
    img = cv2.imread("./data/villeLyon.jpg")  # Read input image in BGR format

    imgYCrCB = cv2.cvtColor(
        img, cv2.COLOR_BGR2YCrCb
    )  # Convert RGB to YCrCb (Cb applies V, and Cr applies U).

    Y, Cr, Cb = cv2.split(imgYCrCB)

    # Fill Y and Cb with 128 (Y level is middle gray, and Cb is "neutralized").
    onlyCr = imgYCrCB.copy()
    onlyCr[:, :, 0] = 128
    onlyCr[:, :, 2] = 128
    onlyCr_as_bgr = cv2.cvtColor(
        onlyCr, cv2.COLOR_YCrCb2BGR
    )  # Convert to BGR - used for display as false color

    # Fill Y and Cr with 128 (Y level is middle gray, and Cr is "neutralized").
    onlyCb = imgYCrCB.copy()
    onlyCb[:, :, 0] = 128
    onlyCb[:, :, 1] = 128
    onlyCb_as_bgr = cv2.cvtColor(
        onlyCb, cv2.COLOR_YCrCb2BGR
    )  # Convert to BGR - used for display as false color

    cv2.imshow("img", img)
    cv2.imshow("Y", Y)
    cv2.imshow("onlyCb_as_bgr", onlyCb_as_bgr)
    cv2.imshow("onlyCr_as_bgr", onlyCr_as_bgr)
    cv2.waitKey()
    cv2.destroyAllWindows()

    cv2.imwrite("./data/treated/villeLyon_Y.jpg", Y)
    cv2.imwrite("./data/treated/villeLyon_Cb.jpg", onlyCb_as_bgr)
    cv2.imwrite("./data/treated/villeLyon_Cr.jpg", onlyCr_as_bgr)


if __name__ == "__main__":
    # compare()
    # rgbToYCbCr_channel_bis()
    energyCompaction("./data/villeLyon.jpg")
    test = np.array([[93, 90, 83, 68, 61, 61, 46, 21],
                    [102, 92, 95, 77, 65, 60, 49, 32],
                    [69, 55, 47, 57, 65, 60, 72, 65],
                    [55, 55, 40, 42, 23, 1, 11, 38],
                    [55, 57, 47, 53, 35, 59, -2, 26],
                    [64, 41, 42, 55, 60, 57, 25, -8],
                    [77, 87, 58, -2, -5, 14, -10, -35],
                    [38, 14, 33, 33, -21, -23, -43, -34]])
    print(dct(dct(test, axis=0, norm="ortho"), axis=1, norm='ortho'))