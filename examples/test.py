from ..phoenyx.engine import Engine

renderer = Engine(600, 600)  # 600x600 window


def setup():
    """
    setup function for the Engine\\
    this function is called once
    """
    # new Slider at 100,100 named "slider"
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


def draw():
    """
    draw function for the Engine\\
    this function is repeated over and over
    """
    renderer.background(51)  # background color
    # getting slider value by name
    renderer.text(100, 500, f"value of slider : {renderer.get_slider_value('slider')}")


if __name__ == "__main__":
    # main loop
    renderer.run(draw, setup=setup)
