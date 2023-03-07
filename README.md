# aurmr-setup 

A setup script for the Amazon Manipulation Project @ UW

The setup script utilizes conda packages provided by the robostack team.
Additionally, it helps to inject custom user variables into the environment and
with the setup.


## Quickstart

To create a new workspace just type `aurmr init`. In the next step you can use
`aurmr install` to install the software.


## Installation

Install with

```sh
pip install git+https://github.com/au-rmr/aurmr-setup.git
```

Run `aurmr recipes system-prepare` to configure the operating system. The step needs to
be only done once.

## Workspace usage

### Creating a new workspace

`aurmr init` will create a new workspace. Similar, `aurmr clone` will clone an
existing workspace copying also the source folder

### Using a workspace

Just use `activate` in the shell. Do not confuse that command with `conda
activate`. Both are similar, but `acticate` also injects the ros parameters
into the current environment and loads some user variables.

### Configuring a workspace

You can create a `user.bashrc` which will be automatically sources

Add new packages with `aurmr add <package-name` or clone repositories with
`aurmr add-src`.

You can also use `aurmr install` to install some existing receipes.


### Misc

You can use `commit` instead of `git commit` to select the author
