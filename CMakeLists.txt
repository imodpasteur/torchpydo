cmake_minimum_required(VERSION 2.8.12)

set(CMAKE_BUILD_TYPE_INIT "Release")
set(EXECUTABLE_OUTPUT_PATH ${CMAKE_BINARY_DIR}/bin)
set(LIBRARY_OUTPUT_PATH ${EXECUTABLE_OUTPUT_PATH})

project(Torchpydo)

find_package(Lua 5.2 REQUIRED)
find_package(PythonLibs REQUIRED)

include_directories(${LUA_INCLUDE_DIR})
include_directories(${PYTHON_INCLUDE_DIR})

add_subdirectory(src)

add_library(python MODULE $<TARGET_OBJECTS:src>)
set_target_properties(python PROPERTIES 
                             PREFIX "")

add_library(torchpydo MODULE $<TARGET_OBJECTS:src>)
if (${CMAKE_SYSTEM_NAME} MATCHES "Windows")
  set_target_properties(torchpydo PROPERTIES 
                            PREFIX ""
                            SUFFIX ".pyd")
else ()
  set_target_properties(torchpydo PROPERTIES 
                            PREFIX "")
endif ()

target_link_libraries(torchpydo ${LUA_LIBRARIES} ${PYTHON_LIBRARIES})
target_link_libraries(python ${LUA_LIBRARIES} ${PYTHON_LIBRARIES})
