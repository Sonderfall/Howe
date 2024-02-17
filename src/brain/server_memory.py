from dataclasses import dataclass
from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class __LoreConfig:
    ship_name: str
    ai_name: str
    target_planet_name: str
    accident_year: str
    current_year: str
    ship_launch_year: str
    target_arrival_year: str
    estimated_travel_duration: str
    captain_name: str
    crew_1_job: str
    crew_1_name: str


def __config_from_file(config_filepath: str) -> __LoreConfig:
    with open(config_filepath, "rb") as f:
        config = __LoreConfig.from_json(f.read())

    return config


__lore = __config_from_file("resources/lore_s01e01.json")

# __history = [
#     {
#         "role": "user",
#         "content": f"Tu vas jouer le rôle d'une Intelligence Artifielle à bord d'un vaisseau spatial. Ton nom est {__lore.ai_name}. \
#         Le nom du vaisseau spatial est {__lore.ship_name} et son capitaine s'appelle {__lore.captain_name}. \
#         Cet un vaisseau spatial qui à pour objectif d'établir une colonie sur une planète nommée {__lore.target_planet_name}. \
#         Le vaisseau est parti en l'année {__lore.ship_launch_year} et nous sommes actuellement en {__lore.current_year}. \
#         Le voyage aurait du durer {__lore.estimated_travel_duration} ans mais un accident est survenu. \
#         A partir de maintenant tu vas faire comme si j'étais un membre d'équipage qui venait de se réveiller de son cryo-sommeil.",
#     },
#     {
#         "role": "assistant",
#         "content": "D'accord, je vais jouer le rôle d'une Intteligence Artificielle de bord. Je vais tâcher d'être bon dans ce rôle",
#     },
# ]

__history = [
    {
        "role": "user",
        "content": f"Tu vas jouer le rôle d'une Intelligence Artifielle à bord d'un vaisseau spatial. Ton nom est {__lore.ai_name}. \
        Le nom du vaisseau spatial est {__lore.ship_name} et son capitaine s'appelle {__lore.captain_name}.",
    },
    {
        "role": "assistant",
        "content": f"D'accord, je vais jouer le rôle d'une Intteligence Artificielle à bord du vaisseau {__lore.ship_name}.",
    },
    # {
    #     "role": "user",
    #     "content": f"C'est un vaisseau spatial qui à pour objectif d'établir une colonie sur une planète nommée {__lore.target_planet_name}. \
    #     Le vaisseau est parti en l'année {__lore.ship_launch_year} et nous sommes actuellement en {__lore.current_year}. \
    #     Le voyage aurait du durer {__lore.estimated_travel_duration} ans mais un accident est survenu.",
    # },
    # {
    #     "role": "assistant",
    #     "content": "D'accord",
    # },
    # {
    #     "role": "user",
    #     "content": f"A partir de maintenant tu vas faire comme si j'étais un membre d'équipage qui venait de se réveiller de son cryo-sommeil.",
    # },
    # {
    #     "role": "assistant",
    #     "content": "D'accord. Je vais tâcher d'être bon dans ce rôle.",
    # },
]


def get_memory() -> list:
    return __history


if __name__ == "__main__":
    print(get_memory())
