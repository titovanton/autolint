# Yet another way to run Python linters
I have a specific setup on my local machine and prefer to run `flake8` & `mypy` in a terminal window on my second display. This package serves to run a list of linters each time a file with a specified extension is changed.

## Current Versions

- 0.0.2, Pre-Release
- 0.0.1, Pre-Release

see more details in `CHANGELOG.md`

## Compatibility

- Python 3.10+

#### Linters
This package does not include any linters as dependencies, allowing you to customize the configuration locally and run your preferred set of tools. You need to specify the linters you want to use in your `poetry` or `pip` dependencies. Additionally, you must provide a command string for each linter in the local configuration file. I've tested it with the following:

- MyPy 1.8+

## Configuration
This app is configurable and comes with a default `config.yaml` located in the source code folder. If you create a config file in your home directory, it will override the default settings using the same logic as updating one dictionary with another. In turn, if you create a `lintify.yaml` file next to `pyproject.toml`, this file will override all previous settings in the same way as the file in the home directory.


#### Default Config
By default, the configuration includes no linters. You can override this in your local configuration to add them. You can adjust any linter parameters, but be sure to include the `{path}` format parameter, which works the same way as Python's `.format()` function. The default `config.yaml` contains two commented lines with examples of how the linter command should be formatted.

    # raw | frame
    theme: 'frame'

    # may be overridden by --watch-dir cli option
    watch_dir: './'

    files:
      - '*.py'

    linters:
      # - 'autoflake --remove-all-unused-imports --in-place {path}'
      # - ['flake8 {path}', 'mypy {path}']

This configuration defines a sequence of linter commands to be executed on a given codebase.

- Each command listed as a single string is executed sequentially, one after another, ensuring that each linter runs only after the previous one completes.
- When a command is specified as a list of strings, the commands in that list are executed concurrently, meaning they run in "parallel", independent of one another.

This setup allows for a flexible and efficient linting process, ensuring both ordered execution when needed and faster processing through concurrency where applicable.


#### Local Config
There are two types of local configuration files: one in your home directory and another in your project root folder (next to `pyproject.toml`).

The path to your config file from home directory must be:

    Path.home() / '.config/lintify/config.yaml'

On a Linux system, it would look like this:

    /home/<username>/.config/lintify/config.yaml

The project folder configuration file should be placed next to `pyproject.toml` and should be named:

    .lintify.yaml

Note that the name starts with a dot in this case.

#### Example
You need to specify at least one linter. Here are two that I'm using:

    # .lintify.yaml

    linters:
      - 'isort {path}'
      - ['flake8 {path}', 'mypy {path}']

#### Priority
Below is a list sorted in descending order of priority:

- The project folder configuration file
- The home folder configuration file
- The default configuration from the package folder

The logic is that the highest priority configuration file overrides the lower ones. You can specify either one or both of the configuration files in the home and project folders, but note that the default configuration has no linters specified.

## CLI

    Usage: lintify [OPTIONS] COMMAND [ARGS]...

    Options:
      --watch-dir DIRECTORY  Directory to watch for changes. Overrides
                             Config.watch_dir if provided.
      --help                 Show this message and exit.

## MyPy Configuration
If you use MyPy in a Django project, you need to configure the appropriate plugins and specify the project path. Otherwise, MyPy will raise various errors.

#### Poetry and MyPy
Below is an example of the `pyproject.toml` section for this configuration:

    # pyproject.toml

    [tool.mypy]
    mypy_path = "./src"
    plugins = [
      "mypy_django_plugin.main",
      "mypy_drf_plugin.main"
    ]

    [tool.django-stubs]
    django_settings_module = "myproject.settings"

    [tool.flake8]
    max-line-length = 80
    import-order-style = "pep8"

In this example, we have a Django/DRF project named `myproject` located in the `./src` folder (with `manage.py` as the entry point in that folder).

#### mypy.ini
For those who do not use Poetry, below is an example of the same configuration, but in a `mypy.ini` file:

    # mypy.ini

    [mypy]
    mypy_path = ./src
    plugins =
        mypy_django_plugin.main,
        mypy_drf_plugin.main

    [mypy.plugins.django-stubs]
    django_settings_module = main.settings

