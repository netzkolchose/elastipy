from mistletoe import Document, BaseRenderer


def parse_markdown(text: str):
    text = "\n".join("" if not line.strip() else line.rstrip() for line in text.splitlines())
    try:
        text_indent = min(len(line) - len(line.lstrip()) for line in text.splitlines() if line.strip())
    except ValueError:
        text_indent = 0

    blocks = text.split("\n\n")

    out_blocks = []
    for block in blocks:
        block_lines = block.splitlines()
        try:
            block_indent = min(len(line) - len(line.lstrip()) for line in block_lines if line.strip())
        except ValueError:
            block_indent = 0
        block_lines = [line[block_indent:] for line in block_lines]
        block = "\n".join(block_lines)

        doc = Document(block)
        # print("-"*30)
        block = convert_markdown_block(doc)
        block = "\n".join(
            " " * (block_indent - text_indent) + line
            for line in block.splitlines()
        )
        # print(block)
        out_blocks.append(block)

    return "\n\n".join(out_blocks)


def convert_markdown_block(doc: Document) -> str:
    with RstRenderer() as renderer:
        result = renderer.render(doc)

    return result


class RstRenderer(BaseRenderer):
    """
    See mistletoe.base_renderer module for more info.
    """
    @staticmethod
    def escape_html(raw):
        return raw

    def render_inner(self, token):
        if hasattr(token, 'children'):
            return ''.join(map(self.render, token.children))
        else:
            return token.content

    def render_to_plain(self, token):
        if hasattr(token, 'children'):
            inner = [self.render_to_plain(child) for child in token.children]
            return ''.join(inner)
        return token.content

    def render_strong(self, token):
        template = '**{}**'
        return template.format(self.render_inner(token))

    def render_emphasis(self, token):
        template = '*{}*'
        return template.format(self.render_inner(token))

    def render_inline_code(self, token):
        template = '``{}``'
        inner = token.children[0].content
        return template.format(inner)

    def render_link(self, token):
        template = '`{title} <{target}>`__'
        inner = self.render_inner(token)
        title = token.title
        if not title:
            title = self.render_inner(token)
        return template.format(target=token.target, title=title, inner=inner)

    def render_escape_sequence(self, token):
        return self.render_inner(token)

    def render_raw_text(self, token):
        return self.escape_html(token.content)

    def render_paragraph(self, token):
        return self.render_inner(token)

    def render_block_code(self, token):
        return f".. CODE::\n\n{self.render_inner(token)}"

    def render_list(self, token):
        return '\n'.join(
            f"- {self.render(child)}"
            for child in token.children
        )

    def render_list_item(self, token):
        return self.render_inner(token)

    def render_line_break(self, token):
        # print(token, token.soft)
        return " "

    @staticmethod
    def render_thematic_break(token):
        return '---'

    def render_document(self, token):
        self.footnotes.update(token.footnotes)
        inner = '\n'.join(
            #f"{child} {self.render(child)}"
            f"{self.render(child)}"
            for child in token.children
        )
        return '{}\n'.format(inner) if inner else ''
