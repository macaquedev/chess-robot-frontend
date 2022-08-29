import string
import cv2
import os
import imgaug.augmenters as iaa
import numpy as np
import pickle


def fen_to_position(fen):
    output = [["empty" for _ in range(8)] for _ in range(8)]
    row = 0
    pointer = 0
    for char in fen:
        if char in string.digits:
            pointer += int(char) - 1

        elif char in string.ascii_lowercase:
            output[row][pointer] = "white"
        elif char in string.ascii_uppercase:
            output[row][pointer] = "black"
        elif char == "/":
            row += 1
            pointer = -1
        pointer += 1
    return output


if __name__ == '__main__':
    augmentation = iaa.Sequential([
        iaa.color.MultiplyHue((0.95, 1.05)),
        iaa.color.MultiplySaturation((0.8, 1.2)),
        iaa.color.MultiplyBrightness((0.8, 1.2)),
        iaa.geometric.Rot90([0, 1, 2, 3]),
    ])

    for label in ["white", "black", "empty"]:
        os.makedirs(os.path.join("processed_data", label), exist_ok=True)
    data_file_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "../../data")
    counter = 0
    for i in range(len(os.listdir(data_file_path))):
        seed_dir = os.path.join(data_file_path, str(i+1))
        for j in range(len(os.listdir(seed_dir))):
            position_dir = os.path.join(seed_dir, str(j))
            with open(os.path.join(position_dir, "board.fen")) as f:
                position = fen_to_position(f.read())

            for file in os.listdir(position_dir):
                if file.endswith(".fen"):
                    continue
                photo = cv2.imread(os.path.join(position_dir, file))
                for m, r in enumerate(range(0, photo.shape[0], 50)):
                    for n, c in enumerate(range(0, photo.shape[1], 50)):
                        roi = photo[r:r + 50, c:c + 50, :]
                        roi = roi // 4 * 4 + 4 // 2
                        augmented_images = [roi.copy()] + augmentation(images=[roi.copy() for _ in range(31)])
                        for k, augmented_image in enumerate(augmented_images):
                            counter += 1
                            cv2.imwrite(os.path.join("processed_data",
                                                     position[m][n],
                                                     f"{counter}.jpg"),
                                        augmented_image)
                            print(f"Processed image {counter}")

    base_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "..", "..", "processed_data")
    labels = ["black", "white", "empty"]

    data = []

    for label in labels:
        path = os.path.join(base_path, label)
        label_num = labels.index(label)

        for filename in os.listdir(path):
            imgpath = os.path.join(path, filename)
            image = cv2.imread(imgpath)
            try:
                image = cv2.resize(image, (50, 50))
                image = np.array(image).flatten()
                data.append([image, label_num])
            except Exception as e:
                pass

    with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), "..", "..", "model", "data.pickle"), 'wb') as f:
        pickle.dump(data, f)
