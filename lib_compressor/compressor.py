from PIL import Image
import numpy as np
import warnings
from sklearn.cluster import MiniBatchKMeans

# default value
elbow_point = 64


class ImageCompressor:
    def __init__(self, image):
        self.image = image
        self.loaded_image = None
        self.height = None
        self.width = None
        self.channels = None
        self.img_data = None

    def load_image(self):
        self.loaded_image = Image.open(self.image)

    def calculate_image_size(self):
        self.width, self.height = self.loaded_image.size
        self.channels = len(self.loaded_image.getbands())

    def image_data_normalize(self):
        self.img_data = (np.array(self.loaded_image)) / 255.0
        self.img_data = self.img_data.reshape(
            self.height * self.width, self.channels)

    def k_means_compression(self):
        warnings.simplefilter('ignore')
        kmeans_clustering = MiniBatchKMeans(elbow_point)
        kmeans_clustering.fit(self.img_data)
        new_colors = kmeans_clustering.cluster_centers_[
            kmeans_clustering.predict(self.img_data)]
        compressed_image = new_colors.reshape(
            self.height, self.width, self.channels)
        compressed_image = Image.fromarray(
            np.uint8(compressed_image * 255.0)).convert('RGB')
        return compressed_image
