import typer
import sys
from typing import *
from rich import print
from rich.console import Console
from modules.Dictionary import (definition, say_aloud)
from modules.Utils import add_tag, fetch_word_history
from modules.Database import initializeDB
from modules.Banner import print_banner
from modules.Utils import show_list




console = Console(record=False, color_system="truecolor")
print_banner(console)   


# initialize the database with the tables if not already existing
initializeDB()



# app configuration
app = typer.Typer(
    name="Vocabulary Builder",
    add_completion=False,
    rich_markup_mode="rich",
    help=":book: [bold green]This is a dictionary and a vocabulary builder CLI.[/bold green]"
)


# add the commands
@app.command()
def bye():
    """
    Say bye to the CLI
    """
    print(":wave: [bold green]Bye bye![/bold green]")


# todo @anay: write PyTest for this. Cover all cases/flags/arguments
@app.command(rich_help_panel="Dictionary", help="📚 [bold blue]Lookup[/bold blue] a word in the dictionary")
def define(
    word: str = typer.Argument(..., help="Word to search"),
    short: Optional[bool] = typer.Option(False, "--short", "-s", help="Lightweight definitions."),
    pronounce: Optional[bool] = typer.Option(False, "--pronounce",  "-p", help="Pronounce the word."),
    tag: Optional[str] = typer.Option(None, "--tag", "-t", help="Tag the word in your vocabulary builder set.")
):
    """
    Shows the definition of WORD. 
    Adds it to the vocabulary builder list along with the timestamp if the user is logged in.
    """

    if short:
        definition(word, short=True)


    if not short:
        definition(word, short=False)
        
    
    if pronounce:
        say_aloud(query=word)
        
    if tag:
        add_tag(word, tag)
    
    if not tag:
        add_tag(word)
    


# todo @anay: add a command to show word list [either all or by tag or by date or by learning/mastered]
# by default export all words in a csv file
# OPTIONS/FLAGS will be (two or more can be used at once):
# -t, --tag TAGNAME: export words of a particular tag
# -l, --learning: export words from the learning list
# -m, --mastered: export words from the mastered list
# -f, --favorite: export words from the favorite list
# -d, --date DATE: export words from a particular date
# --most INT: export the most searched words (INT is the number of words to display)

@app.command(rich_help_panel="Vocabulary Builder", help="📝 [bold blue]Get a list of all your looked up words.[/bold blue]")
def list(
    favorite: Optional[bool] = typer.Option(False, "--favorite", "-f", help="Get a list of your favorite words."),
    learning: Optional[bool] = typer.Option(False, "--learning",  "-l", help="Get a list of words in your learning list."),
    mastered: Optional[bool] = typer.Option(None, "--mastered", "-m", help="Get a list of words in your mastered list."),
    tag: Optional[str] = typer.Option(None, "--tag", "-t", help="Get a list of words with a particular tag."),
    date: Optional[str] = typer.Option(None, "--date", "-d", help="Get a list of words from a particular date."),
    last: Optional[str] = typer.Option(10, "--last", "-L", help="Get a list of last searched words.")
):
    
    if favorite:
        show_list(favorite=True)
    if learning:
        show_list(learning=True)
    if mastered:
        show_list(mastered=True)
    if tag:
        show_list(tag=tag)
    if date:
        show_list(date=date)
    if last:
        show_list(last=last)
    else:
        show_list(favorite=False, learning=False, mastered=False, tag=False, date=False, last=None)    
        
# Make use of the following functions that you will be writing in Dictionary.py
# get_all_words()
# get_words_of_tag()
# get_words_from_learning_list()
# get_words_from_mastered_list()

    
    
# todo @anay: add export command to export the word list
# by default export all words in a csv file
# OPTIONS/FLAGS will be (two or more can be used at once):
# -t, --tag TAGNAME: export words of a particular tag
# -l, --learning: export words from the learning list
# -m, --mastered: export words from the mastered list
# -f, --favorite: export words from the favorite list
# -d, --date DATE: export words from a particular date
# -to-csv (default): export to csv file
# -to-PDF: export to PDF file


# todo @anay: add a command to import the word list
# by default import all words in a csv file
# OPTIONS/FLAGS will be (two or more can be used at once):
# -t, --tag TAGNAME: import words of a particular tag
# -l, --learning: import words from the learning list
# -m, --mastered: import words from the mastered list
# -f, --favorite: import words from the favorite list
# -d, --date DATE: import words from a particular date


# todo @anay: add a command to set word as favorite


# todo @atharva: add a command to get learning rate of the user
# OPTIONS/FLAGS will be (two or more can be used at once):
# --today: get learning rate today
# --week: get learning rate this week
# --month: get learning rate this month
# --year: get learning rate this year
# --graph: get learning rate graph


# todo @atharva: add a command to export flashcards (images)
# OPTIONS/FLAGS will be (two or more can be used at once):
# -t, --tag: export words of a particular tag


# todo @atharva: add a command to delete a word 
# OPTIONS/FLAGS will be (two or more can be used at once):
# DEFAULT: delete a specified word from the database
# -t, --tag: delete all words of a particular tag
# -l, --learning: delete all words from the learning list
# -m, --mastered: delete all words from the mastered list
# -f, --favorite: delete all words from the favorite list


# todo @atharva: add a command "about" to get software details. Banner, version, credits,



if __name__ == "__main__":
    app()
