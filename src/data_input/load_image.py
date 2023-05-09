from PIL import Image
import numpy as np

def load_image(image_path, mode="RGB", scale=None):
  """
  Loads image in the specified image mode, returns numpy array
  
  Parameters
  ----------
  image_path : :obj:`str`
      File path to image.
  mode : :obj:`str`
      PIL.Image mode to use; default='RGB'.
  scale : :obj:`int`, :obj:`tuple`, or :obj:`None`, `optional`
      Scale to resize image; if :obj:`int`, will resize to (scale, scale); if :obj:`None`, will not resize.
  
  Returns
  -------
  numpy.array
      Image array.
  """
  img = Image.open(image_path)
  if img.mode != mode:
    img = img.convert(mode)
  if scale != None:
    if type(scale) == int: #resize to square image
      img = img.resize((scale, scale))
    elif type(scale) == tuple:
      img = img.resize(scale)
    else:
      raise Exception(f"scale should be of type int, tuple, or None, not {type(scale)}")
  return np.asarray(img)