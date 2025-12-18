uic:
    pyside6-uic ui/components/inventory/empty.ui -o ui/components/inventory/empty_ui.py
    pyside6-uic ui/components/inventory/inventory_equipment_form.ui -o ui/components/inventory/inventory_equipment_form_ui.py
    pyside6-uic ui/components/inventory/inventory_stackable_form.ui -o ui/components/inventory/inventory_stackable_form_ui.py
    pyside6-uic ui/components/inventory/inventory.ui -o ui/components/inventory/inventory_ui.py
    pyside6-uic ui/components/settings/settings.ui -o ui/components/settings/settings_ui.py
    pyside6-uic ui/components/equipment_search/equipment_search.ui -o ui/components/equipment_search/equipment_search_ui.py
    pyside6-uic ui/components/stackable_search/stackable_search.ui -o ui/components/stackable_search/stackable_search_ui.py
    pyside6-uic ui/components/mail/mail.ui -o ui/components/mail/mail_ui.py
    pyside6-uic ui/components/mail/equipment_form.ui -o ui/components/mail/equipment_form_ui.py
    pyside6-uic ui/components/mail/stackable_form.ui -o ui/components/mail/stackable_form_ui.py
    pyside6-uic ui/components/characters/characters.ui -o ui/components/characters/characters_ui.py
    pyside6-uic ui/components/quests/quests.ui -o ui/components/quests/quests_ui.py
    pyside6-uic ui/components/character_info/character_info.ui -o ui/components/character_info/character_info_ui.py

build-resource:
    pyside6-rcc resources/resources.qrc -o resources/resources_rc.py

build-python-module:
    uv run maturin develop -r --features python

build-macos-app:
    pyinstaller --clean --noconfirm main.spec

release-macos-app: build-macos-app
    # Create a temporary folder for the DMG contents
    mkdir -p dist/dmg_temp

    # Copy your app bundle into the temporary folder
    cp -r "dist/seria.app" dist/dmg_temp

    # (Optional) Add a symlink to the Applications folder
    ln -sf /Applications dist/dmg_temp/Applications

    rm -f dist/seria.dmg
    # Run create-dmg with specific options
    create-dmg \
      --volname "Seria Installer" \
      --volicon "resources/icon.icns" \
      --window-pos 200 120 \
      --window-size 600 300 \
      --icon-size 100 \
      --icon "seria" 175 120 \
      --app-drop-link 425 120 \
      "dist/seria.dmg" \
      "dist/dmg_temp/"

    # Clean up the temporary folder
    rm -rf dist/dmg_temp

build-windows-app:
    pyinstaller --clean --noconfirm main.spec
