import hou


class Task(object):
    """A Task is a command and the list of frames it relates to.

    It provides a handful of tokens that can be used to
    construct the command.
    """

    def __init__(self, clump, command, parent_tokens):
        """Resolve the tokens and the command.

        After calling setenv, tokens such as start end step
        and so on are valid. So when we expand the command
        any tokens that were used are correctly resolved.
        """
        self._clump = clump
        self._tokens = self._setenv(parent_tokens)
        self._command = hou.expandString(command)

    def _setenv(self, parent_tokens):
        """Env tokens at the task level.

        Task level tokens are joined with Job and submission
        level tokens so that all tokens are available when
        constructing the task command.

        Example:
        python myCmd.py -s $CT_CLUMPSTART -e $CT_CLUMPEND -n $CT_SOURCE -f $CT_SCENE
        """

        tokens = {}
        clump_type = type(self._clump).__name__.lower()[:-5]
        tokens["CT_CLUMPTYPE"] = clump_type
        tokens["CT_CLUMP"] = str(self._clump)
        tokens["CT_CLUMPLENGTH"] = str(len(self._clump))
        tokens["CT_CLUMPSTART"] = str(self._clump.start)
        tokens["CT_CLUMPEND"] = str(self._clump.end)
        tokens["CT_CLUMPSTEP"] = str(
            self._clump.step) if clump_type == "regular" else "~"

        for token in tokens:
            hou.putenv(token, tokens[token])
        tokens.update(parent_tokens)

        return tokens

    def data(self):
        return {
            "frames": str(tuple(self._clump)),
            "command": self._command
        }

    @property
    def clump(self):
        return self._clump

    @property
    def command(self):
        return self._command

    @property
    def tokens(self):
        return self._tokens