from scipy import spatial
import constants_colors

class rgb2color():
    """
    conversion of hexadecimal colors to color name
    """
    def __init__(self, simple=True):
        """
        :param simple: default is True: convert to color with simple text

        """
        self.RGB = constants_colors.NUMPY_RGB_CONSTANT
        self.rgbtree = spatial.cKDTree(self.RGB, leafsize=100)
        if simple:
            self.hex_to_color_dict = constants_colors.HEXT_NAME_DICT_SIMPLE
        else:
            self.hex_to_color_dict = constants_colors.HEXT_NAME_DICT

    """
    Dictionary of colornames indexed by key_Hex:
    See https://bdhacker.wordpress.com/2010/02/27/python-tutorial-dictionaries-key-value-pair-maps-basics/
    """
    def hex2rgb(self, rgb):
        """
        :param rgb: convert hexadecimal color
        :return: numpy array of [0-255,0-255,0-255] representation
        """
        h = rgb.lstrip('#')
        return [int(h[i:i + 2], 16) for i in (0, 2, 4)]

    def rgb2color(self, rgb, convert=True):
        """

        :param rgb: list of hexidemical [0.1,0.1,0.1]
        :param convert: 0-1 to 0-255 representation
        :return: text name of colors
        """
        if convert:
            rgb = [round(x * 255) for x in rgb]
        nearest_rgb = (self.RGB[self.rgbtree.query(rgb, k=1)[1]])
        s = '#' \
            + format(nearest_rgb[0], 'x').zfill(2) \
            + format(nearest_rgb[1], 'x').zfill(2) \
            + format(nearest_rgb[2], 'x').zfill(2)
        color_hex = s.upper()  # "#8B7355"  # "#8B7355"
        try:
            color_name = self.hex_to_color_dict[color_hex]
        except:
            color_name = None
        return color_name


# def main():
#     myclass = rgb2color(simple=False)
#     print(myclass.rgb2color([0.1, 0.1, 0.1], convert=True))
#     for r in range(0, 255, 5):
#         for g in range(0, 255, 5):
#             for b in range(0, 255, 5):
#                 print(r, g, b)
#                 print(myclass.rgb2color([r, g, b]))


if __name__ == '__main__':
    main()
