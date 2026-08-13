from config import load_config


config = load_config()

print("Zaishen Activities Report")
print(f"URL: {config['scraper']['url']}")
print(f"Timeout: {config['scraper']['timeout']} segundos")
print(
    f"Schedule: "
    f"{config['schedule']['hour']:02d}:"
    f"{config['schedule']['minute']:02d} "
    f"({config['schedule']['timezone']})"
)
print(f"Discord enabled: {config['discord']['enabled']}")
print(f"Results directory: {config['storage']['results_directory']}")