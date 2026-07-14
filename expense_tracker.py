import argparse
import json
from datetime import datetime


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        add_help=False,
        prog="expense-tracker",
    )

    subparsers = parser.add_subparsers(
        dest="command",
        required=True,
    )

    add_parser = subparsers.add_parser("add")
    update_parser = subparsers.add_parser("update")
    delete_parser = subparsers.add_parser("delete")
    list_parser = subparsers.add_parser("list")
    summary_parser = subparsers.add_parser("summary")

    description_parser = add_parser.add_argument(
        "--description",
        type=str,
        required=True,
    )

    amount_parser = add_parser.add_argument(
        "--amount",
        type=int,
        required=True,
    )
    month_parser = summary_parser.add_argument(
        "--month",
        type=int,
    )
    delete_id_parser = delete_parser.add_argument(
        "--id",
        type=int,
    )
    delete_all_parser = delete_parser.add_argument(
        "--all",
        action="store_true",
    )

    args = parser.parse_args()

    if args.command == "add":
        try:
            with open("expenses.json", "r") as file:
                data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            data = []
        if len(data) == 0:
            new_id = 1
        else:
            new_id = max(expense["id"] for expense in data) + 1
        expense = {
            "id": new_id,
            "date": datetime.now().strftime("%Y-%m-%d"),
            "description": args.description,
            "amount": args.amount,
        }
        data.append(expense)
        with open("expenses.json", "w") as file:
            json.dump(data, file, indent=4)
        print("Expense successfully added")

    elif args.command == "list":
        try:
            with open("expenses.json", "r") as file:
                data = json.load(file)
        except FileNotFoundError:
            data = []
        print(f"{'ID':<5} | {'Date':<15} | {'Description':<20} | {'Amount':<10}")
        print("==========================================================")

        for expense in data:
            print(
                f"{expense['id']:<5} |"
                f" {expense['date']:<15} |"
                f" {expense['description']:<20} |"
                f" ${expense['amount']:<10}"
            )
            print("----------------------------------------------------------")

    elif args.command == "summary":
        try:
            with open("expenses.json", "r") as file:
                data = json.load(file)
        except FileNotFoundError:
            data = []
        summary = 0
        for expense in data:
            summary += expense["amount"]
        print(f"Total expenses: ${summary}")

    elif args.command == "delete":
        if args.all and args.id is None:
            with open("expenses.json", "w") as file:
                json.dump([], file, indent=4)
            print("Expenses successfully deleted")

        elif args.id is not None:
            try:
                with open("expenses.json", "r") as file:
                    data = json.load(file)
            except FileNotFoundError:
                data = []

            cleaned_data = [expense for expense in data if expense["id"] != args.id]

            if len(cleaned_data) == len(data):
                print(f"Did not find an expense with ID = {args.id}")
            else:
                with open("expenses.json", "w") as file:
                    json.dump(cleaned_data, file, indent=4)

            print(f"Expense with ID =  {args.id} successfully deleted")
