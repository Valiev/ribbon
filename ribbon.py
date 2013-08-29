from subprocess import Popen, PIPE


class RibbonExcecutionException(Exception):
    def __init__(self, command_line, exit_code, message = None):
        Exception.__init__(self)
        self.command_line = command_line
        self.exit_code = exit_code
        self.message = message

    def __str__(self):
        msg = "'%(command_line)s' returned %(exit_code)d exit code" % self.__dict__
        if self.message:
            msg += " with message '%s'" % self.message
        return msg


class CmdBuilder(object):
    def __init__(self, short_option_prefix='', option_prefix='', correct_kwargs=True):
        self.short_option_prefix = short_option_prefix
        self.option_prefix = option_prefix
        self.correct_kwargs = correct_kwargs

    def build_cmd_list(self, *args, **kwargs):
        cmd_list = list(args)

        for k, v in kwargs.iteritems():
            if len(k) == 1:
                option_prefix = self.short_option_prefix
            else:
                option_prefix = self.option_prefix
            key = "%s%s" % (option_prefix, k)

            if self.correct_kwargs:
                key = key.replace('_', '-')

            if type(v) is bool:
                if v:
                    cmd_list.append(key)
            else:
                cmd_list.extend([key, v])
        return cmd_list

    def build_cmd_str(self, *args, **kw):
        cmd_list = self.build_cmd_list(*args, **kw)
        return " ".join(cmd_list)


class PopenArgsSplitter(object):
    DEFAULT_ARGS = ("stdout", "stderr", "stdin")

    def __init__(self, *popen_args):
        self.args_to_parse = set(popen_args or self.DEFAULT_ARGS)

    def split(self, **kwargs):
        popen_args = {}
        for key, value in kwargs.items():
            if key in self.args_to_parse:
                popen_args[key] = kwargs.pop(key)
        return popen_args, kwargs

    def skip_popen_options(self, **kwargs):
        _, kw = self.split(**kwargs)
        return kw


class BaseRibbon(object):
    def __init__(self, cmd_builder, popen_args_splitter, *args, **kwargs):
        self.builder = cmd_builder
        self.splitter = popen_args_splitter
        self.args = args
        self.popen_options, self.kwargs = self.splitter.split(**kwargs)
        self.base_cmd = self.builder.build_cmd_list(*args, **self.kwargs)

    def build_cmd_list(self, *args, **kwargs):
        kwargs = self.splitter.skip_popen_options(**kwargs)
        extra_cmd = self.builder.build_cmd_list(*args, **kwargs)
        return self.base_cmd + extra_cmd

    def build_cmd_str(self, *args, **kwargs):
        return " ".join(self.build_cmd_list(*args, **kwargs))

    def Popen(self, *args, **kwargs):
        popen_options = self.popen_options.copy()
        new_popen_options, kwargs = self.splitter.split(**kwargs)
        popen_options.update(new_popen_options)
        extra_cmd = self.builder.build_cmd_list(*args, **kwargs)
        cmd = self.base_cmd + extra_cmd
        return Popen(cmd, **popen_options)

    def system(self, *args, **kwargs):
        fd = self.Popen(*args, **kwargs)
        return fd.wait()

    def system_exc(self, *args, **kwargs):
        ret = self.system(*args, **kwargs)
        if ret:
            cmd = self.build_cmd_str(*args, **kwargs)
            raise RibbonExcecutionException(cmd, ret)

    def getstatusoutput(self, *args, **kwargs):
        kwargs.update(dict(
            stdout = PIPE,
            stderr = PIPE,
        ))
        fd = self.Popen(*args, **kwargs)
        stdout, stderr = fd.communicate()
        ret = fd.wait()
        return ret, stdout

    def getoutput(self, *args, **kw):
        ret, out = self.getstatusoutput(*args, **kw)
        if ret:
            cmd = self.build_cmd_str(*args, **kw)
            raise RibbonExcecutionException(cmd, ret)
        return out


def Ribbon(*args, **kwargs):
    cmd_builder = CmdBuilder(short_option_prefix='-', option_prefix='--')
    popen_args_splitter = PopenArgsSplitter()
    return BaseRibbon(cmd_builder, popen_args_splitter, *args, **kwargs)


def WinRibbon(*args, **kwargs):
    cmd_builder = CmdBuilder(short_option_prefix='/', option_prefix='/')
    popen_args_splitter = PopenArgsSplitter()
    return BaseRibbon(cmd_builder, popen_args_splitter, *args, **kwargs)
