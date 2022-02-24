import os
from plantcv import plantcv as pcv

# input parameter
num = 25 # initial mask image number
input_path = 'D:\PhD in Agriculture\code\crown rot GAN\data\infection'
save_dir = 'D:\PhD in Agriculture\code\crown rot GAN\processed_data/infection'
doc_list = os.listdir(input_path)

for i in doc_list:
    sav_image = str(num) + '_masked.png'
    pcv.params.debug = 'plot'
    class options:
        def __init__(self):
            self.image = input_path + '/' + i
            # self.debug = "plot"
            self.writeimg = False
            self.result = "vis_tutorial_results.json"
            # self.outdir = save_dir  # Store the output to the current directory


    # Get options
    args = options()

    # Set debug to the global parameter
    # pcv.params.debug = args.debug (觉得是否检查照片)

    # Get the image
    img, path, filename = pcv.readimage(filename=args.image)  # figure 1

    # Get the HSV result
    s = pcv.rgb2gray_hsv(rgb_img=img, channel='s')  # figure 2
    s_thresh = pcv.threshold.binary(gray_img=s, threshold=120, max_value=255, object_type='light')  # figure 3
    # Median Blur for cleaning the noise
    s_mblur = pcv.median_blur(gray_img=s_thresh, ksize=5)  # figure 4
    # Get the LAB result
    b = pcv.rgb2gray_lab(rgb_img=img, channel='b')  # figure 5
    # Second threshold based on "blue-yellow" (155)
    b_thresh = pcv.threshold.binary(gray_img=b, threshold=155, max_value=255,
                                    object_type='light')  # figure 6
    # Combining (1) the both threshold b and s
    combination1 = pcv.logical_or(bin_img1=s_mblur, bin_img2=b_thresh)  # figure 7
    # first mask for the combination 'b' and 's'
    masked = pcv.apply_mask(img=img, mask=combination1, mask_color='white')  # figure 8
    # extract the 'Green-Magenta' and 'Blue-Yellow' channels
    masked_a = pcv.rgb2gray_lab(rgb_img=masked, channel='a')  # figure 9
    masked_b = pcv.rgb2gray_lab(rgb_img=masked, channel='b')  # figure 10

    # threshold for the 'a' = 'Green-Magenta'
    maskeda_thresh = pcv.threshold.binary(gray_img=masked_a, threshold=125,
                                          max_value=255, object_type='dark')  # figure 11
    # threshold for the 'a' = 'Green-Magenta'
    maskeda_thresh1 = pcv.threshold.binary(gray_img=masked_a, threshold=130,
                                           max_value=255, object_type='light')  # figure 12
    # threshold for the 'b' = 'Blue-Yellow' (same to fig 6)
    maskedb_thresh = pcv.threshold.binary(gray_img=masked_b, threshold=155,
                                          max_value=255, object_type='light')  # figure 13
    # combination 2
    ab1 = pcv.logical_or(bin_img1=maskeda_thresh, bin_img2=maskedb_thresh)  # figure 14
    ab = pcv.logical_or(bin_img1=maskeda_thresh1, bin_img2=ab1)  # figure 15

    opened_ab = pcv.opening(gray_img=ab)  # figure 16
    # Fill small objects (reduce image noise) requiring 200 to 3500
    ab_fill = pcv.fill(bin_img=ab, size=25000)  # figure 17
    closed_ab = pcv.closing(gray_img=ab_fill)  # figure 18
    # applying second mask
    pcv.params.debug = 'print'  # 存储图像
    pcv.params.debug_outdir = save_dir
    masked2 = pcv.apply_mask(img=masked, mask=ab_fill, mask_color='white')  # figure 19
    process_image = save_dir + '/' + sav_image
    save_image = save_dir + '/' + i
    os.rename(process_image, save_image)
    num += 25
    print(i)
    print('done !')

print('All done !!!')