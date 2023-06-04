import pygame

# Define the ABC notation for a simple melody
abc_notation = """
X:1
T:Example Melody
M:4/4
L:1/4
K:C
C D E F | G A B c | d e f g | a b c' d' | e' d' c' B A | G F E D
"""


# Define a function to parse the ABC notation
def parse_abc(abc):
    notes = []
    for line in abc.split("\n"):
        if not line:  # Check if line is empty
            continue
        if line.startswith("K:"):
            key = line[2]
        elif line.startswith("L:"):
            note_length = int(line[2])
        elif line[0] in "ABCDEFGabcdefg":
            pitch = line[0]
            if pitch.islower():
                pitch = chr(ord(pitch) - 32) + ","
            notes.append((pitch, note_length))
    return key, notes


# Parse the ABC notation
key, notes = parse_abc(abc_notation)

# Initialize the Pygame library for playing sounds
pygame.init()

# Set the tempo
tempo = 120

# Loop through each note in the melody
for pitch, note_length in notes:
    # Calculate the duration of the note
    duration = int(note_length * 1000 * 60 / tempo)

    # Load the sound file for the pitch
    sound = pygame.mixer.Sound("{}.wav".format(pitch))

    # Play the sound
    sound.play()

    # Wait for the duration of the note
    pygame.time.wait(duration)

# Quit the Pygame library
pygame.quit()
