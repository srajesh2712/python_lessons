import numpy as np
from matplotlib import pyplot as plt

kernel_v = np.array([[-1, 0, 1],
                      [-1, 0, 1],
                      [-1, 0, 1]])

kernel_h = np.array ([[-1,-1,-1],
                      [0,0,0],
                      [1,1,1]])



def conv2d(image,kernerl):
    image_h, image_w = image.shape
    kernel_h, kernel_w = kernerl.shape

    out_h = image_h - kernel_h + 1
    out_w = image_w - kernel_w + 1
    output = np.zeros((out_h, out_w))

    for i in range(out_h):
        for j in range(out_w):
            patch = image[i:i+kernel_h, j:j+kernel_w]
            val = np.sum(kernerl*patch)
            output[i, j] = max(0,val)

    return output


def create_white_square():
    image = np.zeros((10 ,10))
    image[2:6, 2:6] = 1

    return image

def max_pooling2d(feature_map,size=2,stride = 1 ):
    h,w = feature_map.shape
    out_h = (h - size) // stride + 1
    out_w = (w - size) // stride + 1
    pooled_out = np.zeros((out_h, out_w))
    for i in range(out_h):
        for j in range(out_w):
            window = feature_map[i*stride:i*stride+size, j*stride:j*stride+size]
            pooled_out[i, j] = np.max(window)
    return pooled_out


def flatten_data(feature_map_h,feature_map_v):
    vector_h = feature_map_h.flatten()
    vector_v = feature_map_v.flatten()
    input_vector = np.concatenate((vector_h,vector_v))
    return input_vector

def predict_square(input_vector):
    weights = np.ones_like(input_vector)*0.5
    bias = -5

    logit = np.dot(input_vector, weights) + bias
    print(f"Logit score : {logit}")
    probability = 1/(1 + np.exp(-logit))
    return probability

if __name__ == '__main__':
    image = create_white_square()
    feat_map_v = conv2d(image, kernel_v)
    feat_map_h = conv2d(image, kernel_h)

    print(feat_map_v)
    print(feat_map_h)
    pooled_out_h = max_pooling2d(feat_map_h)
    pooled_out_v = max_pooling2d(feat_map_v)

    input_vector = flatten_data(feat_map_v, feat_map_h)
    print(input_vector)
    prob = predict_square(input_vector)
    print(f" Total signals detected :{np.sum(input_vector)}")
    print(f"Probability that this is square :{prob * 100:.2f} %")
    fig, ax = plt.subplots(1,5,figsize=(10,3))

    ax[0].imshow(image, cmap='gray');
    ax[0].title.set_text('Original');
    ax[1].imshow(feat_map_h, cmap='gray');
    ax[1].title.set_text('Convolution Horizontal ');
    ax[2].imshow(feat_map_v, cmap='gray');
    ax[2].title.set_text('Convolution vertical ');


    ax[3].imshow(pooled_out_h, cmap='gray',vmin=0, vmax=2,interpolation='nearest');
    ax[3].title.set_text('Pooled out  ');


    ax[4].imshow(pooled_out_v, cmap='gray',vmin=0, vmax=2,interpolation='nearest');
    ax[4].title.set_text('Pooled out  ');

    plt.show()

