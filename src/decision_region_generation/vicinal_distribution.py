import numpy as np
from PIL import Image, ImageOps

def get_plane(img1, img2, img3):
    ''' 
    Calculate the plane (basis vecs) spanned by 3 images
    
    Parameters
    ----------
    img1, img2, img3 : numpy.array
        Three numpy arrays of images; must all be the same size.
        
    Returns
    -------
    a, b_orthog : numpy.array
        2 orthogonal basis vectors for the plane spanned by the input images
    b : numpy.array
        The second basis vecotr, before being made orthogonal
    coords : list
        Coordinates of img0, img1, and img2    
    '''
    if not img1.shape == img2.shape == img3.shape:
      raise Exception(f"All input images must be the same shape, got shapes: {img1.shape}, {img2.shape}, {img3.shape}")
    a = (img2 - img1).astype("float")
    b = (img3 - img1).astype('float')
    a_norm = np.sqrt(np.dot(a.flatten(), a.flatten()))
    a = a / a_norm
    first_coef = np.dot(a.flatten(), b.astype('float').flatten())
    b_orthog = b - first_coef * a
    b_orthog_norm = np.sqrt(np.dot(b_orthog.flatten(), b_orthog.flatten()))
    b_orthog = b_orthog / b_orthog_norm
    second_coef = np.dot(b.flatten(), b_orthog.flatten())
    coords = [[0,0], [a_norm,0], [first_coef, second_coef]]
    return a, b_orthog, b, coords


class plane_dataset():
    def __init__(self, img1, img2, img3, steps=5, expand=0, shape='rectangle', dtype='uint8'):
        if img1.dtype == 'uint8':
            img1 = img1/255
            img2 = img2/255
            img3 = img3/255
        self.base_image_mean = np.average(np.stack([img1, img2, img3]), (0,1,2))
        self.base_image_std = np.std(np.stack([img1, img2, img3]), (0,1,2))
        self.dtype = dtype
        self.shape = shape
        self.steps = steps
        self.original_images = [img1, img2, img3]
        self.vec1, self.vec2, _, self.coords = get_plane(img1, img2, img3)
        self.base_img = img1.astype(float)
        x_bounds = [coord[0] for coord in self.coords]
        y_bounds = [coord[1] for coord in self.coords]
        self.bound1 = [np.min(np.array(x_bounds)), np.max(np.array(x_bounds))]
        self.bound2 = [np.min(np.array(y_bounds)), np.max(np.array(y_bounds))]
        len1 = self.bound1[-1] - self.bound1[0]
        len2 = self.bound2[-1] - self.bound2[0]
        list1 = np.linspace(self.bound1[0] - expand*len1, self.bound1[1] + expand*len1, steps)
        list2 = np.linspace(self.bound2[0] - expand*len2, self.bound2[1] + expand*len2, steps)
        grid0, grid1 = np.meshgrid(list1, list2, indexing='ij')
        self.coefs1 = grid0.flatten()
        self.coefs2 = grid1.flatten()
        if self.shape == 'triangle':
            line_1 = (self.coords[2][1]-self.coords[0][1])/(self.coords[2][0]-self.coords[0][0])
            line_2 = (self.coords[2][1]-self.coords[1][1])/(self.coords[2][0]-self.coords[1][0])
            # reduce results to those in the convex hull between the three original images' coordinates
            condition_1 = np.logical_and(self.coefs1 < self.coords[2][0], self.coefs2 < line_1*self.coefs1)
            condition_2 = np.logical_and(self.coefs1 >= self.coords[2][0], self.coefs2 < line_2*(self.coefs1 - self.coords[2][0]) + self.coords[2][1])
            shape_arr = np.logical_or(condition_1, condition_2)
            self.coefs1 = self.coefs1[shape_arr]
            self.coefs2 = self.coefs2[shape_arr]
    
    def __len__(self):
        return self.coefs1.shape[0]

    def __getitem__(self, idx):
        return self.normalize(self.base_img + self.coefs1[idx]*self.vec1 + self.coefs2[idx]*self.vec2)
        
    def get_coords(self, idx):
        return self.coefs1[idx], self.coefs2[idx]

    def normalize(self, img):
        if len(self.base_img.shape) == 3:
            for c in range(self.base_img.shape[-1]):
                img[:,:,c] = (img[:,:,c] - self.base_image_mean[c])/self.base_image_std[c]
                img[:,:,c] = img[:,:,c] - img[:,:,c].min()
                img[:,:,c] = img[:,:,c] / img[:,:,c].max()
        return img

    def view_vicinal(self, background='black', border_original=True):
        original_border_color = 'red'
        original_border_thickness = 10
        img_w = self.steps*self.base_img.shape[0]
        img_h = self.steps*self.base_img.shape[1]
        max_x = max(list(self.coefs1) + [x[0] for x in self.coords])
        max_y = max(list(self.coefs2) + [y[1] for y in self.coords])
        new_img = Image.new('RGB', (img_w+self.base_img.shape[0], img_h+self.base_img.shape[1]), color=background) # TODO: check if can paste non RGB imgs on RGB
        # paste all of the vicinal images
        for i in range(len(self)):
            img = Image.fromarray((self[i]*255).astype('uint8'))
            x = self.get_coords(i)[0]
            y = self.get_coords(i)[1]
            x0 = int( (x/max_x)*img_w )
            y0 = int( img_h - (y/max_y)*img_h )
            new_img.paste(img, (x0,y0, x0+img.size[0], y0+img.size[1]))
        # paste the original images
        for i in range(3):
            img = Image.fromarray((self.original_images[i]*255).astype('uint8'))
            x = self.coords[i][0]
            y = self.coords[i][1]
            x0 = int( (x/max_x)*img_w )
            y0 = int( img_h - (y/max_y)*img_h )
            if border_original:
                img = ImageOps.expand(img, original_border_thickness, original_border_color)
            new_img.paste(img, (x0,y0))
        return new_img
