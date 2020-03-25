# JYL toolbox

Flask website + postgresql app for JYL (Japanatown Youth Leaders)

## Setup

Clone the repository and enter it

```
git clone https://github.com/RafaelCenzano/jyl-site.git
cd jyl-site
```

### Requirements

Use pip to install needed libraries

```
make
```

or

```
pip install -r requirements.txt
```

### Run 

```
make run
```

or

```
gunicorn run:app
```

### Test run

```
make test
```

or

```
python runtest.py
```

## Authors

* [**Rafael Cenzano**](https://github.com/RafaelCenzano)

## License

This project is licensed under the GNU Public License - see the [LICENSE](LICENSE) file for details
