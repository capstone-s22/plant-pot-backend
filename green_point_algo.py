import matplotlib.pyplot as plt
import itertools

from functools import reduce
import os
import numpy as np
import cv2
#from kmeans import kmeans_mass_function
from scipy.ndimage.filters import median_filter
from sklearn.cluster import KMeans
import time
import math

def kmeans_clustering(img, k=2):
    kmeans = KMeans(n_clusters=k).fit(img.flatten().reshape(-1, 1))
    cluster_centers = kmeans.cluster_centers_.squeeze(1)
    labels = kmeans.labels_
    labels = [cluster_centers[label] for label in labels]
    clustered_img = np.array(labels).reshape(img.shape)
    return clustered_img, cluster_centers, labels

def kmeans_mass_function(datapoints):
    kmeans_since = time.time()
    clustered_points, cluster_centers, labels = kmeans_clustering(datapoints)
    kmeans_duration = time.time() - kmeans_since
    print(f"Kmeans clustering ran for {kmeans_duration}s")

    gaussian_since = time.time()
    gaussian_datapoints_for_all_subset_clusters, cluster_set = convert_to_gaussian_for_all_subsets_in_clusters(datapoints, labels, cluster_centers)
    gaussian_conversion_duration = time.time() - gaussian_since
    print(f"Gaussian conversion ran for {gaussian_conversion_duration}s")
    #TODO: Do we really want to output the frame of discernment along with the mass function?
    return gaussian_datapoints_for_all_subset_clusters, cluster_set

def convert_to_gaussian_for_all_subsets_in_clusters(img, img_labels, clusters):
    '''
    Args:
        img: original image
        img_labels: image pixel elements are cluster index
        clusters: clusters of interest to convert to gaussian
    Returns:
        gaussian_img_for_all_subsets_windowed
        cluster_set: A.K.A frame of discernments
    '''
    # Combinations of cluster in clusters from i=1 to len(clusters)
    cluster_set = _set_combinations(clusters)

    # TODO: Is there a better way to index the clusters
    # img_labels = convert_labels2idx(img_labels, clusters)

    sigmas = {}
    means = {}
    gaussian_img_for_all_subsets = []
    for cs in cluster_set:
        gaussian_img, sigmas, means = convert_to_gaussian_for_subset(img.flatten().reshape(-1, 1), img_labels, cs, sigmas, means)
        gaussian_img_for_all_subsets.append(gaussian_img.reshape(img.shape))
    # TODO: separate window mean function?
    gaussian_img_for_all_subsets_windowed = [apply_window_mean(gaussian_img).reshape(-1, 1) for gaussian_img in gaussian_img_for_all_subsets]
    gaussian_img_for_all_subsets_windowed = np.stack(gaussian_img_for_all_subsets_windowed)
    return gaussian_img_for_all_subsets_windowed, cluster_set

def convert_to_gaussian_for_subset(img, img_labels, subset, sigmas, means):
    for s in subset:
        if sigmas.get(s) and means.get(s):
            mean = means.get(s)
            sigma = sigmas.get(s)
        else:
            img_s = get_pixels_from_img_with_index_s(img, img_labels, s)
            mean = np.mean(img_s)
            sigma = _standard_deviation(img_s, mean)
            means[s] = mean
            sigmas[s] = sigma
    means_for_compute = [means[s] for s in subset]
    sigmas_for_compute = [sigmas[s] for s in subset]
    img_gaussian = compute_gaussian_for_subset(img, means_for_compute, sigmas_for_compute)
    return img_gaussian, sigmas, means

def get_pixels_from_img_with_index_s(img, img_labels, idx):
    indices = np.where(img_labels != idx)
    pixels_with_index_s = np.delete(img, indices)
    return pixels_with_index_s

def compute_gaussian_for_subset(img, means, sigmas):
    subset_mean = np.mean(means)
    subset_sigma = np.max(sigmas)
    img_gaussian = gaussian_eqn(img, subset_mean, subset_sigma)
    return img_gaussian

def gaussian_eqn(datapoints, mean, sigma):
    gaussian = (1 / (sigma * math.sqrt(2 * math.pi))) * np.exp(-(datapoints - mean)**2 / (2*sigma**2))
    return gaussian

