import oscar.oscar as oscar

if __name__ == '__main__':
    # This is an example of how to retrieve files from a given project
    p = oscar.Project('MisterKeefe_dom-particles')
    for mode, filename, sha in p.head.tree.traverse():
        print(mode, filename, sha)
        if mode != '40000':
            print(oscar.Blob(sha).data)