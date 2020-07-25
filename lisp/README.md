# How do I run these?

A good old Common LISP REPL!

I use [Steel Bank Common Lisp](http://www.sbcl.org/) for Windows, although it is multiplatform.

1. In terminal, run `sbcl --script my_lisp_file_name.lisp`.
2. You may like `watch sbcl --script my_lisp_file_name.lisp`.

Or,

1. In terminal, run `sbcl`.
2. Evaluate `(load "my_lisp_file_name.lisp")`
3. That's it! You can now run all functions/variables defined in that file.

You can also use an IDE like [LispWorks](lispworks.com) or [Portacle](https://portacle.github.io/) if you like.

The [Atom](https://atom.io) text editor with "Script" plugin works nicely!
