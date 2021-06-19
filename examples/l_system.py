import math as m
from phoenyx import *

angle = 0
axiom = "F"
sentence = axiom
length = 100

rules: list[dict[int, str]] = []
rules.append({
    0: "F",
    1: "FF+[+F-F-F]-[-F+F+F]",
})

renderer: Renderer = Renderer(400, 400, "L-system fractal trees")


def generate() -> None:
    global length, sentence
    renderer.text(120, 18, "generating ...")
    renderer.flip()
    length *= .5
    next_sentence = ""
    for i in range(len(sentence)):
        current = sentence[i]
        found = False
        for j in range(len(rules)):
            if current == rules[j][0]:
                found = True
                next_sentence += rules[j][1]
                break
        if not found:
            next_sentence += current
    sentence = next_sentence
    turtle()


def turtle() -> None:
    global length, sentence
    renderer.background(51)
    renderer.reset_matrix()
    renderer.translate(200, 400)
    renderer.stroke = 255

    for i in range(len(sentence)):
        current = sentence[i]

        if current == "F":
            renderer.line((0, 0), (0, -length))
            renderer.translate(0, -length)
        elif current == "+":
            renderer.rotate(angle)
        elif current == "-":
            renderer.rotate(-angle)
        elif current == "[":
            renderer.push()
        elif current == "]":
            renderer.pop()

    renderer.flip()


def setup() -> None:
    global angle
    angle = m.radians(25)
    renderer.background(51)
    renderer.text_size = 20

    renderer.create_button(
        10,
        10,
        "generate",
        width=100,
        height=30,
        color=51,
        stroke=255,
        weight=1,
        shape=RECTANGLE,
        action=generate,
    )
    turtle()


def draw() -> None:
    ...


if __name__ == "__main__":
    renderer.run()
