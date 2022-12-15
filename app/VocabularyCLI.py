from modules.About import *
from modules.Banner import print_banner
from modules.Database import *
from modules.Dictionary import definition, say_aloud
from modules.ImportExport import *
from modules.Study import *
from modules.Thesaurus import *
from modules.Utils import *
from modules.Graph import *
from modules.Flashcard import *
from modules.WordCollections import *

import sys
import typer
from typing import *
from rich import print
from rich.console import Console
from datetime import datetime

# app configuration
app = typer.Typer(
    name="Vocabulary Builder",
    add_completion=True,
    rich_markup_mode="rich",
    help=":book: [bold green]This is a dictionary and a vocabulary builder CLI.[/bold green]"
)


# initialize the database with the tables if not already existing
initializeDB()

# add all the collection words to the database if not already existing
insert_collection_to_DB()

@app.command(rich_help_panel="Vocabulary Builder", help="👋🏼 [bold red]Exits[/bold red] the CLI")
def bye():
    print(Panel(":wave: [bold green]Bye bye![/bold green]"))
    sys.exit(0)


@app.command(rich_help_panel="Vocabulary Builder", help="🔄 Update the JSON response in the cache")
def refresh():
    """
    Refreshes the cached content from the API.
    """
    refresh_cache()


@app.command(rich_help_panel="Vocabulary Builder", help="📚 [bold blue]Lookup[/bold blue] a word in the dictionary")
def define(
    words: List[str] = typer.Argument(..., help="Word to search"),
    short: Optional[bool] = typer.Option(False, "--short", "-s", help="Lightweight definitions."),
    pronounce: Optional[bool] = typer.Option(False, "--pronounce",  "-p", help="Pronounce the word."),
):
    """
    Looks up a word in the dictionary.

    Args:
        words (List[str]): Word which is to be defined.
        short (Optional[bool], optional): If True, prints the short definition of the word. Defaults to False.
        pronounce (Optional[bool], optional): If True, plays the pronunciation of the word. Defaults to False.
    """

    for word in words:
        if short:
            definition(word, short=True)

        if not short:
            definition(word, short=False)

        if pronounce:
            say_aloud(query=word)


# todo @anay: add flag to show words with one line def. Call the flag as --showDefs: Optional[boolean]
@app.command(rich_help_panel="Vocabulary Builder", help="📝 [bold blue]Lists [/bold blue] of all your looked up words")
def list(
    favorite: Optional[bool] = typer.Option(False, "--favorite", "-f", help="Get a list of your favorite words."),
    learning: Optional[bool] = typer.Option(False, "--learning",  "-l", help="Get a list of words in your learning list."),
    mastered: Optional[bool] = typer.Option(None, "--mastered", "-m", help="Get a list of words in your mastered list."),
    tag: Optional[str] = typer.Option(None, "--tag", "-t", help="Get a list of words with a particular tag."),
    days: Optional[int] = typer.Option(None, "--days", "-d", help="Get a list of words from last n number of days."),
    date: Optional[bool] = typer.Option(False, "--date", "-D", help="Get a list of words from a particular date."),
    last: Optional[int] = typer.Option(None, "--last", "-L", help="Get a list of last searched words."),
    most: Optional[int] = typer.Option(None, "--most", "-M", help="Get a list of most searched words."),
    tagnames: Optional[bool] = typer.Option(False, "--tagnames", "-T", help="Get a list of all the tags."),
):
    """
    Lists all the words looked up by the user.

    Args:
        favorite (Optional[bool], optional): If True, prints the list of favorite words. Defaults to False.
        learning (Optional[bool], optional): If True, prints the list of words in learning list. Defaults to False.
        mastered (Optional[bool], optional): If True, prints the list of words in mastered list. Defaults to False.
        tag (Optional[str], optional): If True, prints the list of words with a particular tag. Defaults to None.
        days (Optional[str], optional): If True, prints the list of words from last n number of days. Defaults to None.
        date (Optional[str], optional):  If True, prints the list of words from a particular date. Defaults to None.
        last (Optional[str], optional): If True, prints the list of last searched words. Defaults to None.
        most (Optional[str], optional): If True, prints the list of most searched words. Defaults to None.
        tagnames (Optional[bool], optional): If True, prints the list of all the tags. Defaults to False.
    """

    if favorite:
        show_list(favorite=True)
    if learning:
        show_list(learning=True)
    if mastered:
        show_list(mastered=True)
    if tag:
        show_list(tag=tag)
    if days:
        show_list(days=days)
    if date:
            show_list(date=date)
    if last:
        show_list(last=last)
    if most:
        show_list(most=most)
    if tagnames:
        show_list(tagnames=True)
    elif not any([favorite, learning, mastered, tag, days, date, last, most]):
        show_list()


