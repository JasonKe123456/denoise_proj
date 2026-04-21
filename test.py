import numpy as np


def test():
    x = np.random.rand(2304, 4096)
    mask = x < 0.5
    print(mask.shape)
    # mask[:1, :] = False
    # mask[-1:, :] = False
    # mask[:, :1] = False
    # mask[:, -1:] = False
    mask_copy = mask.copy()
    mask_copy[1::2, 1::3] = mask[1::2, 0::3] * mask[1::2, 3::3] * mask[0::2, 1::3] * mask[0::2, 2::3]
    mask_copy[1::2, 2::3] = mask_copy[1::2, 1::3]
    mask_copy[2:-1:2, 3::3] = mask[2:-1:2, 2::3] * mask[2:-1:2, 4::3] * mask[1::2, 3::3]

if __name__ == "__main__":
    test()