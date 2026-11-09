## 18.0.1.1.1

- \[FIX\] Restore the label pictograms on existing databases. The
  pictograms were lost when the data files were migrated to CSV, and
  the restored `noupdate` data file does not update existing labels.
- \[FIX\] Show the label pictogram next to its code and name in the
  kanban card, so the text no longer overflows the card.

## 14.0.1.0.0 (2021-05-04)

- \[BREAKING\] Gather dangerous goods attributes on a new model
  adr.goods, and replace all product attributes with a Many2one on this
  model. Remove all other unused or unclear attributes.
- \[ADD\] XML data for the dangerous goods table from the 2019 edition,
  including translations in 3 languages.
