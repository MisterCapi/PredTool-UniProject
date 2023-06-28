import cv2
import numpy as np

def put_stats_on_image(stats):
    # Load the image
    img = cv2.imread('screenshot.png')

    # Define the region of interest
    x, y, w, h = 420, 0, 1, 1080
    roi = img[y:y+h, x:x+w]

    # Apply horizontal blur to the selected region
    for i in range(420, 1920):
        img[0:1080, i:i+1] = roi

    def put_text_on_img(text, x_text, y_text, heading=False, small=False):
        if heading:
            size = 1.5
        else:
            size = .7
        if small:
            size = .4
        thickness = 1
        font = cv2.FONT_HERSHEY_SIMPLEX
        color = (225, 225, 225)
        # Get the size of the text
        text_size, _ = cv2.getTextSize(text, font, size, thickness)

        # Compute the position to put the text
        x = x_text - text_size[0] // 2
        y = y_text // 2 + text_size[1] // 2

        # Put the text on the image
        cv2.putText(img, text, (x, y), font, size, color, thickness, cv2.LINE_AA)


    put_text_on_img('Overall:', 380, 65, heading=True)
    put_text_on_img('MMR', 560, 65, heading=True)
    put_text_on_img('WR', 720, 65, heading=True)
    put_text_on_img('KDA', 920, 65, heading=True)
    put_text_on_img('ratio', 1070, 65, heading=True)
    put_text_on_img('Top role', 1250, 65, heading=True)
    put_text_on_img('Hero:', 1450, 65, heading=True)
    put_text_on_img('WR', 1600, 65, heading=True)
    put_text_on_img('KDA', 1750, 65, heading=True)

    for i, stat in enumerate(stats):
        split_distance = 0
        if i > 4:
            split_distance = 120
        # MMR
        put_text_on_img(str(int(stat[0])), 560, 210 + i*180 + split_distance)
        # WR / Total matches
        put_text_on_img(str(stat[1]), 720, 210 + i*180 + split_distance-10)
        put_text_on_img('Matches: ' + str(stat[4]), 720, 210 + i*180 + split_distance + 30, small=True)
        # KDA
        put_text_on_img(str(stat[2]), 920, 210 + i*180 + split_distance)
        # KDA ratio
        put_text_on_img(str(stat[3]), 1070, 210 + i*180 + split_distance)
        # Top role
        put_text_on_img(str(stat[5]), 1250, 210 + i*180 + split_distance)
        # Hero WR / Total matches
        put_text_on_img(str(stat[6]), 1600, 210 + i*180 + split_distance-10)
        put_text_on_img('Matches: ' + str(stat[8]), 1600, 210 + i*180 + split_distance + 30, small=True)
        # Hero KDA ratio
        put_text_on_img(str(stat[7]), 1750, 210 + i*180 + split_distance)

    overlay = img.copy()

    def add_line(x):
        cv2.line(overlay, (x, 0), (x, 510), (170, 170, 170), 2, cv2.LINE_AA)
        cv2.line(overlay, (x, 581), (x, 1020), (170, 170, 170), 2, cv2.LINE_AA)

    add_line(485)
    add_line(640)
    add_line(790)
    add_line(1140)
    add_line(1360)
    add_line(1675)

    # cv2.line(overlay, (900, 0), (900, 510), (170, 170, 170), 2, cv2.LINE_AA)
    # cv2.line(overlay, (1200, 0), (1200, 510), (170, 170, 170), 2, cv2.LINE_AA)
    # cv2.line(overlay, (1400, 0), (1400, 510), (170, 170, 170), 2, cv2.LINE_AA)
    # cv2.line(overlay, (1500, 0), (1500, 510), (170, 170, 170), 2, cv2.LINE_AA)

    img = cv2.addWeighted(overlay, 0.15, img, 0.85, 0)

    # Display the resulting image and save it
    cv2.imwrite('screenshot.png', img)

    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == '__main__':
    put_stats_on_image([(1579.5, '52.9%', '3.3 / 5.9 / 7.9', '1.90', '85', 'Support', 0, 0, 0), (1902.1, '56.0%', '4.6 / 4.5 / 8.1', '2.82', '278', 'Midlane', '87.5%', '6.67', '16'), (1495.6, '58.8%', '2.9 / 6.2 / 4.1', '1.11', '17', 'Offlane', '77.8%', '1.20', '9'), (1445.4, '47.0%', '3.8 / 4.2 / 6.3', '2.37', '221', 'Carry', '39.1%', '3.00', '23'), (1333.3, '41.0%', '2.9 / 4.7 / 3.9', '1.45', '143', 'Offlane', '50.0%', '2.17', '4'), (1565.7, '54.0%', '4.3 / 4.1 / 6.8', '2.68', '597', 'Jungle', '36.8%', '2.00', '38'), (1211.8, '36.0%', '5.4 / 5.1 / 5.7', '2.15', '144', 'Carry', '33.3%', '1.71', '18'), (1301.4, '37.0%', '3.6 / 4.6 / 5.0', '1.89', '247', 'Midlane', '42.9%', '2.50', '14'), (1176.7, '39.0%', '2.9 / 5.8 / 6.3', '1.57', '484', 'Support', '44.1%', '2.00', '127'), (1509.9, '51.0%', '1.8 / 2.8 / 5.4', '2.58', '378', 'Offlane', '48.9%', '3.00', '141')])
