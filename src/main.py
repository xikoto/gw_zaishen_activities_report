from config import load_config
from discord_client import send_message


config = load_config()

print("Zaishen Activities Report")

if config["discord"]["enabled"]:
    send_message("Hola que tal soy colosal")
    print("Mensaje enviado a Discord")