def apply_window_mean(img, window_size=3):
    offset = int((window_size - 1) / 2)
    H, W = img.shape
    H_prime, W_prime = H - 2*offset, W - 2*offset
    new_img = np.empty((H_prime, W_prime))
    for h in range(H_prime):
        for w in range(W_prime):
            window = img[h:h+window_size, w:w+window_size]
            new_img[h, w] = np.sum(window) / window.size
    return new_img

def _set_combinations(arr):
    all_subsets = []
    for i in range(1, len(arr)+1):
        all_subsets.extend(itertools.combinations(arr, i))
    return all_subsets

# def convert_labels2idx(labels, clusters):
#     for i, c in enumerate(clusters):
#         labels = np.where(labels == c, labels, i+1)
#     return labels

def _standard_deviation(datapoints, mean):
    sigma = np.sqrt(np.mean((datapoints - mean)**2))
    return sigma
def _build_frame_intersections(frame_of_discernments, set_dict):
    frame_intersections = []
    null_intersections = []
    for idx, frame in enumerate(frame_of_discernments.keys()):
        intersections = []
        for key, val in set_dict.items():
            if not val:
                null_intersections.append(key)
            elif set(frame) == val:
                intersections.append(key)
        frame_intersections.append(intersections)
    return frame_intersections, null_intersections

def _compute_mass_values(mass_function, info_sources):
    '''
    Args:
        mass_function: function to apply to all information
        info_sources: list of information from different sources
    Returns:
        numpy array of dim (number_of_subsets_in_frame, amount_of_info, info_sources_channel)
    '''
    mass_values_for_all_sources = []
    for source in info_sources:
        mass_values, _ = mass_function(source)
        mass_values_for_all_sources.append(mass_values.squeeze(2))
    mass_values = np.stack(mass_values_for_all_sources).transpose([1, 2, 0])
    return mass_values

def _construct_set_dict_from(frame_set, size):
    subsets = list(frame_set.keys())
    frame_grid = {}
    for combination in itertools.product(subsets, repeat=size):
        intersection = reduce((lambda x, y: set(x) & set(y)), combination)
        frame_grid[combination] = intersection
    return frame_grid

def dempster_shafer(mass_function, info_sources, frame_of_discernments):
    '''
    Args:
        mass_function: function object to calculate mass
        info_sources: list of information sources, information should be flattened to 1-dim array
        frame_of_discernments: a dictionary of {tuple(subset): int(index)}
    Return:
        numpy array of dim (number_of_subsets_in_frame, info_amount)
    '''
    mass_values = _compute_mass_values(mass_function, info_sources)
    set_dict = _construct_set_dict_from(frame_of_discernments, len(info_sources))
    combined_mass_values = _ds_orthogonal_combinations(mass_values, frame_of_discernments, set_dict)
    return combined_mass_values
def _ds_orthogonal_combinations(mass_values, frame_of_discernments, set_dict):
    '''
    Based on Dempster's rule of combination
    Args:
        mass_values: numpy array of shape (number_of_subsets_in_frame, amount_of_info, info_sources_channel)
        frame_of_discernments: list of all possible subsets within frame
        set_dict: dictionary of {key: (set1, set2), value: set(intersection_set)}
    Returns:
        combined_mass_values: numpy array of shape (number_of_subsets_in_frame, amount_of_info)
    '''
    subset_frame_size, info_size, info_source_size = mass_values.shape
    combined_mass = np.empty((subset_frame_size, info_size))
    frame_intersections, null_intersections = _build_frame_intersections(frame_of_discernments, set_dict)

    # TODO: refactor this
    mass_conflicts = np.zeros((info_size))
    for set_pair in null_intersections:
        all_m = []
        for s in range(len(set_pair)):
            m = mass_values[frame_of_discernments[set_pair[s]], :, s]
            all_m.append(m)
        mass_conflict = reduce((lambda x, y: np.multiply(x, y)), all_m)
        mass_conflicts += mass_conflict
    normalization_factor = np.ones(info_size) / (np.ones(info_size) - mass_conflicts)

    for idx, set_pair_list in enumerate(frame_intersections):
        mass_supports = np.zeros((info_size))
        for set_pair in set_pair_list:
            all_m = []
            for s in range(len(set_pair)):
                m = mass_values[frame_of_discernments[set_pair[s]], :, s]
                all_m.append(m)
            mass_support = reduce((lambda x, y: np.multiply(x, y)), all_m)
            mass_supports += mass_support
        combined_mass[idx, :] = np.multiply(normalization_factor, mass_supports)

    return combined_mass

