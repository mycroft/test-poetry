# poetry-demo

That's just a small project to check my setup with nix, running a small flask demo with prometheus client lib. Nothing fancy.

## Run

I'm using `nix-shell`:

```sh
$ cd test-poetry/
$ nix-shell
[nix-shell:~/dev/test-poetry]$ poetry install
... this will install python deps ...

[nix-shell:~/dev/test-poetry]$ poetry run pytest
... this will run tests ...

[nix-shell:~/dev/test-poetry]$ export FLASK_DEBUG=1
[nix-shell:~/dev/test-poetry]$ poetry run python 
poetry run python ./poetry-demo/main.py
 * Serving Flask app 'main'
 * Debug mode: on
...

```