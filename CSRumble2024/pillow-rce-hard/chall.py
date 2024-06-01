#!/usr/bin/env python

from PIL import Image, ImageMath


def main():
    images = {}
    while input("Add image? (y/n) ") in ("y", "yes"):
        name = input("Name: ")
        x = int(input("Width: "))
        y = int(input("Height: "))
        data = bytes.fromhex(input("Data (hex): "))
        images[name] = Image.frombytes("I", (x, y), data)

    exp = input("Expression: ")
    # No attribute access for you
    assert "." not in exp
    # But you get a bonus
    images["free_win"] = ImageMath._Operand.apply

    ImageMath.eval(exp, images)


if __name__ == "__main__":
    main()
