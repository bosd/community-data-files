# Copyright 2026 OBS Solutions B.V.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)
import base64
import logging

from lxml import etree

from odoo import SUPERUSER_ID, api
from odoo.tools import file_open

_logger = logging.getLogger(__name__)


def migrate(cr, version):
    """Fill the label pictograms lost by the XML to CSV data migration.

    ``data/adr_label.xml`` is ``noupdate``, so on an existing database Odoo
    skips the label records that the CSV file already created without an
    image. Load the images from the XML data file for the labels that are
    still empty, leaving any image a user uploaded in the meantime alone.
    """
    env = api.Environment(cr, SUPERUSER_ID, {})
    with file_open("l10n_eu_product_adr/data/adr_label.xml", "rb") as data_file:
        tree = etree.parse(data_file)
    filled = 0
    for field in tree.xpath("//record[@model='adr.label']/field[@name='image'][@file]"):
        xmlid = field.getparent().get("id")
        label = env.ref(f"l10n_eu_product_adr.{xmlid}", raise_if_not_found=False)
        if not label or label.image:
            continue
        with file_open(field.get("file"), "rb") as image_file:
            label.image = base64.b64encode(image_file.read())
        filled += 1
    _logger.info("Restored the pictogram of %s ADR labels", filled)
