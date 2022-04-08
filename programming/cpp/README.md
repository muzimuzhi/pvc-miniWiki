---
title: C/C++
---

# 参考文档

- [cppreference.com](https://en.cppreference.com/w/cpp)
- [Microsoft C/C++ Documentation](https://docs.microsoft.com/en-us/cpp/cpp/?view=msvc-170)

# 语法基础

## 数据类型

## 表达式

## 语句

## [函数](./function.md)

## [异常](./exception.md)

## [预定义宏](./macro.md)

# 标准库

## 文件读写

## 容器

- 顺序容器
- 关联容器
- 迭代器

## [算法](./algorithm.md)

## [动态内存管理](./memory/README.md)

- [原始指针](./memory/raw_pointers.md)
- [智能指针](./memory/smart_pointers.md)
- [内存检查](./memory/check.md)

## [多线程并发](./concurrency.md)

# 抽象机制

## [`class`](https://en.cppreference.com/w/cpp/language/classes)

- [创建类型](./class/class.md)
- [运算符重载](./class/operator.md)
- [拷贝控制](./class/copy_control.md)
- [继承与多态](./class/inheritance.md)

## [`template`](https://en.cppreference.com/w/cpp/language/templates)

- [泛型编程](./template/generic.md)
- [类型推断](./template/type_deduction.md)
- [元编程](./template/metaprogramming.md)

# 开发工具

## 代码规范
- [Google C++ Style Guide](https://google.github.io/styleguide/cppguide.html)（非官方中文版：[Google C++ 风格指南](https://zh-google-styleguide.readthedocs.io/en/latest/google-cpp-styleguide/contents/)）

## [批量构建](./make/README.md)

- GNU Make
- CMake

## [单元测试](./unittest/README.md)

- Google Test
- CTest

## [性能检测](./profile.md)

- Google `gperftools`
- GNU `gprof`

## [断点调试](./debug.md)

- GDB
- LLDB

## [内存检查](./memory/check.md)

- Valgrind
