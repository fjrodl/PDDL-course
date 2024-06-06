# Plansys2

Plansys2 is a framework for developing and executing robot task planning systems. It's designed to be modular, flexible, and scalable, making it suitable for a wide range of robotic applications. Plansys2 is built on top of the Robot Operating System (ROS) 2, which provides a set of tools and libraries for building robot applications.

Plansys2 offers several key features:

1. **Task Planning**: Plansys2 provides tools for task planning, allowing robots to generate plans to achieve complex goals autonomously. It supports various planning domains, including classical planning, temporal planning, and hybrid planning.

2. **ROS Integration**: Being built on ROS 2, Plansys2 seamlessly integrates with the ROS ecosystem. This integration enables communication with robot hardware, perception systems, and other software components using ROS messages and services.

3. **Modularity**: Plansys2 is designed with a modular architecture, allowing developers to easily extend and customize its functionality. Users can plug in different planning algorithms, domain models, and execution engines to tailor the system to their specific requirements.

4. **Scalability**: Plansys2 is designed to be scalable, allowing it to handle large-scale planning problems and complex robotic systems efficiently. It supports distributed planning architectures, enabling collaboration between multiple robots and planning nodes.

5. **Community Support**: Plansys2 benefits from an active community of developers and users who contribute to its development, provide support, and share resources such as tutorials, examples, and documentation.



## Execution

Source: https://github.com/PlanSys2/ros2_planning_system_examples.git

https://plansys2.github.io/tutorials/docs/simple_example.html

### 

## Exercise

Create the Doxygen file an take a look to 


### An example for creating documentation

The `Doxyfile` in this repository was generated using `doxygen -g`, and then
edited in the following way:

```
Line 35:
PROJECT_NAME           = "Example of Doxygen Documentation Procedure"
Line 47:
PROJECT_BRIEF          = "This is just a test of Doxygen"
Line 54:
PROJECT_LOGO           = "./DiConIcon.ico"
Line 61:
OUTPUT_DIRECTORY       = "generated-docs"
Line 438:
EXTRACT_ALL            = YES
Line 363:
DISTRIBUTE_GROUP_DOC   = YES
Line 444:
EXTRACT_PRIVATE        = YES
Line 450:
EXTRACT_PACKAGE        = YES
Line 456:
EXTRACT_STATIC         = YES
Line 481:
EXTRACT_ANON_NSPACES   = YES
Line 759:
WARN_NO_PARAMDOC       = YES
Line 867:
RECURSIVE              = YES
Line 876:
EXCLUDE                = README.md
Line 998:
SOURCE_BROWSER         = YES
Line 1004:
INLINE_SOURCES         = YES
Line 1017:
REFERENCED_BY_RELATION = YES
Line 1023:
REFERENCES_RELATION    = YES
Line 1031:
REFERENCES_LINK_SOURCE = NO
Line 2334:
CALL_GRAPH             = YES
Line 2346:
CALLER_GRAPH           = YES
```
