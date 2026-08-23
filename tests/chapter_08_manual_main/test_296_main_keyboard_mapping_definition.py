"""
Define keyboard-to-NES-button mapping for main.py.

File to update:
    main.py

Why this step exists:
main.py is now the visual pygame runner. To make the ROM interactive, it needs a
small mapping from NES controller button names to pygame key constants.

This first keyboard step only defines the mapping dictionary. The next test covers
the helper that applies key events to Controller button booleans and wires it into
the pygame event loop.

Suggested implementation example:

    import pygame


    KEYS = {
        "a": pygame.K_z,
        "b": pygame.K_x,
        "select": pygame.K_RSHIFT,
        "start": pygame.K_RETURN,
        "up": pygame.K_UP,
        "down": pygame.K_DOWN,
        "left": pygame.K_LEFT,
        "right": pygame.K_RIGHT,
    }

Why this direction?
This dictionary answers the question:

    "Which keyboard key controls this NES button?"

For example, in the next test we will do:

    KEYS["a"] == pygame.K_z

means keyboard Z controls NES A.

Out of scope:
    - handling KEYDOWN / KEYUP events
    - pygame joystick/gamepad support
    - remapping UI
    - controller port 2
"""

import pygame

import main


def test_main_declares_keys_mapping_dictionary():
    """
    Objective:
    main.py exposes a KEYS dictionary for manual keyboard mapping.
    """
    assert hasattr(main, "KEYS")
    assert isinstance(main.KEYS, dict)


def test_keys_mapping_uses_nes_button_names_as_keys():
    """
    Objective:
    The mapping should be button-name -> pygame-key, matching the tutorial example.
    """
    assert set(main.KEYS) == {
        "a",
        "b",
        "select",
        "start",
        "up",
        "down",
        "left",
        "right",
    }


def test_keys_mapping_matches_default_manual_controls():
    """
    Objective:
    The default keyboard controls are simple and common for emulators.
    """
    assert main.KEYS["a"] == pygame.K_z
    assert main.KEYS["b"] == pygame.K_x
    assert main.KEYS["select"] == pygame.K_RSHIFT
    assert main.KEYS["start"] == pygame.K_RETURN
    assert main.KEYS["up"] == pygame.K_UP
    assert main.KEYS["down"] == pygame.K_DOWN
    assert main.KEYS["left"] == pygame.K_LEFT
    assert main.KEYS["right"] == pygame.K_RIGHT
