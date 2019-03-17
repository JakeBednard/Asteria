import mss
import numpy as np


def color_buckets(bounding_box=None):

    with mss.mss() as sct:
        if bounding_box is not None:
            sct_img = sct.grab(bounding_box)
        else:
            sct_img = sct.grab()

        img = np.array(sct_img)

    # Transform to 2-d array, divide everything by 10, grab random sample to reduce processing time.
    img = img.reshape(img.shape[0] * img.shape[1], img.shape[2])
    img = img[np.random.randint(img.shape[0], size=1000), :3]

    img = img // 10

    colors_unique, colors_count = np.unique(img, return_counts=True, axis=0)

    colors_unique = colors_unique * 10
    colors_unique = colors_unique.tolist()

    colors_count = colors_count.tolist()
    colors_count = list(map(list, zip(colors_count)))
    colors_count = [x[0] for x in colors_count]

    colors_rank = list(zip(colors_unique, colors_count))
    colors_rank = sorted(colors_rank, key=lambda x: (x[1]), reverse=True)

    color = colors_rank[0][0]

    for i in range(1, len(colors_rank)):
        if (color[0] + color[1] + color[2]) < 100:
            color = colors_rank[i][0]
        else:
            break

    return ({
        'red': color[2],
        'green': color[1],
        'blue': color[0]
    })
