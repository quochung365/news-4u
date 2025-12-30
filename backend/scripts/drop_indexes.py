# backend/scripts/drop_indexes.py
#!/usr/bin/env python3
"""
Drop old indexes from database.
"""
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from database import get_db, engine
from sqlalchemy import text

def drop_indexes():
    """Drop all the old indexes."""
    db = next(get_db())
    try:
        indexes_to_drop = [
            'idx_feed_category',
            'idx_feed_active',
            'idx_article_category',
            'idx_article_source',
            'idx_article_published',
            'idx_article_processed',
            'idx_article_title',
            'idx_article_slug',
            'idx_log_feed_name',
            'idx_log_timestamp',
            'idx_log_status',
        ]
        
        for index_name in indexes_to_drop:
            try:
                db.execute(text(f"DROP INDEX IF EXISTS {index_name}"))
                print(f"✓ Dropped index: {index_name}")
            except Exception as e:
                print(f"⚠ Could not drop {index_name}: {e}")
        
        db.commit()
        print("\n✓ Index cleanup completed!")
        
    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    drop_indexes()