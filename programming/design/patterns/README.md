---
title: Design Patterns
---

# Creational Patterns

## [Abstract Factory](./abstract_factory/README.md)
> Provide an interface for creating families of related or dependent objects without specifying their concrete classes.

![](./abstract_factory/class.svg)

## [Builder](./builder/README.md)
> Separate the construction of a complex object from its representation so that the same construction process can create different representations.

![](./builder/class.svg)

## [Factory Method](./factory_method/README.md)
> Define an interface for creating an object, but let subclasses decide which class to instantiate.

![](./factory_method/class.svg)

## [Prototype](./prototype/README.md)
> Specify the kinds of objects to create using a prototypical instance, and create new objects by copying this prototype.

![](./prototype/class.svg)

## [Singleton](./singleton/README.md)
> Ensure a class only has one instance, and provide a global point of access to it.

![](./singleton/class.svg)

# Structural Patterns

## [Adapter](./adapter/README.md)
> Convert the interface of a class into another interface clients expect.

![](./adapter/class.svg)

## [Bridge](./bridge/README.md)
> Decouple an abstraction from its implementation so that the two can vary independently.

![](./bridge/class.svg)

## [Composite](./composite/README.md)
> Compose objects into tree structures to represent part-whole hierarchies.
> Composite lets clients treat individual objects and compositions of objects uniformly.

![](./composite/class.svg)

## [Decorator](./decorator/README.md)
> Attach additional responsibilities to an object dynamically.
> Decorators provide a flexible alternative to subclassing for extending functionality.

![](./decorator/class.svg)

## [Facade](./facade/README.md)
> Provide a unified interface to a set of interfaces in a subsystem.
> Facade defines a higher-level interface that makes the subsystem easier to use.

![](./facade/class.svg)

## [Flyweight](./flyweight/README.md)
> Use sharing to support large numbers of fine-grained objects efficiently.

![](./flyweight/class.svg)

## [Proxy](./proxy/README.md)
> Provide a surrogate or placeholder for another object to control access to it.

![](./proxy/class.svg)

# Behavioral Patterns

## [Chain of Responsibility](./chain_of_responsibility/README.md)
> Avoid coupling the sender of a request to its receiver by giving more than one object a chance to handle the request.
> Chain the receiving objects and pass the request along the chain until an object handles it.

![](./chain_of_responsibility/class.svg)

## [Command](./command/README.md)
> Encapsulate a request as an object, thereby letting you parameterize clients with different requests, queue or log requests, and support undoable operations.

![](./command/class.svg)

## [Interpreter](./interpreter/README.md)
> Given a language, define a represention for its grammar along with an interpreter that uses the representation to interpret sentences in the language.

![](./interpreter/class.svg)

## [Iterator](./iterator/README.md)
> Provide a way to access the elements of an aggregate object sequentially without exposing its underlying representation.

![](./iterator/class.svg)

## [Mediator](./mediator/README.md)
> Define an object that encapsulates how a set of objects interact.
> Mediator promotes loose coupling by keeping objects from referring to each other explicitly, and it lets you vary their interaction independently.

![](./mediator/class.svg)

## [Memento](./memento/README.md)
> Without violating encapsulation, capture and externalize an object's internal state so that the object can be restored to this state later.

![](./memento/class.svg)

## [Observer](./observer/README.md)
> Define a one-to-many dependency between objects so that when one object changes state, all its dependents are notified and updated automatically.

![](./observer/class.svg)

## [State](./state/README.md)
> Allow an object to alter its behavior when its internal state changes.
> The object will appear to change its class.

![](./state/class.svg)

## [Strategy](./strategy/README.md)
> Define a family of algorithms, encapsulate each one, and make them interchangeable.
> Strategy lets the algorithm vary independently from clients that use it.

![](./strategy/class.svg)

## [Template Method](./template_method/README.md)
> Define the skeleton of an algorithm in an operation, deferring some steps to subclasses.
> Template Method lets subclasses redefine certain steps of an algorithm without changing the algorithm's structure.

![](./template_method/class.svg)

## [Visitor](./visitor/README.md)
> Represent an operation to be performed on the elements of an object structure.
> Visitor lets you define a new operation without changing the classes of the elements on which it operates.

![](./visitor/class.svg)

# Language Support

## Java

### `implements` an `interface`

```java
public interface Comparable<T> {
  public abstract int compareTo(T that);
}

public class Point implements Comparable<Point> {
  private final double x;
  private final double y;
  
  public Point(double x, double y) {
    this.x = x;
    this.y = y;
  }
  
  @Override
  public int compareTo(Point that) {
    if (this.x < that.x) return -1;
    if (this.x > that.x) return +1;
    if (this.y < that.y) return -1;
    if (this.y > that.y) return +1;
    return 0;
  }
}
```

### `extends` a `class`

所有用 `class` 定义的类都是 [`java.lang.Object`](https://docs.oracle.com/javase/8/docs/api/java/lang/Object.html) 的“子类 (subclass)”或“派生类 (derived classs)”。

```java
public class Object {
  public String toString();
}

public class Point extends Object {
  private final double x;
  private final double y;
  
  public Point(double x, double y) {
    this.x = x;
    this.y = y;
  }
  
  @Override
  public String toString() {
    StringBuilder sb = new StringBuilder();
    sb.append('(');
    sb.append(this.x);
    sb.append(',').append(' ');
    sb.append(this.y);
    sb.append(')');
    return sb.toString();
  }
  
  // extended methods
  // ...
}
```

## C++

### Inheritance

```c++
#include <iostream>
#include <string>

class Object {
 public:
  virtual std::string to_string() = 0;
};

class Point : public Object {
 private:
  const double _x;
  const double _y;
  
 public:
  Point(double x, double y) : _x(x), _y(y) { }
  virtual std::string to_string() override {
    return '(' + std::to_string(_x) + ',' + ' ' + std::to_string(_y) + ')';
  }
};

int main() {
  Point p = Point(1.0, 0.0);
  std::cout << p.to_string() << std::endl;
}
```

### Inheritance + `template`

```cpp
#include <iostream>

template<class T>
class Comparable {
  virtual int compareTo(const T& that) = 0;
};

class Point : public Comparable<Point> {
 private:
  const double _x;
  const double _y;
  
 public:
  Point(double x, double y) : _x(x), _y(y) { }
  virtual int compareTo(const Point& that) override {
    if (_x < that._x) return -1;
    if (_x > that._x) return +1;
    if (_y < that._y) return -1;
    if (_y > that._y) return +1;
    return 0;
  }
};

int main() {
  using P = Point;
  P o = P(0.0, 0.0);
  P p = P(1.0, 0.0);
  std::cout << p.compareTo(o) << std::endl;
}
```
