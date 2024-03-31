# simple-passwd

A simple password database.

## hello
```bash
$ python -m passwd hello --count 4 --name foo
Hello, foo!
Hello, foo!
Hello, foo!
Hello, foo!
```

## encrypt the db
```bash
$ python -m passwd encrypt --password=Soopersecret --input=data/paswddb.csv
```

## decrypt the db
```bash
$ python -m passwd decrypt --password=Soopersecret --input=data/paswddb.csv.enc
```