import os
from io import BytesIO
from pathlib import Path

import aiohttp
import discord
import face_recognition
import numpy
from discord.ext import commands
from dotenv import load_dotenv

IMAGE_PATH = Path.cwd() / "images"
ENCODING_PATH = Path.cwd() / "encodings"

for image_file in IMAGE_PATH.glob("*.jpg"):
    print(f"Encoding {image_file.name}")
    image_encoding_file = ENCODING_PATH / (image_file.stem + ".npy")

    if image_encoding_file.exists():
        print("Encoding already exists")
        continue

    image_data = face_recognition.load_image_file(image_file)
    encodings = face_recognition.face_encodings(image_data, num_jitters=25)

    if len(encodings) != 1:
        print(
            f"{image_file.name} has an invalid number of encodings ({len(encodings)})."
        )
        continue

    numpy.save(image_encoding_file, encodings[0])
    print("Encoding saved.")

ENCODINGS = {
    "jack": [],
    "mitch": [],
}

for encoding_file in ENCODING_PATH.iterdir():
    encoding = numpy.load(encoding_file)
    name = encoding_file.stem.split("_")[0]
    ENCODINGS[name].append(encoding)


load_dotenv()

bot = commands.Bot(command_prefix="😟 ")


@bot.event
async def on_message(message: discord.Message):
    for attachment in message.attachments:
        if not any(
            attachment.filename.lower().endswith(extension)
            for extension in [".png", ".jpg", ".jpeg"]
        ):
            continue

        async with aiohttp.ClientSession(loop=bot.loop) as session:
            async with session.get(attachment.url) as response:
                image_bytes = await response.content.read()
                image_file = BytesIO(image_bytes)

        image = face_recognition.load_image_file(image_file)
        encodings = face_recognition.face_encodings(image, num_jitters=25)

        jack_found = False
        mitch_found = False

        for encoding in encodings:
            jack_matches = face_recognition.compare_faces(
                ENCODINGS["jack"], encoding, tolerance=0.5
            )
            mitch_matches = face_recognition.compare_faces(
                ENCODINGS["mitch"], encoding, tolerance=0.5
            )
            if any(jack_matches):
                jack_found = True
            if any(mitch_matches):
                mitch_found = True

        if jack_found and mitch_found:
            await message.reply(
                "guys somtimes :anguished:  i get really worried :persevere: that mitch and jack aren't in the same room :cry: and then i check #general :astonished: and there is a new photo of them  :star_struck:  so i know that they are in the same room :partying_face:"
            )


bot.run(os.environ["IGRW_TOKEN"])
