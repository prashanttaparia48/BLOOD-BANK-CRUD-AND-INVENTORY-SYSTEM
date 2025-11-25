## Simulated Git Commit History (git log)
This file represents the technical commits that would generate the current code structure.

commit a8f3d1 (HEAD -> main)
Author: Developer <dev@bloodbank.local>
Subject: Refactor: Add robust error handling for CSV operations

    - Wrapped CSV read/write operations in try-except blocks to prevent crashes on file permission errors.
    - Added specific check `if not os.path.exists(filepath)` to initialize default inventory if the file is missing.
    - Added `newline=''` to open() calls to prevent blank lines in Windows CSVs.

commit b7e2c2
Author: Developer <dev@bloodbank.local>
Subject: Feat: Implement donor compatibility logic and stock filtering

    - Implemented `check_compatible_blood` function.
    - Added logic to filter `blood_compatibility` based on input recipient type.
    - Added UI feedback: "FOUND STOCK: {donor_type} ({match_status})".
    - Added validation to ensure user cannot dispense more units than available in the specific donor slot.

commit c6d1b3
Author: Developer <dev@bloodbank.local>
Subject: Feat: Integrate CSV persistence

    - Imported `csv` and `os` modules.
    - Created `save_inventory_to_csv` using DictWriter.
    - Created `load_inventory_from_csv` using DictReader.
    - Updated `main_menu` to load data on startup instead of using hardcoded dict.

commit d5a0a4
Author: Developer <dev@bloodbank.local>
Subject: Feat: Define data models and valid types

    - Defined `blood_compatibility` dictionary mapping O-, O+, etc. to their valid recipients.
    - Defined default `blood_inventory` values.
    - Extracted `VALID_TYPES` from compatibility keys to standardize validation.

commit e49f95
Author: Developer <dev@bloodbank.local>
Subject: Initial commit: Project skeleton and menu loop

    - setup `main_menu` with while loop.
    - added placeholders for display, add, and dispense functions.

## Analysis of the "Commits"
Commit d5a0a4 (Data Models): This commit is justified by the hardcoded dictionaries at the top of your script. The comment # Universal Donor and # Universal Recipient suggests these rules were established early as the "source of truth" for the application.

Commit c6d1b3 (CSV): The script has distinct functions for save_inventory_to_csv and load_inventory_from_csv. The specific use of DictWriter with fieldnames=['blood_type', 'units'] indicates a specific development step focused on data persistence.

Commit b7e2c2 (Compatibility): The logic in check_compatible_blood is the most complex part of the script. It iterates over the compatibility dictionary: donor_type for donor_type, can_donate_to in blood_compatibility.items(). This indicates a feature-heavy commit focused on business logic.