def dempster(image):
    img = cv2.imread(image)
    rgb_r, rgb_g, rgb_b = img[:, :, 2], img[:, :, 1], img[:, :, 0]
    hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
    lmy = cv2.cvtColor(img, cv2.COLOR_RGB2LAB)
    xyz = cv2.cvtColor(img, cv2.COLOR_RGB2XYZ)
    ycrcb = cv2.cvtColor(img, cv2.COLOR_RGB2YCrCb)
    hls = cv2.cvtColor(img, cv2.COLOR_RGB2HLS)
    luv = cv2.cvtColor(img, cv2.COLOR_RGB2LUV)

    hsv_h, hsv_s, hsv_v = hsv[:, :, 0], hsv[:, :, 1], hsv[:, :, 2]
    lmy_l, lmy_m, lmy_y = lmy[:, :, 0], lmy[:, :, 1], lmy[:, :, 2]
    xyz_x, xyz_y, xyz_z = xyz[:, :, 0], xyz[:, :, 1], xyz[:, :, 2]
    ycrcb_y, ycrcb_cr, ycrcb_cb = ycrcb[:, :, 0], ycrcb[:, :, 1], ycrcb[:, :, 2]
    hls_h, hls_l, hls_s = hls[:, :, 0], hls[:, :, 1], hls[:, :, 2]
    luv_l, luv_u, luv_v = luv[:, :, 0], luv[:, :, 1], luv[:, :, 2]
    color_dict = {'hsv_h':hsv_h, 'hsv_s':hsv_s, 'hsv_v':hsv_v,
             'rgb_r':rgb_r, 'rgb_g':rgb_g, 'rgb_b':rgb_b,
             'xyz_x':xyz_x, 'xyz_y':xyz_y, 'xyz_z':xyz_z,
             'ycrcb_y':ycrcb_y, 'ycrcb_cr':ycrcb_cr, 'ycrcb_cb':ycrcb_cb,
             'hls_h':hls_h, 'hls_l':hls_l, 'hls_s':hls_s,
             'luv_l':luv_l, 'luv_u':luv_u, 'luv_v':luv_v,
             'lmy_l':lmy_l, 'lmy_m':lmy_m, 'lmy_y':lmy_y,}
    frame_set = {(1,):0, (2,):1, (1, 2):2}
    combined_mass = dempster_shafer(kmeans_mass_function, [luv_l, lmy_y], frame_set)
    combined_mass_argmax = np.argmax(combined_mass, axis=0)
    #print(combined_mass_argmax)
    h, w = hsv_h.shape
    output_img = combined_mass_argmax.reshape((h-2, w-2))
    #imsave("demp_img/"+ str(i) + "_demp.png",output_img)
    #display_img(np.load("dempster_img.npy"))
    plt.axis('off')
    plt.imshow(output_img)
    plt.savefig("bdempster_", bbox_inches='tight', pad_inches=0)
    #plt.show()
    return "bdempster_"+".png"
def hsv_custom_range_threshold(img, hsv_lower_thresh, hsv_upper_thresh):
    #print(img)
    hsv_img = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
    # Separate channels
    hue, saturation, value = hsv_img[:, :, 0], hsv_img[:, :, 1], hsv_img[:, :, 2]

    # Make mask for each channel
    h_mask = cv2.inRange(hue, hsv_lower_thresh[0], hsv_upper_thresh[0])
    s_mask = cv2.inRange(saturation, hsv_lower_thresh[1], hsv_upper_thresh[1])
    v_mask = cv2.inRange(value, hsv_lower_thresh[2], hsv_upper_thresh[2])

    # Apply masks
    masked_img = cv2.bitwise_and(img, img, mask=h_mask)
    masked_img = cv2.bitwise_and(masked_img, masked_img, mask=s_mask)
    masked_img = cv2.bitwise_and(masked_img, masked_img, mask=v_mask)

    # Combine HSV masks
    mask = cv2.bitwise_and(h_mask, s_mask)
    mask = cv2.bitwise_and(mask, v_mask)
    return mask, masked_img
