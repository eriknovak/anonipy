import unittest

from anonipy.definitions import Entity


# =====================================
# Test Entity
# =====================================


class TestEntity(unittest.TestCase):

    def test_init(self):
        entity = Entity(text="test", label="test", start_index=0, end_index=4)
        self.assertEqual(entity.text, "test")
        self.assertEqual(entity.label, "test")
        self.assertEqual(entity.start_index, 0)
        self.assertEqual(entity.end_index, 4)
        self.assertEqual(entity.type, None)
        self.assertEqual(entity.regex, ".*")


if __name__ == "__main__":
    unittest.main()
