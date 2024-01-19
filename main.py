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
    )

    return origin, p1, p2


def get_coordinates_converter(arm, config, image_shape):
    # Calibrate robot
    origin, p1, p2 = calibrate_from_config(arm, config)

    # Create converter
    converter = CoordinatesConverter(list(reversed(image.shape[:2])), origin, p1, p2)

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
    draw_edges(arm, converted_edges)


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

    if not config["calibration"].get("above_origin") or not config["calibration"].get("above_p1") or not config[
        "calibration"].get("above_p2"):
        # If any of the coordinates is not present in the config, get them from the user
        above_origin, above_p1, above_p2 = get_coordinates_from_user()
        config["calibration"]["above_origin"] = above_origin
        config["calibration"]["above_p1"] = above_p1
        config["calibration"]["above_p2"] = above_p2

    if config["enable_photomaton"]:
        photomaton_meta_loop(arm, config)

    else:
        image = ski.io.imread(config["image_path"])
        draw_image(arm, image, config)
