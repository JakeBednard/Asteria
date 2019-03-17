import mss
import numpy as np
from sklearn.cluster import MiniBatchKMeans


def k_means(bounding_box=None):

    with mss.mss() as sct:
        if bounding_box is not None:
            sct_img = sct.grab(bounding_box)
        else:
            sct_img = sct.grab()

    img = np.array(sct_img)

    # Transform to 2-d array, divide everything by 10, grab random sample to reduce processing time.
    img = img.reshape(img.shape[0] * img.shape[1], img.shape[2])
    img = img[np.random.randint(img.shape[0], size=1000), :3]

    kmeans = MiniBatchKMeans(16)
    kmeans.fit(img)

    colors = kmeans.cluster_centers_ // 10
    colors = colors.astype(int)

    colors_unique, colors_count = np.unique(colors, return_counts=True, axis=0)

    print(colors_unique, colors_count)

    colors = colors.tolist()
    # colors = sorted(colors, key=lambda l: sum(l), reverse=True)

    output = []
    for color in colors:
        output.append({
            'red': color[2],
            'green': color[1],
            'blue': color[0]
        })

    return output
