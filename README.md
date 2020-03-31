# tiny-markdown-flow

Generate the flow by markdown automatically. 

# Flow

![image](https://github.com/wenbinhuang9/tiny-markdown-flow/blob/master/new_nfa_draw.jpg)

# How to use

```
from engine import  interpret

interpret("type LR lexer > parser > layout > draw")
```

# Graphs supported

1. Linear left to right box graph

markdown as follows
```
type LR this > is > left > to > right > graph
```
flow generated by the above markdown
![image](https://github.com/wenbinhuang9/tiny-markdown-flow/blob/master/lr.jpg)

2. Linear top to down box graph

markdown as follows

```
type TD this > is > top > to > down > graph
```

flow generated by the above markdown
![image](https://github.com/wenbinhuang9/tiny-markdown-flow/blob/master/td.jpg)

markdown as follows 



# Graphs to support
1. frame graph
2. sequence graph 