@app.command(rich_help_panel="Vocabulary Builder", help="💙 [bold green]Sets[/bold green] a word as [bold gold1]favorite[/bold gold1]")
def favorite(
    words: List[str] = typer.Argument(..., help="Word to add to favorites."),
):
    """
    Adds a word to the favorite list.

    Args:
        words (List[str]): Word which is to be added to the favorite list.
    """

    for word in words:
        set_favorite(word)


@app.command(rich_help_panel="Vocabulary Builder", help="💔 [bold red]Removes[/bold red] the word from [bold gold1]favorites[/bold gold1]")
def unfavorite(
    words: List[str] = typer.Argument(..., help="Word to remove from favorites"),
):
    """
    Removes a word from the favorite list.

    Args:
        words (List[str]): Word which is to be removed from the favorite list.
    """

    for word in words:
        set_unfavorite(word)


@app.command(rich_help_panel="Vocabulary Builder", help="✍🏼 [bold green]Sets[/bold green] a word as [bold blue]learning[/bold blue]")
def learn(
    words: List[str] = typer.Argument(..., help="Word to add to learning."),
):
    """
    Adds a word to the learning list.

    Args:
        words (List[str]): Word which is to be added to the learning list.
    """

    for word in words:
        set_learning(word)


@app.command(rich_help_panel="Vocabulary Builder", help="😪 [bold red]Removes[/bold red] the word from [bold blue]learning[/bold blue]")
def unlearn(
    words: List[str] = typer.Argument(..., help="Word to remove from learning"),
):
    """
    Removes a word from the learning list.

    Args:
        words (List[str]): Word which is to be removed from the learning list.
    """

    for word in words:
        set_unlearning(word)


@app.command(rich_help_panel="Vocabulary Builder", help="🧠 [bold green]Sets[/bold green] a word as [bold green]mastered[/bold green]")
def master(
    words: List[str] = typer.Argument(..., help="Word to add to mastered."),
):
    """
    Adds a word to the mastered list.

    Args:
        words (List[str]): Word which is to be added to the mastered list.
    """

    for word in words:
        set_mastered(word)


@app.command(rich_help_panel="Vocabulary Builder", help="🤔 [bold red]Removes[/bold red] the word from [bold green]mastered[/bold green]")
def unmaster(
    words: List[str] = typer.Argument(..., help="Word to remove from mastered"),
):
    """
    Removes a word from the mastered list.

    Args:
        words (List[str]): Word which is to be removed from the mastered list.
    """

    for word in words:
        set_unmastered(word)


@app.command(rich_help_panel="Import / Export", help="📂 [bold blue]Exports[/bold blue] a list of all your looked up words")
def export(
    pdf: Optional[bool] = typer.Option(False, "--pdf", "-P", help="Export a list of your looked up words in PDF format."),
):
    """
    Exports a list of all your looked up words.

    Args:
        pdf (Optional[bool], optional): If True, exports a list of your looked up words in PDF format. Defaults to False.
    """

    if pdf:
        export_to_pdf()
    else:
        export_to_csv()


@app.command("import", rich_help_panel="Import / Export", help="🔼 [bold blue]Imports[/bold blue] a list words in the application")
def Import():
    """
    Imports a list of words in the application.
    """

    import_from_csv()


@app.command(rich_help_panel="Vocabulary Builder", help="🔖 [bold blue]Tags[/bold blue] a word")
def tag(
    words: List[str] = typer.Argument(..., help="Words to tagged"),
    tag: str = typer.Option(..., "--name", "-n", help="Tag to add to the words"),
):
    """
    Tags a word.

    Args:
        words (List[str]): Words to tagged.
        tag (str): Tag to add to the words.
    """

    for word in words:
        add_tag(word, tag)


@app.command(rich_help_panel="Vocabulary Builder", help="✂ [bold red] Removes[/bold red] tag of a word in the dictionary")
def untag(
    words: List[str] = typer.Argument(..., help="Word to remove tag from"),
):
    """
    Remove tag of a word in the dictionary.

    Args:
        words (List[str]): Word to remove tag from.
    """

    for word in words:
        remove_tag(word)


