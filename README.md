# env-gap

Compare the variable names in an example dotenv file with a local `.env` file. It reports missing and extra names, and never displays values.

## Use

Requires Python 3.8+; no packages to install.

```sh
python env_gap.py .env.example .env
```

Exit status is `0` when the key sets match, `1` when they differ, and `2` when a file cannot be read or contains an unsupported or duplicate assignment. Both files are read only.

The parser accepts one `NAME=value` assignment per line, optional leading `export`, blank lines, and `#` comments. It does not evaluate shell syntax or expand variables. Only names are used in the comparison; values are never printed.

## License

MIT
