## The 100GB home quota

The home memory fills up like the thermometer in New Delhi on a summer day. To check how much your are using use:

```console
lfs quota -hu $USER /home
```

This commands just shows you the net memory you are using and is very useless when you run out of space.

The command that will actually help you is this:

```console
ll -u -a -h
```

Haha, not really. This one is also useless as it does not show the actual memory occupied by the  folders in your home directory. 

Usually when the memory fills up, it is due to the cache space. You should definitely clear out the cache using:
```console
rm -rf $HOME/.cache
```

If you are working with LLMs, HuggingFace cache requires a ton of memory to save models. The best way to deal with this is to change the location of HuggingFace cache as soon as you login into a node/screen.

```console
export HF_HOME=\$HOME/scratch/huggingface 
```

## Scratch is also limited

Although there's a ton of memory in scratch, it's limited. Check using:

```console
lfs quota -hu $USER /scratch
```

Also ensure that you take backups from scratch as it's not permanent