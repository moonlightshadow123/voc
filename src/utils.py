import sys, traceback
from prompt_toolkit.styles import Style
from prompt_toolkit import print_formatted_text
from prompt_toolkit.formatted_text import FormattedText



style = Style.from_dict({
    '':'bg:#303030 fg:#a0a0a0',
    'completion-menu.completion': 'bg:#008888 #ffffff',
    'completion-menu.completion.current': 'bg:#00aaaa #000000',
    'scrollbar.background': 'bg:#88aaaa',
    'scrollbar.button': 'bg:#222222',
    'primary': 'fg:#00007f bold',
    'success': 'fg:#007f00 bold',
    'info':'fg:#007f7f bold',
    'warning':'fg:#7f7f00 bold',
    'danger':'fg:#7f0000 bold',
    'comp':'fg:#7f007f bold'
})
'''
    'primary': 'bg:#00007f fg:#dfdfdf bold',
    'success': 'bg:#007f00 fg:#dfdfdf bold',
    'info':'bg:#007f7f fg:#dfdfdf bold',
    'warning':'bg:#7f7f00 fg:#dfdfdf bold',
    'danger':'bg:#7f0000 fg:#dfdfdf bold',
    'comp':'bg:#7f007f fg:#dfdfdf bold'

    'primary': 'bg:#0000ff #ffff00 fg:#0f0f0f',
    'success': 'bg:#00ff00 #ff00ff fg:#0f0f0f',
    'info':'bg:#00ffff #ff0000 fg:#0f0f0f',
    'warning':'bg:#ffff00 fg:#0f0f0f',
    'danger':'bg:#ff0000 fg:#0f0f0f',
    'comp':'bg:#ff00ff fg:#0f0f0f'
'''
def print_f(arr):
    text = FormattedText(arr)
    print_formatted_text(text, style=style, end="\n")

def getTraceLog(err):
    exc_type, exc_value, exc_traceback = sys.exc_info()
    traces = traceback.format_exception(exc_type, exc_value, exc_traceback)
    traceLogs = ""
    for trace in traces:
        traceLogs += trace
    return traceLogs

def get_decorator(errors=(Exception, ), default_value=''):

    def decorator(func):

        def new_func(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as err:
                print("Oops, something went wront...Here's the detail:\n{}".format(getTraceLog(err)))
                # return default_value
        return new_func

    return decorator

try_deco = get_decorator((KeyError, NameError), default_value='default')


if __name__ == "__main__":
    a = {}

    @f
    def example1(a):
        return a['b']

    @f
    def example2(a):
        return doesnt_exist()

    print(example1(a))
    print(example2(a))