---
layout: post
comments: true
title: Python内存管理机制及优化简析
---

# 准备工作

为了方便解释Python的内存管理机制, 本文使用了`gc`模块来辅助展示内存中的Python对象以及Python垃圾回收器的工作情况.
本文中具体使用到的接口包括:

```Python
gc.disable()  # 暂停自动垃圾回收.
gc.collect()  # 执行一次完整的垃圾回收, 返回垃圾回收所找到无法到达的对象的数量.
```

完整的`gc`模块文档可以参看[这里](https://docs.python.org/2/library/gc.html).

同时我们还使用了`objgraph`Python库, 本文中具体使用到的接口包括:

```Python
objgraph.count(typename)  # 对于给定类型typename, 返回Python垃圾回收器正在跟踪的对象个数.
```

`objgraph`可以通过命令`pip install objgraph`安装. 完整的文档可以参看[这里](https://mg.pov.lt/objgraph/index.html).

# Python内存管理机制

Python有两种共存的内存管理机制: *引用计数*和*垃圾回收*. 引用计数是一种非常高效的内存管理手段, 当一个Python对象被引
用时其引用计数增加1, 当其不再被一个变量引用时则计数减1. 当引用计数等于0时对象被删除.

```Python
import gc

import objgraph

gc.disable()


class A(object):
	pass

class B(object):
	pass

def test1():
	a = A()
	b = B()

test1()
print objgraph.count('A')
print objgraph.count('B')
```

上面程序的执行结果为:

```Bash
Object count of A: 0
Object count of B: 0
```

在`test1`中, 我们分别创建了类`A`和类`B`的对象, 并用变量`a`, `b`引用起来.
当`test1`调用结束后`objgraph.count('A')`返回0, 意味着内存中`A`的对象数量
没有增长. 同理`B`的对象数量也没有增长. 注意我们通过`gc.disable()`关闭了
Python的垃圾回收, 因此`test1`中生产的对象是在函数调用结束引用计数为0时被自
动删除的.

引用计数的一个主要缺点是无法自动处理循环引用. 继续上面的代码:

```Python
def test2():
    a = A()
    b = B()
    a.child = b
    b.parent = a

test2()
print 'Object count of A:', objgraph.count('A')
print 'Object count of B:', objgraph.count('B')
gc.collect()
print 'Object count of A:', objgraph.count('A')
print 'Object count of B:', objgraph.count('B')
```

在上面的代码的执行结果为:

```Bash
Object count of A: 1
Object count of B: 1
Object count of A: 0
Object count of B: 0
```

`test1`相比`test2`的改变是将`A`和`B`的对象通过`child`和`parent`相互引用
起来. 这就形成了一个循环引用. 当`test2`调用结束后, 表面上我们不再引用两个对象,
但由于两个对象相互引用着对方, 因此引用计数不为0, 则不会被自动回收.
更糟糕的是由于现在没有任何变量引用他们, 我们无法再找到这两个变量并清除.
Python使用垃圾回收机制来处理这样的情况. 执行`gc.collect()`, Python垃圾
回收器回收了两个相互引用的对象, 之后`A`和`B`的对象数又变为0.

# TODO: 垃圾回收机制.
# TODO: 调优手段: 1. 手动GC; 2. 调高阈值; 3. 手动解引用.
