cmake_minimum_required(VERSION 3.1)

project(CommentParser)

set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_FLAGS "-O2 -Wall")

# Setting up tree-sitter
include_directories(${CMAKE_SOURCE_DIR}/3rd-Party/tree-sitter/lib/include)
include_directories(${CMAKE_SOURCE_DIR}/3rd-Party/tree-sitter/lib/src)
include_directories(${CMAKE_SOURCE_DIR}/3rd-Party/tree-sitter/lib/utf8proc)
list(APPEND TREE_SITTER_SRC 
    "${CMAKE_SOURCE_DIR}/3rd-Party/tree-sitter/lib/src/lib.c" 
    "${CMAKE_SOURCE_DIR}/3rd-Party/tree-sitter-java/src/parser.c"
    "${CMAKE_SOURCE_DIR}/3rd-Party/tree-sitter-javascript/src/parser.c"
    "${CMAKE_SOURCE_DIR}/3rd-Party/tree-sitter-javascript/src/scanner.c"
    "${CMAKE_SOURCE_DIR}/3rd-Party/tree-sitter-python/src/parser.c"
    "${CMAKE_SOURCE_DIR}/3rd-Party/tree-sitter-python/src/scanner.cc"
)

add_executable(Parser src/Parser.cpp ${TREE_SITTER_SRC})