def rgb_custom_range_threshold(img, rgb_lower_thresh, rgb_upper_thresh):
    #b, g, r = img[:, :, 0], img[:, :, 1], img[:, :, 2]
    r, g, b = img[:, :, 0], img[:, :, 1], img[:, :, 2]

    # Make mask for each channel
    b_mask = cv2.inRange(b, rgb_lower_thresh[0], rgb_upper_thresh[0])
    g_mask = cv2.inRange(g, rgb_lower_thresh[1], rgb_upper_thresh[1])
    r_mask = cv2.inRange(r, rgb_lower_thresh[2], rgb_upper_thresh[2])

    # Apply masks
    masked_img = cv2.bitwise_and(img, img, mask=b_mask)
    masked_img = cv2.bitwise_and(masked_img, masked_img, mask=g_mask)
    masked_img = cv2.bitwise_and(masked_img, masked_img, mask=r_mask)

    # Combine RGB masks
    mask = cv2.bitwise_and(b_mask, g_mask)
    mask = cv2.bitwise_and(mask, r_mask)
    return mask, masked_img
def pseudo_surface_area(mask):
    """
    Args:
        mask: single channel black and white image (0 - black, 255 - white)
    Returns:
        total_pixels: total white pixels (object of interest)
        pixel_percentage: white pixels over total pixels
    """
    total_pixels = (mask == 255).sum()
    pixel_percentage = (mask == 255).mean()
    return total_pixels, pixel_percentage
def color_analysis(img, mask):
    masked = cv2.bitwise_and(img, img, mask=mask)
    b, g, r = cv2.split(masked)
    lab = cv2.cvtColor(masked, cv2.COLOR_BGR2LAB)
    l, m, y = cv2.split(lab)
    hsv = cv2.cvtColor(masked, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)

    channels = {"b": b, "g": g, "r": r, "l": l, "m": m, "y": y, "h": h, "s": s, "v": v}
    histogram_bins = {}
    for channel, channel_arr in channels.items():
        histogram_bins[channel] = cv2.calcHist([channel_arr], [0], mask, [256], [0, 255])

    return histogram_bins
def run_image_processing_workflow2(image):
    print("running prediction for " + image)
    img_path = dempster(image)
    tmp_img = os.path.join(img_path)
    img = cv2.imread(tmp_img)
    #print(img)
    # Obtain plant mask
    hsv_lower_thresh = [25, 35, 35]
    hsv_upper_thresh = [60, 255, 255]

    rgb_lower_thresh = [0, 100, 0]
    rgb_upper_thresh = [200, 255, 200]
    #print(img)
    #plt.imshow(img)
    #plt.show()
    hsv_mask, hsv_masked_img = hsv_custom_range_threshold(img, hsv_lower_thresh, hsv_upper_thresh)
    rgb_mask, rgb_masked_img = rgb_custom_range_threshold(img, rgb_lower_thresh, rgb_upper_thresh)
    combined_mask = cv2.bitwise_and(hsv_mask, rgb_mask)

    #print(combined_mask)
    denoised_mask = median_filter(combined_mask, size=12)
    #print(denoised_mask)
    #plt.imshow(denoised_mask)
    #plt.show()
    # Obtain "surface area" information

    surface_area, area_percentage = pseudo_surface_area(denoised_mask)

    # Obtain color channels histogram bins
    histogram_bins = color_analysis(img, denoised_mask)

    # Write results
    #outfile = os.path.join(PROCESSED_IMAGE_DIR, image.split(".")[0] + "_mask.png")
    #print(f"Writing image file {outfile}")
    #cv2.imwrite(outfile, denoised_mask)
    #with open("results\\surface_area_results.txt", "a") as f:
     #   f.write(f"{outfile} {surface_area} {area_percentage} \n")
    #np.save(os.path.join(image.split(".")[0] + "_colorbins.npy"), histogram_bins)
    print("surface area is ",surface_area,"percentage is ",area_percentage)
    # Move tmp image file to stored dir
    stored_img = os.path.join(image)
    return surface_area,area_percentage
#run_image_processing_workflow2("test_img.jpeg")
