#
# cmake file
#

CMAKE_MINIMUM_REQUIRED(VERSION 2.8.11)

set (PROJ_NAME nodes)

PROJECT(${PROJ_NAME})

if(CMAKE_COMPILER_IS_GNUCC OR CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES Clang)
  add_compile_options(-std=c++1y)
endif()

set (INCLUDE include/AccumulatorNode.h
             include/BinaryOperationNode.h
             include/BinaryPredicateNode.h
             include/ConstantNode.h
             include/DelayNode.h
             include/DotProductNode.h
             include/ExtremalValueNode.h
             include/MultiplexerNode.h
             include/ForestNode.h
             include/LinearPredictorNode.h
             include/L2NormNode.h
             include/MovingAverageNode.h
             include/MovingVarianceNode.h
             include/DemultiplexerNode.h
             include/SingleElementThresholdNode.h
             include/SumNode.h
             include/TypeCastNode.h
             include/UnaryOperationNode.h
             include/ValueSelectorNode.h)

set (SRC src/ConstantNode.cpp
         src/LinearPredictorNode.cpp
         src/SingleElementThresholdNode.cpp)

set (TCC tcc/AccumulatorNode.tcc
         tcc/BinaryOperationNode.tcc
         tcc/BinaryPredicateNode.tcc
         tcc/ConstantNode.tcc
         tcc/DelayNode.tcc
         tcc/DotProductNode.tcc
         tcc/ExtremalValueNode.tcc
         tcc/MultiplexerNode.tcc
         tcc/ForestNode.tcc
         tcc/L2NormNode.tcc
         tcc/MovingAverageNode.tcc
         tcc/MovingVarianceNode.tcc
         tcc/DemultiplexerNode.tcc
         tcc/SumNode.tcc
         tcc/TypeCastNode.tcc
         tcc/UnaryOperationNode.tcc
         tcc/ValueSelectorNode.tcc)

source_group("include" FILES ${INCLUDE})
source_group("src" FILES ${SRC})
source_group("tcc" FILES ${TCC})

add_library(${PROJ_NAME} ${SRC} ${INCLUDE} ${TCC})
target_include_directories(${PROJ_NAME} PUBLIC include)
if(CMAKE_COMPILER_IS_GNUCXX)
  target_compile_options(${PROJ_NAME} PRIVATE -fPIC)
endif()
target_link_libraries(${PROJ_NAME} model predictors utilities)

set_property(TARGET ${PROJ_NAME} PROPERTY FOLDER "libraries")

#
# test project
#

set (TEST_NAME ${PROJ_NAME}_test)

PROJECT(${TEST_NAME})

set (TEST_SRC test/src/main.cpp 
              test/src/Nodes_test.cpp)
set (TEST_INCLUDE test/include/Nodes_test.h)

source_group("src" FILES ${TEST_SRC})
source_group("include" FILES ${TEST_INCLUDE})

add_executable(${TEST_NAME} ${TEST_SRC} ${TEST_INCLUDE} ${INCLUDE})
target_include_directories(${TEST_NAME} PRIVATE test/include)
target_link_libraries(${TEST_NAME} testing linear model nodes predictors utilities common)

set_property(TARGET ${TEST_NAME} PROPERTY FOLDER "tests")

add_test(NAME ${TEST_NAME} COMMAND ${TEST_NAME})