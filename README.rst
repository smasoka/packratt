# packratt

`packratt` is an application and a python package for downloading and caching Radio Astronomy products, primarily to facilitate testing Radio Astronomy software.

## Installing

For the lastest stable release

```bash
$ pip install packratt
```

## Usage

Use an an linux application

```bash
packratt ....
```

Use as a Python software package

```python
import packratt

packratt.get("")
packratt.get("")
packratt.get("") 
```

### Registry schemas

schemas are defined by a yaml registry file 

```yaml

```

Users can define their registry file and place them under `/home/username/.packratt/registry.yaml`


## Contributing

To contribute, please adhere to [pep8](https://www.python.org/dev/peps/pep-0008/) coding standards

## License

[LICENSE](LICENSE)