@app.command(rich_help_panel="Vocabulary Builder", help="💻 [bold blue]About[/bold blue] the software")
def about():
    """
    Print information about the software.
    """

    console = Console(record=False, color_system="truecolor")
    print_banner(console)
    print_about_app()


@app.command(rich_help_panel="Vocabulary Builder", help="📊 [bold blue]Learning Rate[/bold blue] gives the number of words you have learned in a particular time period with a comparison of a previous time period")
def rate(
    today: Optional[bool] = typer.Option(False, "--today", "-t", help="Get learning rate today"),
    week: Optional[bool] = typer.Option(False, "--week", "-w", help="Get learning rate this week"),
    month: Optional[bool] = typer.Option(False, "--month", "-m", help="Get learning rate this month"),
    year: Optional[bool] = typer.Option(False, "--year", "-y", help="Get learning rate this year"),
):
    """
    Gives the number of words you have learned in a particular time period with a comparison of a previous time period.

    Args:
        today (Optional[bool], optional): If True, get learning rate today. Defaults to False.
        week (Optional[bool], optional): If True, get learning rate this week. Defaults to False.
        month (Optional[bool], optional): If True, get learning rate this month. Defaults to False.
        year (Optional[bool], optional): If True, get learning rate this year. Defaults to False.
    """

    if today:
        get_lookup_rate(today=True)
    elif week:
        get_lookup_rate(week=True)
    elif month:
        get_lookup_rate(month=True)
    elif year:
        get_lookup_rate(year=True)
    elif not any([today, week, month, year]):
        # default is today
        get_lookup_rate(today=True)



@app.command(rich_help_panel="Thesaurus", help="🔎 Find [bold pink]synonyms[/bold pink] for a word")
def synonym(
    words: List[str] = typer.Argument(..., help="Word to search synonyms for"),
):
    """
    Find synonyms for a word.

    Args:
        words (List[str]): Word to search synonyms for.
    """

    for word in words:
        find_synonym(word)


@app.command(rich_help_panel="Thesaurus", help="❌ Find [bold pink]antonyms[/bold pink] for a word")
def antonym(
    words: List[str] = typer.Argument(..., help="Word to search antonyms for"),
):
    """
    Find antonyms for a word.

    Args:
        words (List[str]): Word to search antonyms for.
    """

    for word in words:
        find_antonym(word)


@app.command(rich_help_panel="Vocabulary Builder", help="🔁 Get a lookup history of a word")
def history(
    words: List[str] = typer.Argument(..., help="Word to get lookup history for"),
):
    """
    Get a lookup history of a word.

    Args:
        words (List[str]): Word to get lookup history for.
    """

    for word in words:
        fetch_word_history(word)


