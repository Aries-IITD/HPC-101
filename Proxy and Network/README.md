## Internet connectivity

Use proxy.sh script to activate a proxy connection on a node. Recommended steps are to start a screen on a specific node and run ./proxy.sh.

```console
screen -S proxy
chmod +x proxy.sh
./proxy.sh
```
Use Ctrl + A, D to detach from screen

## PIP SSL ERROR

In case of an SSL error, this usually works for me

```console
pip install <PACKAGE/REQUIREMENTS_LIST/BUILD>  --trusted-host=pypi.org --trusted-host=files.pythonhosted.org --user
```
