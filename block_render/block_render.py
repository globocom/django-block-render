from itertools import islice
from django.http import HttpResponse
from django.template import loader, Context, RequestContext
from django.template.base import Template
from django.template.loader_tags import BlockNode, ExtendsNode


class BlockNotFound(Exception):
    """The requested block did not exist."""
    pass


def render_template_block(template, block, context, extend_nodelist=None):
    """
    Renders a single block from a template.
    This template should have previously been rendered.
    """
    if not isinstance(template, Template):
        template = loader.get_template(template)

    parent_node_list = template.nodelist

    if extend_nodelist:
        _update_nodelist(parent_node_list, extend_nodelist)

    return _render_template_block_nodelist(parent_node_list, block, context)

def _update_nodelist(nodelist, extended_nodelist):
    index = 0
    iterator = islice(nodelist, 0, len(nodelist))

    for node in iterator:
        if isinstance(node, BlockNode):
            for extended_node in extended_nodelist:
                if isinstance(extended_node, BlockNode) and extended_node.name == node.name:
                    nodelist[index] = extended_node

        for key in ('nodelist', 'nodelist_true', 'nodelist_false'):
            if hasattr(node, key):
                try:
                    _update_nodelist(getattr(node, key), extended_nodelist)
                except:
                    pass

        index += 1


def _render_template_block_nodelist(nodelist, block, context):
    for node in nodelist:
        if isinstance(node, BlockNode) and node.name == block:
            return node.render(context)
        for key in ('nodelist', 'nodelist_true', 'nodelist_false'):
            if hasattr(node, key):
                try:
                    rendered = _render_template_block_nodelist(
                        getattr(node, key), block, context)
                except:
                    pass
                else:
                    return rendered
    for node in nodelist:
        if isinstance(node, ExtendsNode):
            try:
                rendered = render_template_block(
                    node.get_parent(context), block, context, extend_nodelist=node.nodelist)
            except BlockNotFound:
                pass
            else:
                return rendered
    raise BlockNotFound


def render_block_to_string(template_name, block_name, dictionary=None,
                           context_instance=None):
    """Return a string
    Loads the given template_name and renders the given block with the
    given dictionary as context.
    """
    dictionary = dictionary or {}
    if context_instance:
        context_instance.update(dictionary)
    else:
        context_instance = Context(dictionary)
    return render_template_block(template_name, block_name, context_instance)


def render_block_to_response(request, template_name, block_name,
                             extra_context=None, mimetype=None, **kwargs):
    """
    Render a given block in a given template with any extra URL
    parameters in the context as ``{{ params }}``.
    """
    if extra_context is None:
        extra_context = {}
    dictionary = {'params': kwargs}
    for key, value in extra_context.items():
        if callable(value):
            dictionary[key] = value()
        else:
            dictionary[key] = value
    c = RequestContext(request, dictionary)
    return HttpResponse(render_template_block(template_name, block_name, c),
                        mimetype=mimetype)
