import click
import os
from unp import select_unpacker, list_unpackers, get_unpacker_class


@click.command()
@click.argument("files", nargs=-1, type=click.Path(), required=True)
@click.option(
    "-q", "--silent", is_flag=True, help="If this is enabled, nothing will be printed."
)
@click.option(
    "-o",
    "--output",
    type=click.Path(),
    help="Defines the output folder.  " "Defaults to the working directory.",
)
@click.option(
    "--unpacker",
    "forced_unpacker",
    callback=select_unpacker,
    metavar="UNPACKER",
    help="Overrides the automatically detected unpacker.  For "
    'a list of available unpackers see "--list-unpackers".',
)
@click.option(
    "--list-unpackers",
    is_flag=True,
    expose_value=False,
    callback=list_unpackers,
    help="Lists all supported and available unpackers.",
)
@click.option(
    "--dump-command",
    is_flag=True,
    help="Instead of executing the unpacker it prints out the "
    "command that would be executed.  This is useful for "
    "debugging broken archives usually.  Note that this command "
    "when executed directly might spam your current working "
    "directory!",
)
@click.version_option()
def cli(files, silent, output, dump_command, forced_unpacker):
    """unp is a super simple command line application that can unpack a lot
    of different archives.  No matter if you unpack a zip or tarball, the
    syntax for doing it is the same.  Unp will also automatically ensure
    that the unpacking goes into a single folder in case the archive does not
    contain a wrapper directory.  This guarantees that you never accidentally
    spam files into your current working directory.

    Behind the scenes unp will shell out to the most appropriate application
    based on filename or guessed mimetype.
    """
    if output is None:
        output = "."

    unpackers = []

    for filename in files:
        filename = os.path.realpath(filename)
        if not os.path.isfile(filename):
            raise click.UsageError(
                'Could not find file "%s".' % click.format_filename(filename)
            )
        if forced_unpacker is not None:
            unpacker_cls = forced_unpacker
        else:
            unpacker_cls = get_unpacker_class(filename)
        unpackers.append(unpacker_cls(filename, silent=silent))

    for unpacker in unpackers:
        if dump_command:
            unpacker.dump_command(output)
        else:
            unpacker.unpack(output)


if __name__ == "__main__":
    cli()
