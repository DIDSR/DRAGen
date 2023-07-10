from PIL import Image
import numpy as np
from typing import Optional

def load_image(image_path, mode:str="RGB", scale:Optional[int|tuple[int]]=None)->np.array:
  """
  Loads image in the specified image mode.
  
  Parameters
  ----------
  image_path
      File path to image.
  mode
      [PIL.Image mode](https://pillow.readthedocs.io/en/stable/handbook/concepts.html#modes) to use.
  scale
      Scale to resize image; if ``int``, will resize to (scale, scale); if ``None``, will not resize.
  
  Returns
  -------
  numpy.array
      Image array.

  Raises
  ======
  Exception
    The provided scale is not in a supported format
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