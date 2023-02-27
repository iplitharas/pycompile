import questionary

answers = questionary.form(
    first=questionary.confirm("Would you like the next question?", default=True),
    second=questionary.select("Select item", choices=["item1", "item2", "item3"]),
    third=questionary.confirm("Are you amazed?", default=False),
).ask()

print(answers)
print(answers.get("third"))
