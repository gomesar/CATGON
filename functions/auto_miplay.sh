_miplay_completions()
{
	if [ "${#COMP_WORDS[@]}" != "2" ]; then
	    return
	fi
	local cur prev opts my_instants_folder
	my_instants_folder=~/Music/my-instants/

	#cur="${COMP_WORDS[COMP_CWORD]}"
	cur="${COMP_WORDS[1]}"
    prev="${COMP_WORDS[COMP_CWORD-1]}"
	#opts="$(ls ${my_instants_folder} | grep '.mp3' | sed 's/\t/\n/')"
	opts="$(ls ${my_instants_folder} | grep '.mp3' | sed 's/\t/\n/')"

	COMPREPLY=( $(compgen -W "${opts}" -- "${cur}") )
	return 0
}
complete -F _miplay_completions miplay
