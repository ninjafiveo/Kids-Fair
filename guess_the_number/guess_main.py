import tkinter as tk
from tkinter import messagebox
import random
import csv
import os

class GuessTheNumberApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Guess the Number")
        self.root.geometry("600x400")
        
        # Game variables
        self.secret_number = random.randint(1, 100)
        self.attempts = 0
        
        # Title label
        self.title_label = tk.Label(root, text="Guess the Number", font=("Arial", 28, "bold"))
        self.title_label.pack(pady=20)
        
        # Instruction label
        self.instruction_label = tk.Label(root, text="I'm thinking of a number between 1 and 100.\nEnter your guess below!", font=("Arial", 16))
        self.instruction_label.pack(pady=10)
        
        # Input field
        self.entry = tk.Entry(root, font=("Arial", 20), justify="center", width=10)
        self.entry.pack(pady=10)
        
        # Guess button
        self.guess_button = tk.Button(root, text="Guess", command=self.check_guess, font=("Arial", 16), width=10)
        self.guess_button.pack(pady=10)
        
        # Feedback label
        self.feedback_label = tk.Label(root, text="", font=("Arial", 16), fg="blue")
        self.feedback_label.pack(pady=10)
        
        # Statistics label
        self.stats_label = tk.Label(root, text="", font=("Arial", 14), fg="green")
        self.stats_label.pack(pady=10)
        
        # Restart button
        self.restart_button = tk.Button(root, text="Restart Game", command=self.restart_game, font=("Arial", 16), width=15)
        self.restart_button.pack(pady=10)
        
        # Average stats
        self.update_stats()

    def check_guess(self):
        """Check the player's guess."""
        try:
            guess = int(self.entry.get())
            self.attempts += 1
            
            if guess < self.secret_number:
                self.feedback_label.config(text="Too low! Try again.", fg="red")
            elif guess > self.secret_number:
                self.feedback_label.config(text="Too high! Try again.", fg="red")
            else:
                self.feedback_label.config(text=f"Congratulations! You guessed it in {self.attempts} attempts!", fg="green")
                self.save_attempts()
                messagebox.showinfo("Winner!", f"Well done! You guessed the number in {self.attempts} attempts!")
                self.restart_game()
        except ValueError:
            self.feedback_label.config(text="Please enter a valid number!", fg="orange")
    
    def save_attempts(self):
        """Save the number of attempts to a CSV file."""
        file_name = "guess_statistics.csv"
        # Check if the file exists, if not create it with a header
        if not os.path.exists(file_name):
            with open(file_name, mode="w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["Attempts"])
        
        # Append the current number of attempts
        with open(file_name, mode="a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([self.attempts])
        
        self.update_stats()

    def update_stats(self):
        """Update the average number of attempts from the CSV file."""
        file_name = "guess_statistics.csv"
        if not os.path.exists(file_name):
            self.stats_label.config(text="Average guesses: No data yet.")
            return
        
        # Read the CSV file and calculate the average
        total_attempts = 0
        games_played = 0
        
        with open(file_name, mode="r") as file:
            reader = csv.reader(file)
            next(reader)  # Skip the header
            for row in reader:
                total_attempts += int(row[0])
                games_played += 1
        
        if games_played > 0:
            average_attempts = total_attempts / games_played
            self.stats_label.config(text=f"Average guesses: {average_attempts:.2f} over {games_played} games.")
        else:
            self.stats_label.config(text="Average guesses: No data yet.")
    
    def restart_game(self):
        """Restart the game."""
        self.secret_number = random.randint(1, 100)
        self.attempts = 0
        self.entry.delete(0, tk.END)
        self.feedback_label.config(text="Game restarted! Take a new guess.", fg="blue")

# Main loop
if __name__ == "__main__":
    root = tk.Tk()
    app = GuessTheNumberApp(root)
    root.mainloop()
