project(Google_tests)

add_subdirectory(googletest-1.15.2)
include_directories(${gtest_SOURCE_DIR}/include ${gtest_SOURCE_DIR})

add_executable(gtest.run ../Task_1/Task_1.cpp)
target_link_libraries(gtest.run gtest gtest_main)