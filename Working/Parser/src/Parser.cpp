#include <iostream>
#include <string>
#include <cstring>
#include <tree_sitter/api.h>

TSLanguage *tree_sitter_javascript();
TSLanguage *tree_sitter_python();
TSLanguage *tree_sitter_java();

inline bool ends_with(std::string const &value, std::string const &ending)
{
    if (ending.size() > value.size())
        return false;
    return std::equal(ending.rbegin(), ending.rend(), value.rbegin());
}

inline char *read_file(const char *path)
{
    FILE *f = fopen(path, "rb");
    fseek(f, 0, SEEK_END);
    long fsize = ftell(f);
    fseek(f, 0, SEEK_SET);

    char *string = (char *)malloc(fsize + 1);
    int bytes_read = fread(string, fsize, 1, f);
    fclose(f);
    if (bytes_read < fsize)
    {
        printf("WARNING: Read %d bytes from %s but its size is %ld\n", bytes_read, path, fsize);
    }
    return string;
}

int main(int argc, char **argv)
{
    if (argc < 2)
    {
        printf("Usage: Parser path_to_src_file\n");
        return -1;
    }

    TSParser *parser = ts_parser_new();

    // Set up the appropriate programming language
    std::string path = argv[1];
    if (ends_with(path, ".js"))
    {
        ts_parser_set_language(parser, tree_sitter_javascript());
    }
    else if (ends_with(path, ".java"))
    {
        ts_parser_set_language(parser, tree_sitter_java());
    }
    else if (ends_with(path, ".py"))
    {
        ts_parser_set_language(parser, tree_sitter_python());
    }
    else
    {
        printf("ERROR: Unsupported file %s\n", path.c_str());
        return -1;
    }

    char *buf = read_file(path.c_str());

    // Get syntax tree (assume utf8 encoding)
    TSTree *tree = ts_parser_parse_string_encoding(
        parser,
        nullptr,
        buf,
        strlen(buf),
        TSInputEncodingUTF8);

    // Start calculating metrics
    int num_func = 0;
    int num_func_with_doc = 0;
    int num_doc_comment = 0;
    int num_impl_comment = 0;
    int num_header_comment = 0;
    TSNode root_node = ts_tree_root_node(tree);
    char *string = ts_node_string(root_node);
    printf("Syntax tree: %s\n", string);

    // Print results
    printf("Number of functions: %d\n", num_func);
    printf("Number of functions with documents: %d\n", num_func_with_doc);
    printf("Number of documentation comments: %d\n", num_doc_comment);
    printf("Number of implementation comments: %d\n", num_impl_comment);
    printf("Number of header comments: %d\n", num_header_comment);

    // Release related resources
    ts_tree_delete(tree);
    ts_parser_delete(parser);
    delete[] buf;
    delete[] string;
}