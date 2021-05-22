import requests
import click
import textwrap
import random
import re

width = 0

TO_REPLACE = [
    "CDU / CSU",
    "CDU/CSU",
    r"/(?:<!(Europäischen|Europäische) )Union/",
    "CDU und CSU",
    "CDU",
    "CSU",
    "Freie Demokraten",
    "Liberalen",
    "Liberale",
    "FDP",
    "BÜNDNIS 90 / DIE GRÜNEN",
    "BÜNDNIS 90/DIE GRÜNEN",
    "Grünen",
    "PIRATENpartei",
    "alternative für deutschland",
    "Die Linken",
    "Die Linke",
    "Linken",
    "Linke",
    "Die Linkspartei.PDS",
    "unionsgeführten Regierungen",
    "SPD",
    "CDU/CSU",
    "GRÜNE",
    "FDP",
    "PIRATEN",
    "DIE LINKE",
    "NPD",
    "Die PARTEI",
    "AfD",
]


def replace_string_to_regex(replace_string):
    if replace_string.startswith("/") and replace_string.endswith("/"):
        return re.compile(replace_string[1:-1], re.IGNORECASE)

    return re.compile(re.escape(replace_string), re.IGNORECASE)


TO_REPLACE = list(map(replace_string_to_regex, TO_REPLACE))


def wrap_print(content, indent=0):
    global width
    print(
        textwrap.indent(
            textwrap.fill(content, (width if width else 80) - indent), " " * indent
        )
    )


@click.command()
def main():
    global width
    width = click.get_terminal_size()[0]

    while True:
        click.clear()

        # see https://stackoverflow.com/a/26445590 for color codes
        print(
            "Wilkommen zu ParteiDuell "
            + "\033[31mK\033[0m\033[33ml\033[0m\033[93m"
            + "\033[32mi\033[0m\033[34me\033[0m\033[35mh\033[0m"
        )
        print("")

        r = requests.get("https://api.parteiduell.de/list")
        json = r.json()[0]
        wrap_print(json["these"])
        print()
        statement = random.choice(list(json["possibleAnswers"].keys()))
        for replace_regex in TO_REPLACE:
            json["possibleAnswers"][statement] = replace_regex.sub(
                "█████", json["possibleAnswers"][statement]
            )

        print(json["possibleAnswers"][statement])

        keys = list(json["possibleAnswers"])
        print(", ".join(f"{i}: {answer}" for i, answer in enumerate(keys)))

        party = input("> ")
        try:
            party = int(party)
            party = keys[party]
        except ValueError as error:
            print(error)

        print()
        print()
        if statement == party:
            print("Richtig!")
        else:
            print(f"Falsch, diese Aussage war von {json['answer']}")
            print()
            print(f"Die Partei {party} hat folgendes Statement abgegeben:\n")
            wrap_print(json["possibleAnswers"][party], indent=4)
        print()
        click.pause()


if __name__ == "__main__":
    main()
