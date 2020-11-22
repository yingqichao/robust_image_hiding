import torch
import torch.nn as nn
from noise_layers.crop import get_random_rectangle_inside


class Cropout(nn.Module):
    """
    Combines the noised and cover images into a single image, as follows: Takes a crop of the noised image, and takes the rest from
    the cover image. The resulting image has the same size as the original and the noised images.
    """
    def __init__(self, height_ratio_range=(0.2,0.5), width_ratio_range=(0.2,0.5)):
        super(Cropout, self).__init__()
        self.height_ratio_range = height_ratio_range
        self.width_ratio_range = width_ratio_range

    def forward(self, noised_image, cover_image):
        # noised_image = noised_and_cover[0]
        # cover_image = noised_and_cover[1]
        print("Cropout Attack Added")
        self.name = "Cropout"
        assert noised_image.shape == cover_image.shape

        cropout_mask = torch.zeros_like(noised_image)
        h_start, h_end, w_start, w_end, _ = get_random_rectangle_inside(image=noised_image,
                                                                     height_ratio_range=self.height_ratio_range,
                                                                     width_ratio_range=self.width_ratio_range)
        cropout_mask[:, :, h_start:h_end, w_start:w_end] = 1

        noised_image = noised_image * (1-cropout_mask) + cover_image * cropout_mask
        return  noised_image