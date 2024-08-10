# Yet another way to run Python linters
I have a specific setup on my local machine and prefer to run flake8 & mypy in a terminal window on my second display. This package serves to run a list of linters each time a file with a specified extension is changed.

### Config
This app is configurable and comes with a default `config.yaml` located in the source code folder. If you create a config file in your home directory, it will override the default settings using the same logic as updating one dictionary with another. The path to your custom config file is:

    Path.home() / '.config/auto_lint/config.yaml'

On a Linux system, it would look like this:

    /home/<username>/.config/auto_lint/config.yaml

### CLI
Currently available command:

    poetry run autolint <dir_to_watch>
