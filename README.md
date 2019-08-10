# Installing
1. have python 3
2. pip install -r requirements.txt

# How to use

to print remnants prtbs and namespaces:
`python clean.py clustername accesskey secretkey rancherurl`

to delete remnants prtbs use -d:
`python clean.py clustername accesskey secretkey rancherurl`

to delete remnants namespaces use -dn:
`python clean.py clustername accesskey secretkey rancherurl -dn`


use option -c clustername to only do for a certain cluster:
`python clean.py clustername accesskey secretkey rancherurl -c c-asdf2`
