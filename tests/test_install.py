import importlib.util
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("install", ROOT / "scripts/install.py")
installer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(installer)


class InstallTests(unittest.TestCase):
    def test_install_idempotence_and_protected_update(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "app/skills"
            installer.install(installer.SOURCE, root)
            dest = root / installer.NAME
            self.assertEqual(installer.digest(installer.SOURCE), installer.digest(dest))
            self.assertIn("Already current", installer.install(installer.SOURCE, root))
            (dest / "SKILL.md").write_text("local customization")
            with self.assertRaises(ValueError):
                installer.install(installer.SOURCE, root)
            installer.install(installer.SOURCE, root, replace=True)
            backups = list((root.parent / "skill-backups").iterdir())
            self.assertEqual(len(backups), 1)
            self.assertEqual((backups[0] / "SKILL.md").read_text(), "local customization")
            self.assertEqual(installer.digest(installer.SOURCE), installer.digest(dest))

    def test_refuses_symlink_replacement(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / installer.NAME).symlink_to(installer.SOURCE, target_is_directory=True)
            with self.assertRaises(ValueError):
                installer.install(installer.SOURCE, root, replace=True)


if __name__ == "__main__":
    unittest.main()
