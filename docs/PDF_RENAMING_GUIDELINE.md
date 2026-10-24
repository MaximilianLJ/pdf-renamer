# PDF Renaming Guideline

Rename each PDF before uploading it to Paperless-ngx.

## Default Folder Workflow

Process every PDF placed in this folder in this order:

1. Inspect and rename the PDF using this guideline.
2. Deduplicate only when two files are byte-for-byte identical, sending the redundant copy to the Windows Recycle Bin.
3. Move the processed PDF to the configured consume folder or the target of `paperless_consume.lnk`.

The shortcut target is workstation-specific. Keep the local shortcut in the repository root; it is excluded from Git. The application can use a direct consume-folder path from its configuration instead.

Use the language of the document when naming the file:

- Use the English format for English documents.
- Use the German format for German documents.

## English Documents

### Filename Format

`YYYY-MM-DD_Document-Type_Correspondent_Description.pdf`

### Rules

1. Start with the document date in `YYYY-MM-DD` format.
2. Use an English document type.
3. Add the company, organization, authority, or person who issued the document.
4. Add a short description when useful.
5. Separate sections with underscores.
6. Use hyphens within multi-word sections.
7. Keep the filename short and descriptive.
8. Keep the `.pdf` extension unchanged.

### Examples

- `2026-07-11_Invoice_Amazon_Office-Supplies.pdf`
- `2026-06-30_Bank-Statement_Deutsche-Bank_Checking-Account.pdf`
- `2026-05-15_Insurance-Policy_Allianz_Home-Insurance.pdf`
- `2026-04-02_Receipt_IKEA_Furniture.pdf`
- `2026-03-01_Contract_Vodafone_Internet.pdf`

### Recommended English Document Types

- Invoice
- Receipt
- Bank-Statement
- Contract
- Insurance-Policy
- Tax-Notice
- Letter
- Payslip
- Medical-Report
- Warranty
- Manual
- Certificate
- Report

## German Documents

### Dateiformat

`YYYY-MM-DD_Dokumentart_Absender_Beschreibung.pdf`

### Regeln

1. Beginne mit dem Dokumentdatum im Format `YYYY-MM-DD`.
2. Verwende eine deutsche Dokumentart.
3. Fuege den Namen des Unternehmens, der Behoerde, Organisation oder Person hinzu, die das Dokument ausgestellt hat.
4. Ergaenze bei Bedarf eine kurze Beschreibung.
5. Trenne die einzelnen Bereiche mit Unterstrichen.
6. Verwende Bindestriche innerhalb mehrteiliger Begriffe.
7. Halte den Dateinamen kurz und eindeutig.
8. Behalte die Dateiendung `.pdf` unveraendert bei.
9. Verwende `ae`, `oe`, `ue` und `ss` anstelle von Umlauten und Eszett.

### Beispiele

- `2026-07-11_Rechnung_Amazon_Bueromaterial.pdf`
- `2026-06-30_Kontoauszug_Deutsche-Bank_Girokonto.pdf`
- `2026-05-15_Versicherungspolice_Allianz_Hausratversicherung.pdf`
- `2026-04-02_Kassenbon_IKEA_Moebel.pdf`
- `2026-03-01_Vertrag_Vodafone_Internetanschluss.pdf`
- `2026-02-15_Steuerbescheid_Finanzamt_Einkommensteuer-2025.pdf`

### Empfohlene deutsche Dokumentarten

- Rechnung
- Kassenbon
- Quittung
- Kontoauszug
- Vertrag
- Versicherungspolice
- Steuerbescheid
- Bescheid
- Schreiben
- Gehaltsabrechnung
- Arztbericht
- Garantie
- Bedienungsanleitung
- Bescheinigung
- Zertifikat
- Bericht

## General Rules

- Do not use `/`, `\`, `:`, `*`, `?`, `"`, `<`, `>` or `|` in filenames.
- Use consistent names for recurring correspondents and document types.
- Keep names concise while retaining useful identifying details.
- Preserve the `.pdf` extension.
- If only the year and month are known, use `YYYY-MM` (for example, `2026-07`).
- Use `Unknown-Date` for English documents only when no reliable date or month can be identified.
- Use `Datum-Unbekannt` for German documents only when no reliable date or month can be identified.

For example, consistently use `Deutsche-Bank`. Do not alternate between `Deutsche-Bank`, `DB`, `DeutscheBank` and `DeuBa`.

## Exact Duplicates

If two PDFs are byte-for-byte identical, keep one copy and send the redundant copy to the Windows Recycle Bin. Do not permanently delete it. Do not deduplicate merely because documents look similar or share an invoice number; translated versions, revisions and different scans should remain separate.

## Avoid

- `scan001.pdf`
- `Dokument (4).pdf`
- `rechnung neu final.pdf`
- `Amazon_11-07-26.pdf`
- `Brief von Versicherung.pdf`

## Checklist Before Uploading

- [ ] The date is correct.
- [ ] The document language is used for the filename.
- [ ] The document type is clear.
- [ ] The correspondent name is consistent.
- [ ] The description is short and useful.
- [ ] The filename contains no unsupported characters.
- [ ] Umlauts and Eszett are transliterated in German filenames.
- [ ] The `.pdf` extension is unchanged.
- [ ] Exact duplicates have been removed.
