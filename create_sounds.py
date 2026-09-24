import wave
import math
import struct
import os


# ============================================================
# CREATE FOLDER
# ============================================================

os.makedirs(
    "sounds",
    exist_ok=True
)


# ============================================================
# CREATE WAV
# ============================================================

def create_wav(
    filename,
    frequencies,
    duration=0.2
):

    sample_rate = 44100

    amplitude = 16000

    samples = int(
        sample_rate * duration
    )

    with wave.open(
        filename,
        "w"
    ) as wav:

        wav.setnchannels(1)

        wav.setsampwidth(2)

        wav.setframerate(
            sample_rate
        )

        for i in range(samples):

            t = i / sample_rate

            frequency = frequencies[
                min(
                    int(
                        t
                        /
                        duration
                        *
                        len(frequencies)
                    ),
                    len(frequencies) - 1
                )
            ]

            value = (
                amplitude
                *
                math.sin(
                    2
                    * math.pi
                    * frequency
                    * t
                )
            )

            # Fade out
            fade = 1 - (
                t / duration
            )

            value *= fade

            data = struct.pack(
                "<h",
                int(value)
            )

            wav.writeframes(
                data
            )


# ============================================================
# EAT SOUND
# ============================================================

create_wav(
    "sounds/eat.wav",
    [
        600,
        800,
        1000
    ],
    0.18
)


# ============================================================
# GAME OVER SOUND
# ============================================================

create_wav(
    "sounds/game_over.wav",
    [
        500,
        400,
        300,
        200
    ],
    0.7
)


print(
    "Sounds created successfully!"
)

print(
    "sounds/eat.wav"
)

print(
    "sounds/game_over.wav"
)
