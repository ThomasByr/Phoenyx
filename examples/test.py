from phoenyx import Renderer

renderer = Renderer(600, 600)  # 600x600 window


def setup():
    """
    setup function for the Renderer\\
    this function is called once
    """
    # new Slider at 100, 100 named "slider"
    # minimum value : 0
    # maximum value : 10
    # initial value : 1
    # increment of one digit (one after coma) i.e. precision of 1e-1
    # length of 300
    renderer.create_slider(100, 100, "slider", 0, 10, 1, 1, length=300)

    # new Button at 300, 300 named "button"
    # wich prints "button pressed" when pressed
    renderer.create_button(300, 300, "button", action=lambda: print("button pressed"))

    # makes text appear bigger
    renderer.text_size = 15

    # global drawing settings
    renderer.no_fill()  # disable filling
    renderer.stroke = "red"  # enable stroking with red color
    renderer.stroke_weight = 5  # stroke weight of 5
    renderer.rect_mode = "CENTER"  # rect base point is now center instead of top left corner
    renderer.translation_behaviour = "KEEP"  # keep rect mode each time trough draw


def draw():
    """
    draw function for the Renderer\\
    this function is repeated over and over
    """
    renderer.background(51)  # background color
    # getting slider value by name
    renderer.text(100, 500, f"value of slider : {renderer.get_slider_value('slider')}")

    renderer.rect((325, 325), 60, 60)  # draw rect around button


if __name__ == "__main__":
    # main loop
    renderer.run(draw, setup=setup)
