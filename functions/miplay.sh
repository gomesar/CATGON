#!/bin/bash
# gomesar (https://github.com/gomesar/CATGON) 2018
# Correctly configure 'my_instant_folder' variable
# (Put only .mp3 files from 'www.myinstants.com' in this folder).
# Dependency: <sudo apt-get install> sox libsox-fmt-mp3
# Add to your interpreter config file (.bashrc, .zsh, etc):
# 	source path/to/miplay.sh &>/dev/null

my_instant_folder=~/Music/my-instants/

function miplay() {
	play "${my_instant_folder}"$1
}

_miplay_completions()
{
	if [ "${#COMP_WORDS[@]}" != "2" ]; then
	    return
	fi

	local cur prev opts

	cur="${COMP_WORDS[1]}"
    prev="${COMP_WORDS[COMP_CWORD-1]}"
	opts="$(ls ${my_instants_folder} | grep '.mp3' | sed 's/\t/\n/')"

	COMPREPLY=( $(compgen -W "${opts}" -- "${cur}") )
	return 0
}
if [ -z "$ZSH" ]; then
	echo "ZSH not found"
	complete -F _miplay_completions miplay
else
	echo "ZSH detected"
	compdef _miplay_completion miplay
fi
