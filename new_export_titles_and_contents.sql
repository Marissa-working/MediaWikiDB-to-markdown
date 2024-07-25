SELECT page.page_title, text.old_text
FROM page
JOIN revision ON page.page_latest = revision.rev_id
JOIN slots ON revision.rev_id = slots.slot_revision_id
JOIN content ON slots.slot_content_id = content.content_id
JOIN text ON CAST(SUBSTR(content.content_address, 4) AS INTEGER) = text.old_id
WHERE page.page_namespace = 0;

