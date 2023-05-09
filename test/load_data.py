import sys
sys.path.append('../')
from src.data_input.load_image import load_image
from src.data_input.load_attributes import load_attributes
import matplotlib.pyplot as plt
from PIL import Image


if __name__ == "__main__":
  # testing loading images
  #test_fp = "/gpfs_projects/ravi.samala/OUT/2022_CXR/data_summarization/20221010/20221010_open_A1_jpegs/10003752-gxbvm8keQkKPhXpbHo8GQ_0.jpg"
  #img_arr = load_image(test_fp, scale=320)
  #print(img_arr.shape)
  #print(type(img_arr))
  #fig, ax = plt.subplots(figsize=(4,4))
  #plt.imshow(img_arr)
  #ax.axis('off')
  #plt.tight_layout()
  #plt.savefig("/gpfs_projects/alexis.burgon/OUT/2022_CXR/temp/test.svg")
  #plt.close('all')
  # testing loading attributes
  test_fp = "/gpfs_projects/alexis.burgon/OUT/2022_CXR/model_runs/open_A1_scenario_1_v4/1_step_all_CR_stratified/RAND_0/step_0_validation.csv"
  subgroup_information = {"test_attribute":["F", "M"]}
  df = load_attributes(test_fp, subgroup_information=subgroup_information, id_column='patient_id')
  print(df.head(2))
  #print(df)
  
  