@app.command(rich_help_panel="Vocabulary Builder", help="🚮 Deletes the word from the database")
def delete(
    mastered: Optional[bool] = typer.Option(False, "--mastered", "-m", help="Deletes all mastered words"),
    learning: Optional[bool] = typer.Option(False, "--learning", "-l", help="Deletes all learning words"),
    favorite: Optional[bool] = typer.Option(False, "--favorite", "-f", help="Deletes all favorite words"),
    tag: Optional[str] = typer.Option(None, "--tag", "-t", help="Tag of words to be deleted"),
    words: List[str] = typer.Argument(None, help="Word to be deleted"),
):
    """
    Deletes the word from the database.

    Args:
        mastered (Optional[bool], optional): Deletes all mastered words. Defaults to False.
        learning (Optional[bool], optional): Deletes all learning words. Defaults to False.
        favorite (Optional[bool], optional): Deletes all favorite words. Defaults to False.
        tag (Optional[str], optional): Tag of words to be deleted. Defaults to None.
        words (List[str], optional): Word to be deleted. Defaults to None.
    """


    if mastered:
        print(Panel.fit(title="[b reverse yellow]  Warning!  [/b reverse yellow]", 
                title_align="center",
                padding=(1, 1),
                renderable="🛑 [bold red]DANGER[/bold red] Are you sure you want to delete [b]all words from your mastered list[/b]?")
        )

        if sure := typer.confirm(""):
            delete_mastered()
        else:
            print(Panel("OK, not deleting anything."))

    elif learning:
        print(Panel.fit(title="[b reverse yellow]  Warning!  [/b reverse yellow]", 
                title_align="center",
                padding=(1, 1),
                renderable="🛑 [bold red]DANGER[/bold red] Are you sure you want to delete [b]all words from your learning list[/b]?")
        )
        if sure := typer.confirm(""):
            delete_learning()
        else:
            print(Panel("OK, not deleting anything."))

    elif favorite:
        print(Panel.fit(title="[b reverse yellow]  Warning!  [/b reverse yellow]", 
                title_align="center",
                padding=(1, 1),
                renderable="🛑 [bold red]DANGER[/bold red] Are you sure you want to delete [b]all words from your favorite list[/b]?")
        )
        if sure := typer.confirm(""):
            delete_favorite()
        else:
            print(Panel("OK, not deleting anything."))

    elif tag:
        print(Panel.fit(title="[b reverse yellow]  Warning!  [/b reverse yellow]", 
                title_align="center",
                padding=(1, 1),
                renderable=f"🛑 [bold red]DANGER[/bold red] Are you sure you want to delete [b]all words from tag {tag}[/b]?")
        )
        if sure := typer.confirm(""):
            delete_words_from_tag(tag)
        else:
            print(Panel("OK, not deleting anything."))

    elif words:
        print(Panel.fit(title="[b reverse yellow]  Warning!  [/b reverse yellow]", 
                title_align="center",
                padding=(1, 1),
                renderable="🛑 [bold red]DANGER[/bold red] Are you sure you want to delete [b]all words from your list[/b]?")
        )
        if sure := typer.confirm(""):
            for word in words:
                delete_word(word)
        else:
            print(Panel("OK, not deleting anything."))

    elif not any([mastered, learning, favorite, tag, words]):
        print(Panel.fit(title="[b reverse yellow]  Warning!  [/b reverse yellow]", 
                title_align="center",
                padding=(1, 1),
                renderable="🛑 [bold red]DANGER[/bold red] Are you sure you want to delete [b]all words from your list[/b]?")
        )
        if sure := typer.confirm(""):
            delete_all()
        else:
            print(Panel("OK, not deleting anything."))


# todo @atharva should add a function to clear tags of all the words
@app.command(rich_help_panel="Vocabulary Builder", help="🧹 [bold red]Clears[/bold red] all lists")
def clear(
    learning: Optional[bool] = typer.Option(False, "--learning", "-l", help="Clear all words in your learning list"),
    master: Optional[bool]= typer.Option(False, "--mastered", "-m", help="Clear all words in your mastered list"),
    favorite: Optional[bool] = typer.Option(False, "--favorite", "-f", help="Clear all words in your favorite list"),
    tag: Optional[str] = typer.Option(None, "--tag", "-t", help="Clear all words with a particular tag"),
):
    """
    Clears all the words from the lists.

    Args:
        learning (Optional[bool], optional): If True, clears all the words from the learning list. Defaults to False.
        master (Optional[bool], optional): If True, clears all the words from the mastered list. Defaults to False.
        favorite (Optional[bool], optional): If True, clears all the words from the favorite list. Defaults to False.
        tag (Optional[str], optional): If True, clears all the words with a particular tag. Defaults to None.
    """

    if learning:
        print(Panel.fit(title="[b reverse yellow]  Warning!  [/b reverse yellow]", 
                title_align="center",
                padding=(1, 1),
                renderable="🛑 [bold red]DANGER[/bold red] Are you sure you want to clear [b]all words from your learning list[/b]?")
        )
        if sure := typer.confirm(""):
            clear_learning()
        else:
            print(Panel("OK, not clearing anything."))

    elif master:
        print(Panel.fit(title="[b reverse yellow]  Warning!  [/b reverse yellow]", 
                title_align="center",
                padding=(1, 1),
                renderable="🛑 [bold red]DANGER[/bold red] Are you sure you want to clear [b]all words from your mastered list[/b]?")
        )
        if sure := typer.confirm(""):
            clear_mastered()
        else:
            print(Panel("OK, not clearing anything."))

    elif favorite:
        print(Panel.fit(title="[b reverse yellow]  Warning!  [/b reverse yellow]", 
                title_align="center",
                padding=(1, 1),
                renderable="🛑 [bold red]DANGER[/bold red] Are you sure you want to clear [b]all words from your favorite list[/b]?")
        )
        if sure := typer.confirm(""):
            clear_favorite()
        else:
            print(Panel("OK, not clearing anything."))

    elif tag:
        print(Panel.fit(title="[b reverse yellow]  Warning!  [/b reverse yellow]", 
                title_align="center",
                padding=(1, 1),
                renderable=f"🛑 [bold red]DANGER[/bold red] Are you sure you want to clear [b]all words from your tag {tag}[/b]?")
        )
        if sure := typer.confirm(""):
            clear_all_words_from_tag(tag)
        else:
            print(Panel(f"OK, not clearning any words from the tag {tag}."))


