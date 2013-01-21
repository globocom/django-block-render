from django.template.base import Template
from block_render.block_render import render_block_to_string
import unittest


class BlockRenderTest(unittest.TestCase):

    def setUp(self):
        self.html = '{% block main %}\
bloco principal\
 {% block interno %}\
 block interno\
{% endblock %}\
{% endblock %}'
        self.template = Template(self.html)

    def test_renderizacao_bloco_main(self):
        rendered = render_block_to_string(self.template,
                                          "main")
        self.assertEqual("bloco principal  block interno", rendered)

    def test_renderizacao_bloco_interno(self):
        rendered = render_block_to_string(self.template,
                                          "interno")
        self.assertEqual(" block interno", rendered)

    def test_renderizacao_load_template(self):
        template = "block_render.html"
        text = render_block_to_string(template, "main")
        self.assertEqual("\nbloco main\n\nbloco main include\n\n\n",
                         text)

    def test_contexto_include(self):
        contexto = {"TESTE_DE_CONTEXTO": "Teste de contexto"}
        template = "block_render.html"
        text = render_block_to_string(template, "main", contexto)
        self.assertIn("Teste de contexto", text)

    def test_contexto_extends(self):
        contexto = {"TESTE_DE_CONTEXTO": "Teste de contexto"}
        template = "extend_block.html"
        text = render_block_to_string(template, "main", contexto)
        self.assertIn("Teste de contexto", text)
