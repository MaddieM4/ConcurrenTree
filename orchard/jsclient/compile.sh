#/usr/bin/sh

coffee -o js/ -c coffee/
cat js/util.js js/bcp.js js/operation.js js/tree.js > js/ctree.js
