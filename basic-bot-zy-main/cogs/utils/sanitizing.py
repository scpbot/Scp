def sanitize_emoji(emoji: str):
    if "<" in emoji:
        # Store the custom emojis ID
        try:
            emoji = emoji.split(":")[-1].split(">")[0]
        except KeyError:
            pass
    return emoji
