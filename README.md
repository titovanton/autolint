# Yet another way to run Python linters
I have a specific setup on my local machine and prefer to run `flake8` & `mypy` in a terminal window on my second display. This package serves to run a list of linters each time a file with a specified extension is changed.

## Compatibility

- Python 3.10+

#### Linters
This package does not include any linters as dependencies, allowing you to customize the configuration locally and run your preferred set of tools. You need to specify the linters you want to use in your `poetry` or `pip` dependencies. Additionally, you must provide a command string for each linter in the local configuration file. I've tested it with the following:

- MyPy 1.8+

## Configuration
This app is configurable and comes with a default `config.yaml` located in the source code folder. If you create a config file in your home directory, it will override the default settings using the same logic as updating one dictionary with another.

#### Default Config
By default, the configuration includes no linters. You can override this in your local configuration to add them. You can adjust any linter parameters, but be sure to include the `{path}` format parameter, which works the same way as Python's `.format()` function. The default `config.yaml` contains two commented lines with examples of how the linter command should be formatted.

    theme: 'frame'  # raw | frame
    files:
      - '*.py'
    linters:
      # - 'flake8 {path}'
      # - 'mypy {path}'

#### Local Config
The path to your custom config file is:

    Path.home() / '.config/auto_lint/config.yaml'

On a Linux system, it would look like this:

    /home/<username>/.config/auto_lint/config.yaml

#### Example
You need to specify at least one linter. Here are two that I'm using:

    linters:
      - 'flake8 {path}'
      - 'mypy {path}'

## CLI
Currently available commands:

    poetry run autolint <dir_to_watch>
