# -----------------------------------------------------------------------------
# Bootstrap configuration of make, macros
# -----------------------------------------------------------------------------

# Export all Make variables by default to sub-make as well as Shell calls.
#
# Note that you can still explicitely mark a variable with `unexport` and it is
# not going to be exported by Make, regardless of this setting.
#
# https://www.gnu.org/software/make/manual/html_node/Variables_002fRecursion.html
export

# Disable/enable various make features.
#
# https://www.gnu.org/software/make/manual/html_node/Options-Summary.html
MAKEFLAGS += --no-builtin-rules
MAKEFLAGS += --no-builtin-variables
MAKEFLAGS += --no-print-directory
MAKEFLAGS += --warn-undefined-variables

# Never delete a target if it exits with an error.
#
# https://www.gnu.org/software/make/manual/html_node/Special-Targets.html
.DELETE_ON_ERROR :=

# The shell that should be used to execute the recipes.
SHELL       := bash
.SHELLFLAGS := -euo pipefail -c

# Determine the root directory of our codebase and export it, this allows easy
# file inclusion in both Bash and Make.
override ROOT := $(shell path="$(CURDIR)"; while [[ "$${path}" != "/" \
 && ! -f "$${path}/.root.mk" ]]; do path="$${path%/*}"; done; echo "$${path}")
ifeq ($(ROOT),$(CURDIR))
override IS_ROOT := true
else
override IS_ROOT := false
endif

# We extend the path with our global bin directory, as well as the make specific
# one from the resources. Note that we append instead of prepending them, is
# ensures that a) our scripts never overwrite existing executables, and b)
# overwriting of our scripts is possible (as we do it in CI).
PATH := $(PATH):$(ROOT)/bin:$(ROOT)/resources/make/bin

ifeq ($(IS_ROOT),false)
PATH := $(PATH):$(CURDIR)/bin:$(CURDIR)/resources/make/bin
endif


# This makes all targets silent by default, unless VERBOSE is set.
ifndef VERBOSE
.SILENT:
endif

# This executes all targets in a single shell. This improves performance, by
# not spawning a new shell for each line, and also allows use to write multiline
# commands like conditions and loops without escaping sequences.
#
# https://www.gnu.org/software/make/manual/html_node/One-Shell.html
.ONESHELL:

# Disable the suffix functionality of make.
#
# https://www.gnu.org/software/make/manual/html_node/Suffix-Rules.html
.SUFFIXES:

dash-split = $(word $2,$(subst -, ,$1))
dash-1 = $(call dash-split,$*,1)
dash-2 = $(call dash-split,$*,2)
