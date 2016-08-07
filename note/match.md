# logscan项目设计思路





匹配规则说明：

以`#`号作为分隔符号，类似数学的计算一样，如：

(!kazoo & rest) | !yum

这与Linux下的模式匹配一样



## Token类

Token类接收一个值和该值的类型，在此类实例对象中初始化了一个值和相应的类型。

## ASTree类

此类接收一个token值，实例化为一个没有左右节点的树，树根为token值。这里的token值是类tokenize类把表达式处理后的数据，即tokenize类返回列表中的元素。

### tokenize.tokenize方法

此类把原始的匹配规则解析成一个列表，返回值为一个列表

### tokenize.make_sub_ast方法

此方法是为了配合make_ast类工作，当

### tokenize.make_ast方法

把tokenize类解析后的数据构造成一个颗语法树，返回这颗语法树

### tokenize.cacl方法

此方法计算语法树的bool值，采用递归方式实现

## Matcher类

此类接收一个原始的匹配规则，实例化时构建成抽象语法树，并提供`match`方法对一行数据进行匹配，并返回bool值。









