import tomllib
from arms import get_arm, calibrate, draw_edges, wait_for_input
import skimage as ski
from photo2drawing import rgb2edge_image, rgb2edges
from photomaton import photomaton_loop
from coordinates import CoordinatesConverter
from utils import sort_edges
import signal
import cv2

import tkinter as tk
from tkinter import simpledialog
from utils import calibrate_from_user_input

import numpy as np
import os

from CustomTkinter import App
from robot_control_app import RobotControlApp

def load_config():
    with open("config.toml", "rb") as f:
        return tomllib.load(f)


def signal_handler(sig, frame):
    wait_for_input("continue")


def calibrate_from_config(arm, config):
    origin, p1, p2 = calibrate(
        arm,
        [
            config["calibration"]["above_origin"],
            config["calibration"]["above_p1"],
            config["calibration"]["above_p2"],
        ],
        absolute_epsilon=config["calibration"]["epsilon"],
        relative_epsilon=config["calibration"]["relative_epsilon"],
    )

    return origin, p1, p2

"""
# Ouvre une fenêtre qui permet de déplacer le robot aux points origin, p1 et p2
def calibrate_from_config(arm, config):
    origin = calibrate_from_user_input(arm)
    p1 = calibrate_from_user_input(arm)
    p2 = calibrate_from_user_input(arm)
    return origin, p1, p2"""

def get_coordinates_converter(arm, config, image_shape):
    # Calibrate robot
    origin, p1, p2 = calibrate_from_config(arm, config)

    # Create converter
    converter = CoordinatesConverter(list(reversed(image_shape[:2])), origin, p1, p2)

    return converter


def edges_from_config(image, config):
    edges = rgb2edges(
        image,
        nb_edges=config["edge_processing"]["nb_edges"],
        min_edge_length=config["edge_processing"]["min_edge_length"],
        step=config["edge_processing"]["edge_step"],
        method=config["image_processing"]["edge_finding_method"],
    )

    if config["edge_processing"]["sort_edges"]:
        edges = sort_edges(edges)

    return edges


def draw_image(arm, image, config, converter=None):
    if converter is None:
        converter = get_coordinates_converter(arm, config, image.shape)
    edges = edges_from_config(image, config)
    converted_edges = converter.convert_list_of_points(edges)

    save_contours_image(image, edges)    # Save the image with contours

    draw_edges(arm, converted_edges)

    """final=config["calibration"]["above_origin"]
    return final"""



def save_contours_image(image, edges):
    # Create a binary image with white background
    contours_image = np.ones_like(image, dtype=np.uint8) * 255
    # Draw contours in black
    cv2.drawContours(contours_image, [np.array(edge, dtype=np.int32) for edge in edges], -1, (0, 0, 0), 1)
    # Get the path to the "data" folder
    data_folder = os.path.join(os.getcwd(), "data")
    # Ensure the "data" folder exists
    os.makedirs(data_folder, exist_ok=True)
    # Save the image in the "data" folder
    contours_image_path = os.path.join(data_folder, "contours_image.png")
    cv2.imwrite(contours_image_path, contours_image)
    print(f"Contours image saved at: {contours_image_path}")




def photomaton_meta_loop(arm, config):
    cap = cv2.VideoCapture(config["photomaton"]["camera_index"])
    converter = None
    while True:
        if config["photomaton"]["recalibrate_every_time"]:
            converter = None
        image = photomaton_loop(cap)
        draw_image(arm, image, config, converter)


def get_coordinates_from_user():
    root = tk.Tk()
    root.withdraw()

    above_origin = simpledialog.askstring("Input", "Enter coordinates for above_origin (comma-separated):")
    above_p1 = simpledialog.askstring("Input", "Enter coordinates for above_p1 (comma-separated):")
    above_p2 = simpledialog.askstring("Input", "Enter coordinates for above_p2 (comma-separated):")

    root.destroy()

    return list(map(int, above_origin.split(','))), list(map(int, above_p1.split(','))), list(map(int, above_p2.split(',')))


if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)

    config = load_config()

    # Connect to robot
    arm = get_arm(config["robot_ip"])

    """# Permet de rentrer soi-même les valeurs pour les points origin, p1, p2
    if not config["calibration"].get("above_origin") or not config["calibration"].get("above_p1") or not config[
        "calibration"].get("above_p2"):
        
        above_origin, above_p1, above_p2 = get_coordinates_from_user()
        config["calibration"]["above_origin"] = above_origin
        config["calibration"]["above_p1"] = above_p1
        config["calibration"]["above_p2"] = above_p2"""

    if config["enable_photomaton"]:
        photomaton_meta_loop(arm, config)

    else:
        image = ski.io.imread(config["image_path"])
        draw_image(arm, image, config)