# todo - add more flags/options
@app.command(rich_help_panel="Vocabulary Builder", help="🔀 Gets a random word")
def random(
    learning: Optional[bool] = typer.Option(False, "--learning", "-l", help="Get a random learning word"),
    mastered: Optional[bool] = typer.Option(False, "--mastered", "-m", help="Get a random mastered word"),
    favorite: Optional[bool] = typer.Option(False, "--favorite", "-f", help="Get a random favorite word"),
    tag: Optional[str] = typer.Option(None, "--tag", "-t", help="Get a random word from a particular tag"),
):
    """
    Gets a random word.

    Args:
        learning (Optional[bool], optional): Get a random learning word. Defaults to False.
        mastered (Optional[bool], optional): Get a random mastered word. Defaults to False.
    """

    if learning:
        get_random_word_from_learning_set()
    elif mastered:
        get_random_word_from_mastered_set()
    elif favorite:
        get_random_word_from_favorite_set()
    elif tag:
        get_random_word_from_tag(tag)
    elif not any([learning, mastered, tag]):
        get_random_word_definition_from_api()


# todo - need to write the function
@app.command(rich_help_panel="study", help="💡 Revise words from your learning list")
def revise(
    number: Optional[int] = typer.Option(None, "--number", "-n", help="Number of words to revise in random order."),
    tag: Optional[str] = typer.Option(None, "--tag", "-t", help="Revise words in a particular tag."),
    learning: Optional[bool] = typer.Option(False, "--learning", "-l", help="Revise words in your learning list"),
    mastered: Optional[bool] = typer.Option(False, "--mastered", "-m", help="Revise words in your mastered list"),
    favorite: Optional[bool] = typer.Option(False, "--favorite", "-f", help="Revise words in your favorite list"),
    collection: Optional[str] = typer.Option(None, "--collection", "-c", help="Revise words in a particular collection")
):  # sourcery skip: remove-redundant-if
    """
    Revise words from your learning list.

    Args:
        number (Optional[int], optional): Number of words to revise. Defaults to 10.
        tag (Optional[str], optional): Tag of words to revise. Defaults to None.
    """

    if not any([learning, mastered, favorite, collection, tag]) and not number:
        revise_all()
        
    elif number and not any([learning, mastered, favorite, collection, tag]):
        revise_all(number=number)

    elif tag and not number:
        revise_tag(tag=tag)
    elif tag and number:
        revise_tag(number=number, tag=tag)

    elif learning and not number:
        revise_learning(learning=True)
    elif learning and number:
        revise_learning(number=number, learning=True)

    elif mastered and not number:
        revise_mastered(mastered=True)
    elif mastered and number:
        revise_mastered(number=number, mastered=True)
    
    elif favorite and not number:
        revise_favorite(favorite=True)
    elif favorite and number:
        revise_favorite(number=number, favorite=True)
    

