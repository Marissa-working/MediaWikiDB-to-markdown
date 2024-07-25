SELECT page.page_title, text.old_text
FROM page
JOIN revision ON page.page_latest = revision.rev_id
JOIN text ON revision.rev_text_id = text.old_id
WHERE page.page_namespace = 0;

