Documentation in zh_CN
===================

通知
---

* Blade 发布1.1.1，包含以下特性：
 * python 最低版本要求从2.7下降到2.4
 * 修正了python 2.7.0 argparse 模块 bug 带来的问题
 * install 命令支持 zsh
 * 集成cpplint，构建前自动调用cpplint对被更改的代码做代码检查。
 * 新增 cc_config.optimize 选项，可以控制整体默认优化级别。
 * 更新文档

贡献者名单：

* chenjingxu at qiyi dot com
* whuwxl at github dot com
* yeshunping at github dot com
* guanqun at github dot com

概述
---
Blade 是一个现代构建系统，期望的目标是强大而好用，把程序员从构建的繁琐中解放出来。

Blade主要定位于linux下的大型C++项目，密切配合研发流程，比如单元测试，持续集成，覆盖率统计等。但像unix下的文本过滤程序一样，保持相对的独立性，可以单独运行。目前重点支持i386/x86_64 Linux，未来可以考虑支持其他的类Unix系统。

在[腾讯公司“台风”云计算平台](http://wenku.it168.com/d_000434944.shtml)开发过程中，为了解决 GNU Make，Autotools 的难用和繁琐的问题，我们开发了这个全新的构建系统，整个系统基于多个声明式的构建脚本，在构建脚本里，只需要声明要构建什么目标，目标的源代码，以及其直接依赖的其它目标，不需要说明如何构建。大大降低了使用难度，提高了开发效率。

首先，Blade解决了依赖问题。
当你在构建某些目标时，头文件有变化，会自动重新构建。
最方便的是，Blade也能追踪库文件的依赖关系。比如
库 foo 依赖库 common，那么在库 foo 的 BUILD 文件中列入依赖：
```python
cc_library(
    name = 'foo',
    srcs = ...,
    deps = ':common'
)
```
那么对于使用foo的程序，如果没有直接用到common，那么久只需要列出foo，并不需要列出common。
```python
cc_binary(
    name = 'my_app',
    srcs = ...,
    deps = ':foo'
)
```
这样当你的库实现发生变化，增加或者减少库时，并不需要通知库的用户一起改动，Blade自动维护这层间接的依赖关系。当构建my_app时，也会自动检查foo和common是否也需要更新。

说到易用性，除了依赖关系的自动维护，Blade还可以做到，用户只需要敲一行命令，就能把整个目录树的编译链接和单元测试全部搞定。例如：

递归构建和测试common目录下所有的目标
```bash
$ blade test common...
```
以32位模式构建和测试
```bash
$ blade test -m32 common...
```
以调试模式构建和测试
```bash
$ blade test -pdebug common...
```
显然，你可以组合这些标志
```bash
$ blade test -m32 -pdebug common...
```
特点
---
* 自动分析头文件依赖关系，构建受影响的代码。
* 增量编译和链接，只构建因变更受影响而需要重新构建的代码。
* 自动计算库的间接依赖，库的作者只需要写出直接依赖，构建时自动检查所依赖的库是否需要重新构建。
* 在任意代码树的任意子目录下都能构建。
* 支持一次递归构建多个目录下的所有目标，也支持只构建任意的特定的目标。
* 无论构建什么目标，这些目标所依赖的目标也会被自动连坐更新。
* 内置 debug/release 两种构建类型。
* 彩色高亮构建过程中的错误信息。
* 支持 ccache
* 支持 distcc
* 支持基于构建多平台目标
* 支持构建时选择编译器（不同版本的gcc，clang等）
* 支持编译 protobuf，lex, yacc, swig
* 支持自定义规则
* 支持测试，在命令行跑多个测试
* 支持并行测试（多个测试进程并发运行）
* 支持增量测试（无需重新运行的测试程序自动跳过）
* 集成 gperftools，自动检测测试程序的内存泄露
* 构建脚本 vim 语法高亮
* svn 式的子命令命令行接口。
* 支持 bash 命令行补全
* 用 python 编写，无需编译，直接安装使用。

彻底避免以下问题：

* 头文件更新，受影响的模块没有重新构建。
* 被依赖的库需要更新，而构建时没有被更新，比如某子目录依

致谢
---
* Blade 是受 Google 官方博客发表的这篇文章启发而开发的：
[ 云构建：构建系统是如何工作的](http://google-engtools.blogspot.hk/2011/08/build-in-cloud-how-build-system-works.html)
* 现阶段 Blade 生成 [SCons](http://www.scons.org/) 脚本进行构建，因此 Blade 的运行还需要依赖 SCons。
* [Python](http://www.python.org) 是一种简单易用而又强大的语言，我们喜欢python。
* 为了支持python 2.6及更低版本，我们把python 2.7中的argparse.py放入了源码包。
* Google 开放的一些库强大而好用，我们很喜欢，我们把对这些库的支持集成进了Blade中，既方便了库的使用，又增强了 Blade，这些库包括 [glog](http://code.google.com/p/google-glog/), [protobuf](http://code.google.com/p/protobuf/),[gtest](http://code.google.com/p/googletest/), [gproftools](http://code.google.com/p/gperftools/)。

更多文档请参考Blade wiki。

欢迎使用以及帮助我们改进Blade，我们期待你的贡献。

Documentation in en_US
====================
Brief
----
Blade is designed to be a modern building system. It is powerful and easy to use. It supports building multiple languages, such as c/c++, Java, protobuf and swig etc. It analyzes the target dependency automatically and integrates compiling, linking, testing(includes incremental testing and parallel testing) and static code inspection
together. It aims to improve the clarity and simplicity of the building rules for a project.

With Blade, you can compile, link and test multiple targets by just inputting one simple command line.
For example:

Build and test all targets in common directory recursively.
```bash
$ blade test common...
```

Build and test targets as 32 bit
```bash
$ blade test -m32 common...
```
Build and test targets as debug mode
```bash
$ blade test -pdebug common...
```

And you can combine the flags together:
```bash
$ blade test -m32 -pdebug common...
```
Features
-------
* Auto dependency analysis, includes header files and libraries.
* Test integration: built-in support of gtest. Support incremental testing and parallel testing.
* Simple syntax, easy to use.
* Simple command line interface similar to svn.
* Memory leak checking(with gperftools).
* Bash command line completion.
* Colorful diagnostic message displaying.
* Vim integration, includes syntax hi-light, quickfix.

Credit
-----
* Blade is inspired by Google's public information about their building system. Here is a reference article from Google's official blog.
[http://google-engtools.blogspot.hk/2011/08/build-in-cloud-how-build-system-works.html build in cloud: how build system works]
* Blade generates [SCons](http://www.scons.org/) script internally, and it depends on SCons right now.
* [Python](http://www.python.org) is a powerful and easy-to-used language, we like python.
* To support python 2.6, we put argparse.py from python 2.7 into code base.
* Some libraries open sourced by Google, such as
[protobuf](http://code.google.com/p/protobuf/), [gtest](http://code.google.com/p/googletest/), [gproftools](http://code.google.com/p/gperftools/) are handy and powerful, we integrate these libraries into Blade, make them easier to use, and also enhance Blade's ability.

Read our wiki to get more documents. Only Chinese version is ready now, English version is coming soon, sorry for inconvenience.

Welcome to enjoy and help us to improve blade, we are expecting your contribution.