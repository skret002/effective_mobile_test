import os
import sys

import click

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))
from src.models.model import WalletAction


class WalletCLI:
    def __init__(self):
        self.cli = click.Group(help="Wallet CLI @by Tarasenko A.V ")

        # Регистрация команд
        self.cli.add_command(self.balance)
        self.cli.add_command(self.add_entry)
        self.cli.add_command(self.edit_entry)
        self.cli.add_command(self.search)
        self.cli.add_command(self.last_post)
        self.cli.add_command(self.delete_post)

    @click.command(help="Текущий баланс, доходы и расходы, вызывается без параметров")
    @click.pass_context
    def balance(self, ctx):
        """Показывает текущий баланс, доходы и расходы."""
        result = WalletAction.check_balance()
        if result:
            click.echo(f"Баланс: {result['balance']}")
            click.echo(f"Доходы: {result['income']}")
            click.echo(f"Расходы: {result['consumption']}")
        else:
            click.echo("Нет данных для отображения.")

    @click.command()
    @click.option("--category", prompt=True, help="Доход|Расход")
    @click.option("--value", prompt=True, type=float, help="Сумма операции")
    @click.option("--description", prompt=True, help="Описание операции")
    @click.option("--note", prompt=True, help="Примечание к операции")
    @click.pass_context
    def add_entry(ctx, category, value, description, note):
        """Добавление новой записи."""
        new_data = {
            "category": category,
            "value": value,
            "description": description,
            "note": note,
        }
        result = WalletAction.write_data(new_data)
        click.echo(result)

    @click.command()
    @click.option("--id", prompt=True, help="Введите Id записи")
    @click.pass_context
    def edit_entry(self, id):
        """Изменение существующей записи."""
        post = WalletAction.get_post(int(id))
        post["category"] = click.prompt(
            "Введите новую категорию", default=post["category"]
        )
        post["value"] = click.prompt(
            "Введите новую сумму операции", default=post["value"], type=float
        )
        post["description"] = click.prompt(
            "Введите новое описание операции", default=post["description"]
        )
        post["note"] = click.prompt(
            "Введите новое примечание к операции", default=post["note"]
        )
        WalletAction.write_data(post)
        click.echo("Изменения сохранены.")

    @click.command(help="Пример: main.py search 'смузи' или main.py search '25-07'")
    @click.argument("keyword", required=True)
    @click.pass_context
    def search(self, keyword):
        """Поиск по записям."""
        results = WalletAction.search_data(keyword)
        if results:
            click.echo(f"Найдено записей {len(results)} шт.")
            for result in results:
                click.echo(result[0])
        else:
            click.echo("Ничего не найдено по вашему запросу.")

    @click.command(help="Покажет последние 5 записей")
    @click.pass_context
    def last_post(self):
        """Поиск по записям."""
        results = WalletAction.get_some_last_post()
        if results:
            for result in results:
                click.echo(result[0])
        else:
            click.echo("Ничего не найдено по вашему запросу.")

    @click.command(help="Удаление записи по Id или 'YES' для удаления всех.")
    @click.option(
        "--id", prompt=True, type=str, help="Id записи или 'YES' для удаления всех."
    )
    @click.pass_context
    def delete_post(self, id):
        """Очистка."""
        try:
            id = int(id)
        except ValueError:
            if id == "YES":
                id = None
                click.echo("Удаляем все записи")
            else:
                click.echo(
                    "Неверный формат Id. Введите число или слово YES для удаления всех."
                )
        result = WalletAction.delete_post(id)
        click.echo(result)


def main():
    cli_app = WalletCLI().cli
    cli_app()


if __name__ == "__main__":
    main()