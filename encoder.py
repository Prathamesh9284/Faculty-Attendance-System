# import face_recognition

# import cv2

# import os



# def load_and_encode_image(image_path):

#     """Load an image, convert it to RGB, and get face encodings."""

#     if not os.path.exists(image_path):

#         print(f"Error: File not found - {image_path}")

#         return None



#     # Load the image

#     img = cv2.imread(image_path)



#     if img is None:

#         print(f"Error: Unable to read the image file - {image_path}")

#         return None



#     # Convert to RGB

#     rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)



#     # Get face encodings

#     encodings = face_recognition.face_encodings(rgb_img)



#     if not encodings:

#         print(f"Error: No face detected in {image_path}")

#         return None



#     return encodings[0]



# # Load and encode the first image

# encoding1 = load_and_encode_image(r'faces/Aniket2.jpg')

# if encoding1 is None:

#     exit()



# # Load and encode the second image

# encoding2 = load_and_encode_image(r'faces/Aniket.jpg')

# if encoding2 is None:

#     exit()



# # Compare faces

# result = face_recognition.compare_faces([encoding1], encoding2)

# print(f'Result: {result}')



# # Display the first image

# img = cv2.imread(r'faces/Shlok.jpg')

# cv2.imshow('Shlok', img)

# cv2.waitKey(0)

# cv2.destroyAllWindows()

import face_recognition
import cv2
import os
import pickle


def load_and_encode_image(image_path):
    """Load an image, convert it to RGB, and get face encodings."""
    if not os.path.exists(image_path):
        print(f"Error: File not found - {image_path}")
        return None

    # Load the image
    img = cv2.imread(image_path)

    if img is None:
        print(f"Error: Unable to read the image file - {image_path}")
        return None

    # Convert to RGB
    rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Get face encodings
    encodings = face_recognition.face_encodings(rgb_img)

    if not encodings:
        print(f"Error: No face detected in {image_path}")
        return None

    return encodings[0]


def save_encodings_to_file(encoding_dict, filename):
    """Save encodings to a pickle file."""
    with open(filename, 'wb') as f:
        pickle.dump(encoding_dict, f)
    print(f"Encodings saved to {filename}")


def load_encodings_from_file(filename):
    """Load encodings from a pickle file."""
    if not os.path.exists(filename):
        print(f"Error: Encoding file not found - {filename}")
        return None

    with open(filename, 'rb') as f:
        return pickle.load(f)


# Encode all images in the faces folder
encodings = {}
faces_folder = 'faces'
encoding_file = 'encoding.pkl'

for file_name in os.listdir(faces_folder):
    file_path = os.path.join(faces_folder, file_name)
    if file_name.endswith(('jpg', 'jpeg', 'png')):  # Check for image files
        encoding = load_and_encode_image(file_path)
        if encoding is not None:
            encodings[file_name] = encoding

# Save the encodings to a file
save_encodings_to_file(encodings, encoding_file)
