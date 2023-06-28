import os
import cv2
import easyocr
from PIL import Image


def get_hero_name_from_image(image_path: str):
    # Load the piece of image with the hero avatar in-game
    query_image = cv2.imread(image_path)

    # Load each image from the hero_avatars folder
    hero_avatars_dir = 'hero_avatars'
    hero_avatars = []
    for filename in os.listdir(hero_avatars_dir):
        if filename.endswith('.png'):
            image_path = os.path.join(hero_avatars_dir, filename)
            image = cv2.imread(image_path)
            hero_avatars.append((filename.rsplit('.', 1)[0], image))

    # Extract features using the SIFT algorithm
    sift = cv2.xfeatures2d.SIFT_create()
    _, query_descriptors = sift.detectAndCompute(query_image, None)
    hero_avatars_descriptors = []
    for _, image in hero_avatars:
        _, descriptors = sift.detectAndCompute(image, None)
        hero_avatars_descriptors.append(descriptors)

    # Compute similarity using the Euclidean distance
    results = []
    for i in range(len(hero_avatars)):
        hero_name, _ = hero_avatars[i]
        descriptors = hero_avatars_descriptors[i]

        # Compute matches between the query image and the current hero avatar image
        matcher = cv2.BFMatcher()
        matches = matcher.match(query_descriptors, descriptors)
        if len(matches):
            distance = sum(match.distance for match in matches) / len(matches)
            results.append((distance, hero_name))
        else:
            return ""

    # Sort the results by similarity score
    results.sort(key=lambda x: x[0])

    # Display the most similar image
    most_similar_hero = results[0][1]
    return most_similar_hero


def extract_usernames_and_heroes(image_path: str):
    reader = easyocr.Reader(['en'])
    results = reader.readtext("screenshot.png")
    results = [result for result in results if 110 < result[0][0][0] < 120]
    results = [result[1] for result in results]
    player_names = [result for result in results if not result.startswith('LEVEL:')]

    heroes = []
    img = Image.open("screenshot.png")
    cropped_hero_path = "cropped_hero.png"
    for i in range(10):

        splitter_distance = 0
        if i > 4:
            splitter_distance = 67
        cropped_img = img.crop((50,
                                86 + 89 * i + splitter_distance,
                                50 + 52,
                                86 + 52 + 89 * i + splitter_distance))
        # Display the cropped image
        cropped_img.save(cropped_hero_path)
        heroes.append(get_hero_name_from_image(cropped_hero_path))
    if os.path.exists(cropped_hero_path):
        os.remove(cropped_hero_path)
    return player_names, heroes
