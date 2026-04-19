import numpy as np
from PIL import Image
from PIL import ImageOps
import argparse
import os


def add_gaussian_noise(image, mean=0, std=25):
    noisy_image = np.array(image).astype(np.float32)
    noise = np.random.normal(mean, std, noisy_image.shape)
    noisy_image = noisy_image + noise
    noisy_image = np.clip(noisy_image, 0, 255).astype(np.uint8)
    return Image.fromarray(noisy_image)


def add_salt_pepper_noise(image, salt_prob=0.01, pepper_prob=0.01):
    noisy_image = np.array(image).astype(np.float32)
    height, width = noisy_image.shape[:2]
    total_pixels = height * width

    salt_num = int(total_pixels * salt_prob)
    pepper_num = int(total_pixels * pepper_prob)

    y_salt = np.random.randint(0, height, salt_num)
    x_salt = np.random.randint(0, width, salt_num)
    noisy_image[y_salt, x_salt] = 255

    y_pepper = np.random.randint(0, height, pepper_num)
    x_pepper = np.random.randint(0, width, pepper_num)
    noisy_image[y_pepper, x_pepper] = 0

    return Image.fromarray(noisy_image.astype(np.uint8))


def add_poisson_noise(image):
    noisy_image = np.array(image).astype(np.float32)
    vals = len(np.unique(noisy_image))
    vals = 2 ** np.ceil(np.log2(vals))
    noisy_image = np.random.poisson(noisy_image * vals) / float(vals)
    noisy_image = np.clip(noisy_image, 0, 255).astype(np.uint8)
    return Image.fromarray(noisy_image)


def add_speckle_noise(image, variance=0.1):
    noisy_image = np.array(image).astype(np.float32)
    noise = np.random.randn(*noisy_image.shape)
    noisy_image = noisy_image + noisy_image * noise * variance
    noisy_image = np.clip(noisy_image, 0, 255).astype(np.uint8)
    return Image.fromarray(noisy_image)


def add_uniform_noise(image, low=-25, high=25):
    noisy_image = np.array(image).astype(np.float32)
    noise = np.random.uniform(low, high, noisy_image.shape)
    noisy_image = noisy_image + noise
    noisy_image = np.clip(noisy_image, 0, 255).astype(np.uint8)
    return Image.fromarray(noisy_image)


def main():
    parser = argparse.ArgumentParser(description='Add noise to images')
    parser.add_argument('input', help='Input image path')
    parser.add_argument('output', help='Output image path')
    parser.add_argument('--type', '-t', choices=['gaussian', 'salt_pepper', 'poisson', 'speckle', 'uniform'],
                        default='gaussian', help='Type of noise to add')
    parser.add_argument('--mean', '-m', type=float, default=0, help='Mean for Gaussian noise')
    parser.add_argument('--std', '-s', type=float, default=25, help='Standard deviation for Gaussian noise')
    parser.add_argument('--salt', type=float, default=0.01, help='Salt probability for salt-pepper noise')
    parser.add_argument('--pepper', type=float, default=0.01, help='Pepper probability for salt-pepper noise')
    parser.add_argument('--variance', '-v', type=float, default=0.1, help='Variance for speckle noise')
    parser.add_argument('--low', type=float, default=-25, help='Low bound for uniform noise')
    parser.add_argument('--high', type=float, default=25, help='High bound for uniform noise')

    args = parser.parse_args()

    if not os.path.exists(args.input):
        print(f"Error: Input file '{args.input}' does not exist.")
        return

    image = Image.open(args.input)
    image = ImageOps.exif_transpose(image)

    if image.mode != 'L' and image.mode != 'RGB':
        image = image.convert('RGB')

    if args.type == 'gaussian':
        noisy_image = add_gaussian_noise(image, mean=args.mean, std=args.std)
    elif args.type == 'salt_pepper':
        noisy_image = add_salt_pepper_noise(image, salt_prob=args.salt, pepper_prob=args.pepper)
    elif args.type == 'poisson':
        noisy_image = add_poisson_noise(image)
    elif args.type == 'speckle':
        noisy_image = add_speckle_noise(image, variance=args.variance)
    elif args.type == 'uniform':
        noisy_image = add_uniform_noise(image, low=args.low, high=args.high)

    noisy_image.save(args.output)
    print(f"Noisy image saved to '{args.output}'")


if __name__ == '__main__':
    main()
