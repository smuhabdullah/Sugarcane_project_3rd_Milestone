import cv2
import numpy as np
# from rembg import remove
import tensorflow as tf
from sklearn import preprocessing

le = preprocessing.LabelEncoder()
model = tf.keras.models.load_model('static/CNN_Model.h5')
rembg_model = tf.keras.models.load_model('static/Rembg.h5')

def Removed_bg_Image(image_path):
    gray_image = cv2.imread(f'media/{image_path}', 0)
    rgb_image = cv2.imread(f'media/{image_path}')

    gray_image = cv2.resize(gray_image, (224, 224), interpolation=cv2.INTER_AREA)
    rgb_image = cv2.resize(rgb_image, (224, 224), interpolation=cv2.INTER_AREA)

    image = np.expand_dims(gray_image, axis=-1)  # expand the dimensions to (height, width, 1)

    # Predict the mask
    mask = rembg_model.predict(np.array([image]))

    mask = ( mask > 0.5 ).astype(np.uint8)
    mask = np.squeeze(mask)

    # Find the contour with the largest area
    contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    largest_contour = max(contours, key=cv2.contourArea)

    # Create a new mask image and fill it with black color
    new_mask = np.zeros_like(mask)

    # Draw the contour on the new mask with white color
    cv2.drawContours(new_mask, [largest_contour], 0, 255, -1)

    # Use bitwise AND to combine the original mask with the new mask
    result = cv2.bitwise_and(mask, new_mask)
    
    closing_kernel = np.ones((3,3),np.uint8)
    mask = cv2.morphologyEx(result, cv2.MORPH_CLOSE, closing_kernel)

    mask = result*255
    mask = np.repeat(mask[...,np.newaxis],3,axis = -1)
    # # Perform the bitwise AND operation
    removed_bg_image = cv2.bitwise_and(mask,rgb_image)
   
    return removed_bg_image

def Read_Image(image):
    # RGB`
    if (image.shape[0] < 300 and image.shape[1] < 400):
        print("True")
        rgb_image_size = cv2.resize(image,(300,400), interpolation = cv2.INTER_CUBIC)
    else:
        print("False")
        rgb_image_size = cv2.resize(image,(300,400), interpolation = cv2.INTER_AREA)
    return rgb_image_size 

def Gray_Scale_Image(rgb_image):
    # Converting to gray
    # blur = cv2.medianBlur(rgb_image, 7)
    gray = cv2.cvtColor(rgb_image, cv2.COLOR_BGR2GRAY)
    return gray

def Equalized_Hist(gray_image):
    # Converting to equalized
    eqalized_image = cv2.equalizeHist(gray_image)
    return eqalized_image

def Binary_Image(image):
    # Converting to Binary
    binary = cv2.threshold(image,125, 255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)[1]
    return binary

def Morphology_Image(binary_image):
    # Converting to Morphology by using kernel 3x3
    kernel = np.ones((3,3),np.uint8)
    MORPH_close = cv2.morphologyEx(binary_image,cv2.MORPH_CLOSE,kernel, iterations = 1)
    return MORPH_close


def Contours(M_Image):
    # Figuring out number of infected region
    contours, hierarchy = cv2.findContours(M_Image, mode=cv2.RETR_LIST, method=cv2.CHAIN_APPROX_NONE)
    
    biggest_contour =  max(contours,key=cv2.contourArea)
    leaf_area = cv2.contourArea(biggest_contour)

    infected_contour_lst = []
    for i in contours:
        infected_contour_lst.append(cv2.contourArea(i))
    infected_contour_lst.remove(leaf_area)
    infected_area =    sum(infected_contour_lst)

    Num_of_contour = len(contours)

    return contours, leaf_area, infected_area, Num_of_contour

def Contours_On_Orinial(Image, contours):
    # Drawing image of number of infected region
    image_copy = Image.copy()
    spot_on_org_img = cv2.drawContours(image_copy, contours, -1, (0, 255, 0), thickness=2)

    # draw the contours on the black image
    black_img = np.zeros(Image.shape)
    cv2.drawContours(black_img, contours, -1, (0,255,0), 1)
    return spot_on_org_img, black_img


def Save_Images(img_path,rgb_original_image, removed_bg_image, gray, eqalized_image, binary, MORPH_close, spot_on_org_img, black_img):
    cv2.imwrite(f'media/rgb_original_image/{img_path}', rgb_original_image)  
    cv2.imwrite(f'media/Removed_bg_Images/{img_path}', removed_bg_image)  
    cv2.imwrite(f'media/GrayScale_Images/{img_path}', gray)  
    cv2.imwrite(f'media/Equalized_images/{img_path}', eqalized_image)  
    cv2.imwrite(f'media/binary_Images/{img_path}', binary)  
    cv2.imwrite(f'media/morphological_images/{img_path}', MORPH_close)  
    cv2.imwrite(f'media/spot_on_org_images/{img_path}', spot_on_org_img)  
    cv2.imwrite(f'media/spot_on_black_images/{img_path}', black_img)  
    return True

def disease_Name(result):
    Labels_dict = {0: 'Bacterial Blight',
                     1: 'Leaf Rust',
                      2: 'Leaf Spot',
                      3: 'Mite Insect',
                      4: 'Red Rot',
                      5: 'Red Rust',
                      6: 'White Fly',
                      7: 'Yellow Leaf Virus'}
    
    return Labels_dict[result]


def predict(img_path): 
    # print(model.summary())
    img = cv2.imread(f'media/{img_path}')
    # print(img)
    img = cv2.resize(img, (224, 224))
    img = img/255.0
    img = np.expand_dims(img, axis=0)
    prediction = model.predict(img)
    print("prediction: ",prediction)
    # data = chart_data(prediction)
    result = [np.argmax(res) for res in prediction]
    # print("result: ", result)
    # print(disease_Name(result[0]))
    disease = disease_Name(result[0])
    return disease, prediction[0].tolist()


def get_treatment(treatment):
    symptoms = treatment.symptoms
    caused = treatment.caused
    organic_control = treatment.organic_control
    chemical_control = treatment.chemical_control
    preventive_measures = treatment.preventive_measures
    preventive_measures = preventive_measures.split(".")
    # print(preventive_measures)
    return symptoms, caused, organic_control, chemical_control, preventive_measures

def chart_data(prediction):
    prediction_data = prediction[0].tolist()
    total = sum(prediction_data)

    # Normalize the data
    prediction_data = [x/total for x in prediction_data]
    data = [
      { "label": "Red Rot", "y":            prediction_data[4]*100 },
      { "label": "Yellow Leaf Virus", "y":  prediction_data[7]*100  },
      { "label": "Leaf rust", "y":          prediction_data[1]*100  },
      { "label": "Leaf spot", "y":          prediction_data[2]*100  },
      { "label": "White Fly", "y":          prediction_data[6]*100  },
      { "label": "Red Rust", "y":           prediction_data[5]*100  },
      { "label": "Bacterial Blight", "y":   prediction_data[0]*100  },
      { "label": "Mite Insect", "y":        prediction_data[3]*100  }
    ]
    # print("data of prediction",prediction_data)
    # print("Bacterial Blight",prediction_data[0])
    # print("Leaf rust",prediction_data[1])
    # print("Leaf spot",prediction_data[2])
    # print("Mite Insect",prediction_data[3])
    # print("Red Rot",prediction_data[4])
    return data
