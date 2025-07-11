#!/bin/bash

README_FILE="README.md"
INDEX_FILE="index.html"

LAST_UPDATED=$(python3 -c "from orbeat_time import to_ucy, to_eastern; print(f'{to_ucy()} UCY | {to_eastern()}')")

echo $LAST_UPDATED

sed -i "/<!-- LAST_UPDATED_START -->/,/<!-- LAST_UPDATED_END -->/c\\
<!-- LAST_UPDATED_START -->\\
<span>Last Updated: $LAST_UPDATED</span>\\
<!-- LAST_UPDATED_END -->
" "$INDEX_FILE"

sed -i "/<!-- LAST_UPDATED_START -->/,/<!-- LAST_UPDATED_END -->/c\\
<!-- LAST_UPDATED_START -->\\
**Last Updated:** $LAST_UPDATED\\
<!-- LAST_UPDATED_END -->
" "$README_FILE"
