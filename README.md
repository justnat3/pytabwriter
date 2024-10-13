# pytabwriter
a kind of tabwriter impl. very reduced

## Usage
```py
wr = TabWriter("")
wr.writeln("Name\tAge\tDescription")
wr.writeln("nate\t24\tsome type of programmer laksjdlfkj")
wr.writeln("bob\t25\tHR Representative")
wr.flush()
```

Returns
```
|  Name  |  Age |  Description                        |  
|  nate  |  24  |  some type of programmer laksjdlfkj |  
|  bob   |  25  |  HR Representative                  |
```
