# MediaWiki to Markdown Exporter
This repository contains scripts and tools for exporting all pages from a MediaWiki database to Markdown format using Pandoc. The process involves extracting page content from the MediaWiki SQLite/MySQL database for mediawiki > 1.35 and converting it into Markdown files.

## Find your MediaWiki version
If you go to the main page of the wiki and in the sidebar click on 'special pages' under 'Tools' and then click on 'version' under 'Wiki data and tools' It will give you the version and php etc.

## MediaWiki Database Schema Reference
* https://www.mediawiki.org/wiki/Manual:Database_layout
* https://www.mediawiki.org/w/index.php?title=Manual:Database_layout/diagram&action=render
* Three most important tables:
  * Page table: https://www.mediawiki.org/wiki/Manual:Page_table
    * Contains page_title(page title!), page_id, page_latest
  * Revision table: https://www.mediawiki.org/wiki/Manual:Revision_table
    * Contains rev_id, rev_page, rev_text_id(in older version of mediawiki)
  * Text table: https://www.mediawiki.org/wiki/Manual:Text_table
    * Contains old_id, old_text(content!)
## Reference
* https://www.mediawiki.org/wiki/Topic:Pxovvjcr9goluynq
