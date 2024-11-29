from typing import Dict, Any, Type, Tuple
import pygame
import DataStructures as ds
from GUI import main_loop


def get_inputs(inputs: Dict[str, Type]) -> Dict[str, Any]:
    """
    Function to get the inputs from the user

    inps: Dict[str,Any] -> Dictionary of Inputs

    Returns:
    Dict[str,Any]: Dictionary of Inputs
    """

    outputs = {}

    for key, value in inputs.items():

        inp = None

        while inp is None:
            try:
                inp = value(input(f"Enter the {key}: "))
                outputs[key] = inp
            except:
                print(f"Invalid Input for {key}")
                print("--------------------")

    return outputs

def get_params() -> Tuple[Dict[str, Any], Dict[str, Any]]:
    """
    Function to get the parameters from the user

    Returns:
    Tuple[Dict[str,Any],Dict[str,Any]]: Tuple of Screen Size and Matrix Size
    """
    pygame.display.init()
    max_screen_size = pygame.display.Info()


    print("Enter the Screen Size")

    SCREEN_SIZE = get_inputs({"width": int, "height": int})
    while SCREEN_SIZE["width"] > max_screen_size.current_w or SCREEN_SIZE["height"] > max_screen_size.current_h:
        print("Screen Size is too large")
        SCREEN_SIZE = get_inputs({"width": int, "height": int})

    print("******************************")

    print("Enter the Matrix Size")
    MATRIX_SIZE = get_inputs({"width": int, "height": int})
    print("******************************")

    return SCREEN_SIZE, MATRIX_SIZE


if __name__ == "__main__":

    SCREEN_SIZE, MATRIX_SIZE = get_params()


    main_loop(screen_size=(SCREEN_SIZE["width"], SCREEN_SIZE["height"]),
              matrix_size=(MATRIX_SIZE["width"], MATRIX_SIZE["height"]))
