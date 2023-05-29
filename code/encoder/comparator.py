import numpy as np
import encoder
import sys, os
from pathlib import Path
from PIL import Image

LIM = 25 # number of files to test tos


def write_stat(statFile, stat, quality, subsample, standHuffTables):
    with open(statFile, 'a+') as f:
        f.write("\n" * 2)
        f.write("New sample \n")
        f.write(f"Size of sample : {LIM} images \n")
        f.write(f"Parameters of compression : (quality) {quality}, (subsample) {subsample}, (usage of standard HuffTables) {'Yes' if standHuffTables else 'No'} \n")
        avgPreviousSize = np.average(stat[:, 0])
        avgNewSize = np.average(stat[:, 1])
        f.write(f"Average size of image before compression : {avgPreviousSize} bytes \n")
        f.write(f"Average size of images after compression : {avgNewSize} bytes \n")
        f.write(f"Ratio is {avgPreviousSize / avgNewSize:.2f}")
        

if __name__ == "__main__":
    quality = np.random.randint(0, 101)
    subsample = "4:2:2"
    directory = "./data/datasetBmp"
    output_directory = f'./data/treated/quality{quality}-subsample{subsample}'
    i = 0
    stat = np.zeros((LIM, 2), dtype=object)
    for filename in os.listdir(directory):
        if i >= LIM:
            break
        f = os.path.join(directory, filename)
        if not os.path.exists(output_directory):
            os.makedirs(output_directory)
        f_out = os.path.join(output_directory, filename + ".jpg")
        if os.path.isfile(f):
            previousSize = os.stat(f).st_size
            image = Image.open(f)
            encoder.write_jpeg(f_out, np.array(image), quality, subsample, False)
            newSize = os.stat(f_out).st_size
            stat[i][0] = previousSize
            stat[i][1] = newSize
        i += 1
    write_stat("./data/treated/stat.txt", stat, quality, subsample, False)
