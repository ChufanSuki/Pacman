for r in self._constraints:
    self._joined_utils = join(self._joined_utils, r)

    # use projection to eliminate self out of the message to our parent
util = projection(self._joined_utils, self._variable, self._mode)