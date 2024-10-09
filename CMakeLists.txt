cmake_minimum_required(VERSION 3.29)
project(LR2)

set(CMAKE_CXX_STANDARD 20)

add_subdirectory(Google_tests)
link_libraries(gtest)

# set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -fsanitize=address")

add_executable(Task_1 Task_1/Task_1.cpp)
add_executable(Task_2 Task_2/Task_2.cpp)
add_executable(Task_3 Task_3/Task_3.cpp)
add_executable(Task_4 Task_4/Task_4.cpp)
add_executable(Task_5 Task_5/Task_5.cpp)
add_executable(Task_6 Task_6/Task_6.cpp)
add_executable(Task_7 Task_7/Task_7.cpp)
add_executable(Task_8 Task_8/Task_8.cpp)
add_executable(Task_9 Task_9/Task_9.cpp)
add_executable(Task_10 Task_10/Task_10.cpp)
add_executable(Task_11 Task_11/Task_11.cpp)
add_executable(Task_12 Task_12/Task_12.cpp)
add_executable(Task_13 Task_13/Task_13.cpp)