# todo - need to write the function
@app.command(rich_help_panel="study", help="❓ Take a quiz on words in your learning list")
def quiz(
    number: Optional[int] = typer.Option(None, "--number", "-n", help="Number of words to quiz on. If not specified, all words will be included in the quiz in alphabetical order.", min=4),
    tag: Optional[str] = typer.Option(None, "--tag", "-t", help="Tag of words to quiz on."),
    learning: Optional[bool] = typer.Option(False, "--learning", "-l", help="Take a quiz on words in your learning list"),
    mastered: Optional[bool] = typer.Option(False, "--mastered", "-m", help="Take a quiz on words in your mastered list"),
    favorite: Optional[bool] = typer.Option(False, "--favorite", "-f", help="Take a quiz on words in your favorite list"),
    collection: Optional[str] = typer.Option(None, "--collection", "-c", help="Take a quiz on words in a particular collection")
):  # sourcery skip: remove-redundant-if
    """
    Take a quiz on words in your learning list.

    Args:
        number (Optional[int], optional): Number of words to quiz on. Defaults to 10.
        tag (Optional[str], optional): Tag of words to quiz on. Defaults to None.
    """
    if not any([learning, mastered, favorite, collection, tag]) and not number:
        quiz_all()
        
    elif number and not any([learning, mastered, favorite, collection, tag]):
        quiz_all(number=number)

    elif tag and not number:
        quiz_tag(tag=tag)
    elif tag and number:
        quiz_tag(number=number, tag=tag)

    elif learning and not number:
        quiz_learning(learning=True)
    elif learning and number:
        quiz_learning(number=number, learning=True)

    elif mastered and not number:
        quiz_mastered(mastered=True)
    elif mastered and number:
        quiz_mastered(number=number, mastered=True)
    
    elif favorite and not number:
        quiz_favorite(favorite=True)
    elif favorite and number:
        quiz_favorite(number=number, favorite=True)
    
    # todo - need to write the function
    elif collection and not number:
        quiz_collection(collection=collection)
    elif collection and number: 
        quiz_collection(number=number, collection=collection)
        
    else:
        print(Panel.fit(title="[b reverse red]  Error!  [/b reverse red]", 
                title_align="center",
                padding=(1, 1),
                renderable="Cannot combine these arguments")
        ) 

@app.command(rich_help_panel="report", help="📚 Generate Graphical Charts based on your vocabulary")
def graph(
    topWordsBar: Optional[int] = typer.Option(None, "--topwordsbar", "-twb", help="Bar Graph of Top N Most Looked Up Words", max=25, min=1),
    topTagsBar: Optional[int] = typer.Option(None, "--toptagsbar", "-ttb", help="Bar Graph of Top N Tags with the most words.", max=25, min=1),
    
    topWordsPie: Optional[int] = typer.Option(None, "--topwordspie", "-twp", help="Pie Chart of Top N Most Looked Up Words", max=25, min=1),
    topTagsPie: Optional[int] = typer.Option(None, "--toptagspie", "-ttp", help="Pie Chart of Top N Tags with the most words.", max=25, min=1),
    
    lookupWeek: Optional[bool] = typer.Option(False, "--lookupweek", "-lw", help="Bar Graph of the word count distribution for days in the past week."),
    lookupMonth: Optional[bool] = typer.Option(False, "--lookupmonth", "-lm", help="Bar Graph of the word count distribution for days in the past month."),
    lookupYear: Optional[bool] = typer.Option(False, "--lookupyear", "-ly", help="Bar Graph of the word count distribution for days in the past year."),
    
    learnVSmaster: Optional[bool] = typer.Option(False, "--learnvsmaster", "-lvm", help="Stacked Graph the number of words in your learning list vs. your mastered list."),
    slider: Optional[bool] = typer.Option(False, "--slider", "-s", help="Shows all graphs one by one in a slider.")
):
    """
    Generate Graphical Charts based on your vocabulary.

    Args:
        tag (Optional[int], optional): Visualizes the top N tags with the most words. Defaults to None.
    """
    
    if slider:
        # importing this here will automatically open the slider window. DO NOT TOUCH.
        import modules.Carousel
    if topWordsBar:
        viz_top_words_bar(N=topWordsBar, popup=True)
    if topTagsBar:
        viz_top_tags_bar(N=topTagsBar,popup=True)
    
    if topWordsPie:
        viz_top_words_pie(N=topWordsPie, popup=True)
    if topTagsPie:
        viz_top_tags_pie(N=topTagsPie, popup=True)
    
    if lookupWeek:
        viz_word_distribution_week(popup=True)
    if lookupMonth:
        viz_word_distribution_month(popup=True)
    if lookupYear:
        viz_word_distribution_year(popup=True)
    
    if learnVSmaster:
        viz_learning_vs_mastered(popup=True)

# todo - need to write the function
@app.command(rich_help_panel="study", help="📇 Create flashcards for words in your learning list")
def flashcard():
    """
    Create flashcards for words in your learning list.
    """
    pass


# todo - command for homophones

if __name__ == "__main__":
    app()

    

# todo: SPACY: paraphrase

# todo: SPACY: sentiment analysis

# todo: SPACY: check paraphrase
