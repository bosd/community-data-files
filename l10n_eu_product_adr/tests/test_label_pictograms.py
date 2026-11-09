# Copyright 2026 OBS Solutions B.V.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)
import base64
import importlib.util

from odoo.modules.module import get_module_path
from odoo.tests import TransactionCase


class TestLabelPictograms(TransactionCase):
    def _load_migration(self):
        path = (
            get_module_path("l10n_eu_product_adr")
            + "/migrations/18.0.1.1.1/post-migration.py"
        )
        spec = importlib.util.spec_from_file_location("adr_label_migration", path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    def test_labels_have_pictograms(self):
        labels = self.env["adr.label"].search([])
        self.assertEqual(len(labels), 22)
        self.assertFalse(labels.filtered(lambda label: not label.image))

    def test_migration_restores_empty_pictograms(self):
        """Empty labels get their pictogram back, custom images are kept."""
        empty = self.env.ref("l10n_eu_product_adr.adr_label_3")
        custom = self.env.ref("l10n_eu_product_adr.adr_label_8")
        custom_image = base64.b64encode(b"<svg/>")
        # The image is stored as an attachment; drop it like the CSV data did
        self.env["ir.attachment"].search(
            [
                ("res_model", "=", "adr.label"),
                ("res_field", "=", "image"),
                ("res_id", "=", empty.id),
            ]
        ).unlink()
        empty.invalidate_recordset()
        custom.image = custom_image
        self.assertFalse(empty.image)

        self._load_migration().migrate(self.env.cr, "18.0.1.1.0")

        empty.invalidate_recordset()
        custom.invalidate_recordset()
        self.assertTrue(empty.image)
        self.assertEqual(custom.image, custom_image)
