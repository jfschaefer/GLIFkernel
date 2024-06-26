# from ipykernel.kernelbase import Kernel
# it seems easier to use IPythonKernel if we want to use widgets... - TODO: find a more stable solution
from ipykernel.ipkernel import IPythonKernel as Kernel
from ipywidgets import widgets
from IPython.display import display
from glif.glif import Glif
from glif import utils
from glif.commands.items import Repr
import html
import os


def html_escape(string):
    """ escapes html chars and replaces '\n' by '<br/>' """
    return html.escape(str(string)).replace('\n', '<br/>').replace('  ', '&nbsp;&nbsp;')

def markdown_escape(string):
    return string.replace('*', '\\*').replace('$', '\\$')


class GlifKernel(Kernel):
    implementation = 'GLIF Kernel'
    implementation_version = '0.0.1'
    language = 'glif'
    language_version = '0.0.1'
    language_info = {
        'name': 'GLIF',
        'mimetype': 'text/glif',
        'file_extension': '.glif',  # ???
        "codemirror_mode": {
            "name": "glif",
            # "name": "ipython",
            # "version": 3
        },
    }
    banner = "GLIF"

    def __init__(self, **kwargs):
        Kernel.__init__(self, **kwargs)
        self.glif = Glif()
        self._unicode_latex_map = None  # for tab completion, will be loaded on demand
        self.myexecutioncount = 0  # IPythonKernel does its own thing and overrides the
        # kernelbase.Kernel.execution_count

    def do_execute(self, code, silent, store_history=True, user_expressions=None, allow_stdin=False):
        if not silent:
            for i, r in enumerate(self.glif.execute_cell(code)):
                if i > 0:
                    # separator
                    self.html_response('<hr class="glif-sep"/>')
                if r.value:
                    self.handle_items(r.value)
                else:
                    self.html_response(f'<div class="glif-stderr">{html_escape(r.logs)}</div>')

        self.myexecutioncount += 1
        return {'status': 'ok',
                'execution_count': self.myexecutioncount,
                'payload': [],
                'user_expressions': {},
                }

    def html_response(self, html):
        self.send_response(self.iopub_socket, 'display_data', {
            'data': {'text/html': html},
            'metadata': {}, 'transient': {},
        })

    def handle_items(self, items):
        # check current representation
        cur_repr = None
        if items.items:
            cur_repr = items.items[0].currentRepr
        if not all(i.currentRepr == cur_repr for i in items.items):
            self.html_response(
                f'<div class="glif-stderr">Internal error:'
                f'Inconsistent output representations: {set([i.currentRepr for i in items.items])}</div>')
        if cur_repr in {Repr.GRAPH_DOT, Repr.GRAPH_SVG}:
            self.show_graphs(items)
        else:
            self.html_response(markdown_escape(items.html()))

    def show_graphs(self, items):
        assert items.items
        label2item = {}
        origidcount = {}
        labels = []
        for i in items.items:
            if i.original_id not in origidcount:
                origidcount[i.original_id] = 0

            ast = i.content[Repr.AST] if Repr.AST in i.content else '[no AST]'
            label = f'{i.original_id}.{origidcount[i.original_id]}. {ast}'
            label2item[label] = i
            labels.append(label)
            origidcount[i.original_id] += 1

        dropdown = widgets.Dropdown(
            layout={'width': 'max-content'},
            options=labels,
            value=labels[0],
            description='',
            disabled=False,
        )

        image = widgets.Image(format='svg+xml')

        def show_graph(label):
            item = label2item[label]
            if Repr.GRAPH_SVG not in item.content:
                r = utils.dot2svg(item.content[Repr.GRAPH_DOT].encode())
                if r.success:
                    item.content[Repr.GRAPH_SVG] = r.value
                else:
                    self.html_response(
                        f'<div class="glif-stderr">Failed to produce graph:<br/>{html_escape(r.logs)}</div>')
                    return
            image.value = item.content[Repr.GRAPH_SVG]

        show_graph(labels[0])
        dropdown.observe(lambda bunch: show_graph(bunch['new']), names='value')
        display(dropdown, image)

    @property
    def unicode_latex_map(self):
        if self._unicode_latex_map is None:
            self._unicode_latex_map = {}
            with open(os.path.join(os.path.dirname(__file__), 'unicode-latex-map'), 'r', encoding='utf-8') as fp:
                for line in fp:
                    line = line.strip()
                    if line.startswith('//'):  # comment
                        continue
                    if not line:
                        continue
                    e = line.split('|')
                    if len(e) != 2 or e[0][0] != 'j':
                        print(f'Failed to understand the following entry in unicode-latex-map: {line}')
                    self._unicode_latex_map[e[0][1:]] = e[1]
        return self._unicode_latex_map

    def do_complete(self, code, cursor_pos):
        # 1. UNICODE COMPLETION
        # find preceding backslash for character completion
        c = cursor_pos - 1
        while c >= 0 and code[c].isalnum():
            c -= 1
        if c >= 0 and code[c] == '\\' and code[c + 1:cursor_pos] in self.unicode_latex_map:
            return {'matches': [self.unicode_latex_map[code[c + 1: cursor_pos]]],
                    'cursor_end': cursor_pos,
                    'cursor_start': c,
                    'metadata': {},
                    'status': 'ok'}

        # 2. VIEW/CONCRETE COMPLETION
        c2 = None
        if c >= 0 and code[c] == ' ':
            if c >= 8 and code[c - 8:c] == 'concrete':
                c2 = c - 8
            elif c >= 4 and code[c-4:c] == 'view':
                c2 = c - 4
        if c2 is not None:
            stub = self.glif.stub_gen(code[c2:cursor_pos])
            if not stub.success:
                print('Stub generation failed:', stub.logs)
            assert stub.value
            return {'matches': [stub.value],
                    'cursor_end': cursor_pos,
                    'cursor_start': c2,
                    'metadata': {},
                    'status': 'ok'}

    def do_shutdown(self, restart):
        self.glif.do_shutdown()
        return {'status': 'ok', 'restart': restart}
