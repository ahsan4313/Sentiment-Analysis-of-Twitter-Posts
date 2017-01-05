import numpy as np
from PIL import Image
from os import path
import matplotlib.pyplot as plt
import random
from wordcloud import WordCloud, STOPWORDS

class Cloud:
    def __init__(self):
        d = path.dirname(__file__)
        mask = np.array(Image.open(path.join(d, "square.png")))
        text = open("allwords.txt").read()
        text = text.replace("HAN", "Han")
        text = text.replace("LUKE'S", "Luke")
        text=text.replace("AT_USER"," ")
        text=text.replace("URL"," ")
        text=text.replace("amp"," ")
        stopwords = set(STOPWORDS)
        stopwords.add("int")
        stopwords.add("ext")
        stopwords.add("AT_USER")
        stopwords.add("URL")
        wc = WordCloud(max_words=1000, mask=mask, stopwords=stopwords, margin=20,random_state=1).generate(text)
# store default colored image
        default_colors = wc.to_array()
        plt.title("Custom colors")
        plt.imshow(wc.recolor(color_func=grey_color_func, random_state=3))
        wc.to_file("a_new_hope.png")
        plt.axis("off")
        plt.figure()
        plt.title("Default colors")
        plt.imshow(default_colors)
        plt.axis("off")
        plt.show()
    def grey_color_func(word, font_size, position, orientation, random_state=None, **kwargs):
        return "hsl(0, 0%%, %d%%)" % random.randint(60, 100)