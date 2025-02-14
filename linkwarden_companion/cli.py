import click

from collections.abc import Callable
from linkwarden_companion import logger
from linkwarden_companion.messages import *
from linkwarden_companion.models import NewLink
from linkwarden_companion.utils import command_tree
from linkwarden_companion.linkwarden import Linkwarden
from linkwarden_companion.config import LINKWARDEN_COMPANION_CONFIG


def require_linkwarden(function: Callable):
    def wrapper(*args, **kwargs):
        linkwarden = Linkwarden.get_instance()
        kwargs['linkwarden'] = linkwarden
        return function(*args, **kwargs)

    return wrapper


# noinspection StrFormat
@click.group()
def cli():
    """
    Linkwarden companion CLI
    :return:
    """
    required_keys = ['ACCESS_TOKEN', 'HOST', 'USER']
    for key in required_keys:
        if key not in LINKWARDEN_COMPANION_CONFIG['AUTH']:
            echo(MISSING_KEY.format(key=key), 'error')


def echo(message: str, level: str = 'debug'):
    function_to_call = getattr(logger, level)
    function_to_call(message)
    click.echo(message)
    if level in ['error', 'critical']:
        raise click.Abort()


@cli.group()
def auth():
    """
    Set of commands for authenticating with the Linkwarden API,
    and managing the authentication token.
    :return:
    """
    pass


@auth.command(name="set-token")
@click.argument('token')
def set_access_token(token: str):
    """
    Set the Linkwarden API token.
    :return:
    """
    LINKWARDEN_COMPANION_CONFIG['AUTH']['ACCESS_TOKEN'] = token
    LINKWARDEN_COMPANION_CONFIG.save()


@auth.command(name="set-user")
@click.argument('user')
def set_user(user: str):
    """
    Set the Linkwarden API user.
    :return:
    """
    LINKWARDEN_COMPANION_CONFIG['AUTH']['USER'] = user
    LINKWARDEN_COMPANION_CONFIG.save()


@auth.command(name="set-host")
@click.argument('host')
def set_host(host: str):
    """
    Set the Linkwarden API host.
    :return:
    """
    LINKWARDEN_COMPANION_CONFIG['AUTH']['HOST'] = host
    LINKWARDEN_COMPANION_CONFIG.save()


@cli.group()
def links_group():
    pass


# noinspection StrFormat
@links_group.command(name="list-links")
@click.option('-v', '--verbose', help="Verbosity level", default=0, count=True)
@require_linkwarden
def list_links(linkwarden: Linkwarden, verbose: int):
    """
    List all links
    :return:
    """
    echo("Listing all links")
    links = linkwarden.get_links()
    for link in links:
        verbose_level = {
            0: "\tID: {id} Name: {name} URL: {url} Collection: {collectionId} Created By: {createdById}",
            1: "\tID: {id} Name: {name} URL: {url} Collection: {collectionId}"
               " Created By: {createdById} Description: {description}",
        }
        if verbose <= 2:
            echo(verbose_level[verbose].format(**link.model_dump()))
        else:
            echo(link.json())


@links_group.command(name="add-link")
@click.argument('name')
@click.argument('url')
@click.option('-d', '--description', help="Link description", default="")
@click.option('-c', '--collection', help="Collection ID", default=0)
@click.option('-i', '--icon', help="Link icon", default=None)
@click.option('-w', '--icon-weight', help="Link icon weight", default=None)
@click.option('-C', '--color', help="Link color", default=None)
@require_linkwarden
def add_link(linkwarden: Linkwarden, name: str, url: str,
             description: str, collection: int, icon: str,
             icon_weight: str, color: str):
    """
    Add a link
    :return:
    """
    echo("Adding link")
    new_link = NewLink(name=name, url=url, description=description, collectionId=collection, icon=icon,
                       iconWeight=icon_weight, color=color)
    link = linkwarden.create_link(new_link)
    echo(f"Link added with ID: {link.id}")


command_groups = command_tree(cli).keys()
# for each string in command_groups, get the function it points to
command_groups = [globals()[command.replace('-', '_')] for command in command_groups]
main = click.CommandCollection(sources=command_groups)
if __name__ == "__main__":
    main()
