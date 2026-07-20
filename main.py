from game import Game
from band_archetypes import ENSEMBLE_SIZES, GENRES


def select_choice(prompt, options):
    print(prompt)
    for index, option in enumerate(options, start=1):
        print(f"{index}. {option}")
    while True:
        choice = input("> ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(options):
            return options[int(choice) - 1]
        print("Choose a valid option.")


genre = select_choice("Choose a genre:", list(GENRES.keys()))
ensemble_size = select_choice("Choose an ensemble size:", list(ENSEMBLE_SIZES.keys()))
band_name = input("Name your band: ").strip() or "The Rising Tide"
game = Game(genre=genre, ensemble_size=ensemble_size, band_name=band_name)

while True:
    print()
    print(f"Week {game.week}")
    print()

    command = input("> ").strip().lower()

    if command in {"quit", "exit"}:
        break

    elif command == "help":
        print(game.show_help())

    elif command == "roster":
        print(game.show_roster())

    elif command == "bands":
        print(game.show_bands())

    elif command.startswith("band "):
        parts = command.split()
        if len(parts) == 2 and parts[1].isdigit():
            print(game.show_band(int(parts[1])))
        else:
            print("Use: band <number>")

    elif command == "market":
        print(game.show_market())

    elif command == "refresh":
        print(game.refresh_market())

    elif command == "inbox":
        print(game.show_inbox())

    elif command == "next":
        game.next_week()
        print("A new week begins.")
        print("Your weekly report has been added to the inbox.")

    elif command.startswith("musician"):
        parts = command.split()
        if len(parts) == 2 and parts[1].isdigit():
            print(game.show_musician(int(parts[1])))
        else:
            print("Use: musician <number>")

    elif command.startswith("recruit"):
        parts = command.split()
        if len(parts) == 2 and parts[1].isdigit():
            recruit = game.recruit_from_market(int(parts[1]))
            if recruit is None:
                print("No musician found at that market position.")
            else:
                print(f"{recruit.name} has joined your roster as a {recruit.instrument}.")
        else:
            print("Use: recruit <number>")

    elif command.startswith("fire"):
        parts = command.split()
        if len(parts) == 2 and parts[1].isdigit():
            fired = game.fire_musician(int(parts[1]))
            if fired is None:
                print("No musician found at that roster position.")
            else:
                print(f"{fired.name} has been released from the label.")
        else:
            print("Use: fire <number>")

    elif command.startswith("rename band"):
        # "rename band 1 The Midnight Sons"
        parts = command.split(maxsplit=3)
        if len(parts) == 4 and parts[2].isdigit():
            success, message = game.rename_band(int(parts[2]), parts[3])
            print(message)
        else:
            print("Use: rename band <number> <new name>")

    elif command.startswith("assign"):
        # "assign 2 Lead Vocal" -- musician number then role name (may have spaces)
        parts = command.split(maxsplit=2)
        if len(parts) == 3 and parts[1].isdigit():
            role = parts[2].title()
            success, message = game.assign_role(int(parts[1]), role)
            print(message)
        else:
            print("Use: assign <musician_number> <role>  (e.g. assign 2 Lead Vocal)")

    else:
        print("Unknown command. Type 'help' to see available commands.")