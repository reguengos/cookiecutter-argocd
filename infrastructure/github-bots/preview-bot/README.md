# Editing the config.yaml

Parts of the file are encrypted using `sops` and a google kms key.

Decrypt the file **before** editing:

```bash
make sops-de
```

Now edit the file.

And encrypt it again:

```bash
make sops-en
```

Commit.

In a code review: if the file was edited, the checksum at the bottom must change.
If it does not, the file was edited in an encrypted state.
