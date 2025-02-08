import tkinter as tk
from tkinter import PhotoImage
import subprocess
import os

# Function to launch Guess the Number
def launch_guess_the_number():
    game_path = os.path.join("guess_the_number", "guess_main.py")
    subprocess.Popen(["python", game_path])

# Function to launch Space Invaders
def launch_space_invaders():
    game_path = os.path.join("space_invaders", "space_main.py")
    subprocess.Popen(["python", game_path])

# Function to launch Snake Game
def launch_snake_game():
    game_path = os.path.join("snake", "snake_main.py")
    subprocess.Popen(["python", game_path])

# Function to launch Pong Game
def launch_pong_game():
    game_path = os.path.join("pong", "pong_main.py")
    subprocess.Popen(["python", game_path])

# Create the main Tkinter window
root = tk.Tk()
root.title("Game Launcher")
root.geometry("800x600")

# Add the background image
bg_image_path = "splash_background.png"
bg_image = PhotoImage(file=bg_image_path)  # Load the background image
bg_label = tk.Label(root, image=bg_image)
bg_label.place(relwidth=1, relheight=1)  # Fill the entire window

# Title label
title_label = tk.Label(
    root,
    text="Game Launcher",
    font=("Arial", 30, "bold"),
    bg="#000000",
    fg="#ffffff"
)
title_label.pack(pady=20)

# Subtitle label
subtitle_label = tk.Label(
    root,
    text="Choose your game and start playing!",
    font=("Arial", 16),
    bg="#000000",
    fg="#ffffff"
)
subtitle_label.pack(pady=10)

# Play Guess the Number button
guess_button = tk.Button(
    root,
    text="Play Guess the Number",
    font=("Arial", 18),
    bg="#3498db",
    fg="white",
    activebackground="#2980b9",
    activeforeground="white",
    relief="raised",
    width=20,
    command=launch_guess_the_number
)
guess_button.pack(pady=20)

# Play Space Invaders button
space_button = tk.Button(
    root,
    text="Play Space Invaders",
    font=("Arial", 18),
    bg="#e74c3c",
    fg="white",
    activebackground="#c0392b",
    activeforeground="white",
    relief="raised",
    width=20,
    command=launch_space_invaders
)
space_button.pack(pady=20)

# Play Snake Game button
snake_button = tk.Button(
    root,
    text="Play Snake Game",
    font=("Arial", 18),
    bg="#2ecc71",  # Green color for Snake
    fg="white",
    activebackground="#27ae60",
    activeforeground="white",
    relief="raised",
    width=20,
    command=launch_snake_game
)
snake_button.pack(pady=20)

# Play Pong Game button
pong_button = tk.Button(
    root,
    text="Play Pong Game",
    font=("Arial", 18),
    bg="#9b59b6",  # Purple color for Pong
    fg="white",
    activebackground="#8e44ad",
    activeforeground="white",
    relief="raised",
    width=20,
    command=launch_pong_game
)
pong_button.pack(pady=20)

# Exit button
exit_button = tk.Button(
    root,
    text="Exit",
    font=("Arial", 16),
    bg="#7f8c8d",
    fg="white",
    activebackground="#95a5a6",
    activeforeground="white",
    relief="raised",
    width=10,
    command=root.quit
)
exit_button.pack(pady=20)

# Run the Tkinter event loop
root.mainloop()
