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

class A(object):
    pass

class B(object):
    pass

gc.disable()

a = A()
b = B()
del a
del b()

print 'Object count of A:', objgraph.count('A')
print 'Object count of B:', objgraph.count('B')
```

上面程序的执行结果为:

```Bash
Object count of A: 0
Object count of B: 0
```

可以看到, 我们创建了一个类`A`的对象, 并用变量`a`引用起来, 然后用`del a`删除这个引用.
`objgraph.count('A')`返回0, 意味着内存中'A'的对象数量没有增长.

引用计数的一个主要缺点是无法自动处理循环引用. 将上面的代码稍做修改:

```Python
import gc
import objgraph

class A(object):
    pass

class B(object):
    pass

gc.disable()

a = A()
b = B()
a.child = b
b.parent = a
del a
del b

print 'Object count of A:', objgraph.count('A')
print 'Object count of B:', objgraph.count('B')
print 'Unreachable object count:', gc.collect()
```

在上面的代码的执行结果为:

```Bash
Object count of A: 1
Object count of B: 1
Unreachable object count: 2
```

我们创建了类A和类B的两个对象, 并分别用变量a和变量b引用他们. 然后我们利用`child`和`parent`属性将两个对象相互引用
起来. 这就形成了一个循环引用. 当我们执行`del a`和`del b`的时候，表面上我们不再引用两个对象, 但由于两个对象相互
引用着对方, 因此引用计数不为0, 则不会被自动回收. 更糟糕的是由于现在没有任何变量引用他们, 我们无法再找到这两个变量
并清除. Python使用垃圾回收机制来处理这样的情况. 执行`gc.collect()`, Python垃圾回收器回收了两个相互引用的对象, 并
返回2.

# TODO: 垃圾回收机制.
# TODO: 调优手段: 1. 手动GC; 2. 调高阈值; 3. 手动解引用.
